import logging

from requests import Session as RequestsSession
from gevent.event import Event
from gevent.lock import BoundedSemaphore
from apscheduler.schedulers.gevent import GeventScheduler
from couchdb import Database, Session

from openprocurement.auction.executor import AuctionsExecutor
from openprocurement.auction.worker.mixins import\
    DBServiceMixin, RequestIDServiceMixin, AuditServiceMixin,\
    DateTimeServiceMixin, BiddersServiceMixin, PostAuctionServiceMixin,\
    StagesServiceMixin, TIMEZONE

from openprocurement.auction.esco.tender_types import simple, multilot
from openprocurement.auction.esco.server import run_server


LOGGER = logging.getLogger('Auction Worker')
SCHEDULER = GeventScheduler(job_defaults={"misfire_grace_time": 100},
                                executors={'default': AuctionsExecutor()},
                                logger=LOGGER)
SCHEDULER.timezone = TIMEZONE


class EscoDBMixin(DBServiceMixin):

    def get_auction_info(self, prepare=False):
        self._type.get_auction_info(self, prepare)

    def prepare_auction_document(self):
        self.generate_request_id()
        public_document = self.get_auction_document()

        self.auction_document = {}
        if public_document:
            self.auction_document = {"_rev": public_document["_rev"]}
        if self.debug:
            self.auction_document['mode'] = 'test'
            self.auction_document['test_auction_data'] = deepcopy(self._auction_data)

        self.get_auction_info(prepare=True)
        if self.worker_defaults.get('sandbox_mode', False):
            submissionMethodDetails = self._auction_data['data'].get('submissionMethodDetails', '')
            if submissionMethodDetails == 'quick(mode:no-auction)':
                self._type.post_results_data(self, with_auctions_results=False)
                return 0
            elif submissionMethodDetails == 'quick(mode:fast-forward)':

                self._type.prepare_auction_document(self)
                if not self.debug:
                    self.set_auction_and_participation_urls()
                self.get_auction_info()
                self.prepare_auction_stages_fast_forward()
                self.save_auction_document()
                self._type.post_results_data(self, with_auctions_results=False)
                if hasattr(self, 'lot_id')
                    simple.announce_results_data(self, None)
                self.save_auction_document()
                return
        self._type.prepare_auction_document(self)

        self.save_auction_document()
        if not self.debug:
            self.set_auction_and_participation_urls()


class EscoPostAuctionMixin(PostAuctionServiceMixin):

    def put_auction_data(self):
        if self.worker_defaults.get('with_document_service', False):
            doc_id = self.upload_audit_file_with_document_service()
        else:
            doc_id = self.upload_audit_file_without_document_service()
        
        results = self._type.post_results_data(self)

        if results:
            if hasattr(self, 'lot_id'):
                bids_information = None
            else:
                bids_information = self._type.announce_results_data(self, results)

            if doc_id and bids_information:
                self.approve_audit_info_on_announcement(approved=bids_information)
                if self.worker_defaults.get('with_document_service', False):
                    doc_id = self.upload_audit_file_with_document_service(doc_id)
                else:
                    doc_id = self.upload_audit_file_without_document_service(doc_id)

                return True
        else:
            LOGGER.info(
                "Auctions results not approved",
                extra={"JOURNAL_REQUEST_ID": self.request_id,
                       "MESSAGE_ID": AUCTION_WORKER_API_AUCTION_RESULT_NOT_APPROVED}
            )

class EscoStagesMixin(StagesServiceMixin):
    def prepare_auction_stages_fast_forward(self):
        """TODO: """


class Auction(EscoDBMixin,
              RequestIDServiceMixin,
              AuditServiceMixin,
              BiddersServiceMixin,
              DateTimeServiceMixin,
              EscoStagesMixin,
              EscoPostAuctionMixin):
    """ESCO Auction Worker Class"""

    def __init__(self, tender_id,
                 worker_defaults={},
                 auction_data={},
                 lot_id=None):
        super(Auction, self).__init__()
        self.generate_request_id()
        self.tender_id = tender_id
        if lot_id:
            self.lot_id = lot_id
        self._type = multilot if lot_id else simple
        self.auction_doc_id = self._type.FORMATTER(tender_id=tender_id, lot_id=lot_id)
        self.tender_url = urljoin(
            worker_defaults["TENDERS_API_URL"],
            '/api/{0}/tenders/{1}'.format(
                worker_defaults["TENDERS_API_VERSION"], tender_id
            )
        )
        if auction_data:
            self.debug = True
            LOGGER.setLevel(logging.DEBUG)
            self._auction_data = auction_data
        else:
            self.debug = False
        self._end_auction_event = Event()
        self.bids_actions = BoundedSemaphore()
        self.session = RequestsSession()
        self.worker_defaults = worker_defaults
        if self.worker_defaults.get('with_document_service', False):
            self.session_ds = RequestsSession()
        self._bids_data = {}
        self.db = Database(str(self.worker_defaults["COUCH_DATABASE"]),
                           session=Session(retry_delays=range(10)))
        self.audit = {}
        self.retries = 10
        self.bidders_count = 0
        self.bidders_data = []
        self.mapping = {}
        self.rounds_stages = []

    def schedule_auction(self):
        self.generate_request_id()
        self.get_auction_document()
        if self.debug:
            LOGGER.info("Get _auction_data from auction_document")
            self._auction_data = self.auction_document.get('test_auction_data', {})
        self.get_auction_info()
        self.prepare_audit()
        self.prepare_auction_stages()
        self.save_auction_document()
        round_number = 0
        SCHEDULER.add_job(
            self.start_auction, 'date',
            kwargs={"switch_to_round": round_number},
            run_date=self.convert_datetime(
                self.auction_document['stages'][0]['start']
            ),
            name="Start of Auction",
            id="Start of Auction"
        )
        round_number += 1

        SCHEDULER.add_job(
            self.end_first_pause, 'date', kwargs={"switch_to_round": round_number},
            run_date=self.convert_datetime(
                self.auction_document['stages'][1]['start']
            ),
            name="End of Pause Stage: [0 -> 1]",
            id="End of Pause Stage: [0 -> 1]"
        )
        round_number += 1
        for index in xrange(2, len(self.auction_document['stages'])):
            if self.auction_document['stages'][index - 1]['type'] == 'bids':
                SCHEDULER.add_job(
                    self.end_bids_stage, 'date',
                    kwargs={"switch_to_round": round_number},
                    run_date=self.convert_datetime(
                        self.auction_document['stages'][index]['start']
                    ),
                    name="End of Bids Stage: [{} -> {}]".format(index - 1, index),
                    id="End of Bids Stage: [{} -> {}]".format(index - 1, index)
                )
            elif self.auction_document['stages'][index - 1]['type'] == 'pause':
                SCHEDULER.add_job(
                    self.next_stage, 'date',
                    kwargs={"switch_to_round": round_number},
                    run_date=self.convert_datetime(
                        self.auction_document['stages'][index]['start']
                    ),
                    name="End of Pause Stage: [{} -> {}]".format(index - 1, index),
                    id="End of Pause Stage: [{} -> {}]".format(index - 1, index)
                )
            round_number += 1
        LOGGER.info(
            "Prepare server ...",
            extra={"JOURNAL_REQUEST_ID": self.request_id,
                   "MESSAGE_ID": AUCTION_WORKER_SERVICE_PREPARE_SERVER}
        )
        self.server = run_server(self, self.convert_datetime(self.auction_document['stages'][-2]['start']), LOGGER)
import logging
from datetime import datetime, timedelta
from copy import deepcopy
from dateutil.tz import tzlocal
from barbecue import cooking
from fractions import Fraction


from openprocurement.auction.utils import\
    get_latest_bid_for_bidder, sorting_by_amount
from openprocurement.auction.worker.utils import prepare_service_stage
from openprocurement.auction.worker.constants import ROUNDS, BIDS_SECONDS,\
    FIRST_PAUSE_SECONDS, PAUSE_SECONDS
from openprocurement.auction.worker.journal import (
    AUCTION_WORKER_API_AUCTION_RESULT_NOT_APPROVED,
    AUCTION_WORKER_SERVICE_END_BID_STAGE,
    AUCTION_WORKER_SERVICE_START_STAGE,
    AUCTION_WORKER_BIDS_LATEST_BID_CANCELLATION
)
from openprocurement.auction.esco.constants import BIDS_KEYS_FOR_COPY
from openprocurement.auction.esco.auctions import simple, multilot
from openprocurement.auction.esco.utils import (
    prepare_initial_bid_stage, prepare_bids_stage, prepare_results_stage, sorting_start_bids_by_amount
)
from openprocurement.auction.worker.mixins import DBServiceMixin,\
    PostAuctionServiceMixin, StagesServiceMixin, BiddersServiceMixin, \
    AuditServiceMixin


LOGGER = logging.getLogger("Auction Esco")


class ESCODBServiceMixin(DBServiceMixin):
    """ Mixin class to work with couchdb"""

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
                if self.lot_id:
                    multilot.post_results_data(self, with_auctions_results=False)
                else:
                    simple.post_results_data(self, with_auctions_results=False)
                return 0
            elif submissionMethodDetails == 'quick(mode:fast-forward)':
                if self.lot_id:
                    self.auction_document = multilot.prepare_auction_document(self)
                else:
                    self.auction_document = simple.prepare_auction_document(self)
                if not self.debug:
                    self.set_auction_and_participation_urls()
                self.get_auction_info()
                self.prepare_auction_stages_fast_forward()
                self.save_auction_document()
                if self.lot_id:
                    multilot.post_results_data(self, with_auctions_results=False)
                else:
                    simple.post_results_data(self, with_auctions_results=False)
                    simple.announce_results_data(self, None)
                self.save_auction_document()
                return

        if self.lot_id:
            self.auction_document = multilot.prepare_auction_document(self)
        else:
            self.auction_document = simple.prepare_auction_document(self)

        self.save_auction_document()
        if not self.debug:
            self.set_auction_and_participation_urls()


class ESCOBiddersServiceMixin(BiddersServiceMixin):
    """Mixin class to work with bids data"""

    def filter_bids_keys(self, bids):
        filtered_bids_data = []
        for bid_info in bids:
            bid_info_result = {key: bid_info[key] for key in BIDS_KEYS_FOR_COPY}
            if self.features:
                bid_info_result['amount_features'] = bid_info['amount_features']
                bid_info_result['coeficient'] = bid_info['coeficient']
            bid_info_result["bidder_name"] = self.mapping[bid_info_result['bidder_id']]
            filtered_bids_data.append(bid_info_result)
        return filtered_bids_data

    def approve_bids_information(self):
        if self.current_stage in self._bids_data:
            LOGGER.info(
                "Current stage bids {}".format(self._bids_data[self.current_stage]),
                extra={"JOURNAL_REQUEST_ID": self.request_id}
            )

            bid_info = get_latest_bid_for_bidder(
                self._bids_data[self.current_stage],
                self.auction_document["stages"][self.current_stage]['bidder_id']
            )
            if bid_info['amount'] == -1.0:
                LOGGER.info(
                    "Latest bid is bid cancellation: {}".format(bid_info),
                    extra={"JOURNAL_REQUEST_ID": self.request_id,
                           "MESSAGE_ID": AUCTION_WORKER_BIDS_LATEST_BID_CANCELLATION}
                )
                return False
            bid_info = {key: bid_info[key] for key in BIDS_KEYS_FOR_COPY}
            bid_info["bidder_name"] = self.mapping[bid_info['bidder_id']]
            if self.features:
                bid_info['amount_features'] = str(Fraction(bid_info['amount']) * self.bidders_coeficient[bid_info['bidder_id']])
            self.auction_document["stages"][self.current_stage] = prepare_bids_stage(
                self.auction_document["stages"][self.current_stage],
                bid_info
            )
            self.auction_document["stages"][self.current_stage]["changed"] = True

            return True
        else:
            return False

class EscoPostAuctionMixin(PostAuctionServiceMixin):

    def put_auction_data(self):
        if self.worker_defaults.get('with_document_service', False):
            doc_id = self.upload_audit_file_with_document_service()
        else:
            doc_id = self.upload_audit_file_without_document_service()

        # results = self._type.post_results_data(self) TODO: initialize self._type field
        if self.lot_id:
            results = multilot.post_results_data(self)
        else:
            results = simple.post_results_data(self)

        if results:
            if self.lot_id:
                bids_information = None
            else:
                # bids_information = self._type.announce_results_data(self, results) TODO: initialize self._type field
                bids_information = simple.announce_results_data(self, results)

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
        self.auction_document['auction_type'] = 'meat' if self.features else 'default'
        bids = deepcopy(self.bidders_data)
        self.auction_document["initial_bids"] = []
        bids_info = sorting_start_bids_by_amount(bids, features=self.features, reverse=False)
        for index, bid in enumerate(bids_info):
            amount = bid["value"]["amountPerformance"]
            annualCostsReduction = bid["value"]["annualCostsReduction"]
            if self.features:
                amount_features = cooking(
                    amount,
                    self.features, self.bidders_features[bid["id"]],
                    reverse=True
                )
                coeficient = self.bidders_coeficient[bid["id"]]

            else:
                coeficient = None
                amount_features = None
            initial_bid_stage = prepare_initial_bid_stage(
                time=bid["date"] if "date" in bid else self.startDate,
                bidder_id=bid["id"],
                bidder_name=self.mapping[bid["id"]],
                amount=amount,
                coeficient=coeficient,
                amount_features=amount_features,
                annualCostsReduction=annualCostsReduction,
                yearlyPaymentsPercentage=bid["value"]["yearlyPaymentsPercentage"],
                contractDurationDays=bid["value"]["contractDurationDays"],
                contractDurationYears=bid["value"]["contractDurationYears"]
            )
            self.auction_document["initial_bids"].append(
                initial_bid_stage
            )
        self.auction_document['stages'] = []
        next_stage_timedelta = datetime.now(tzlocal())
        for round_id in xrange(ROUNDS):
            # Schedule PAUSE Stage
            pause_stage = prepare_service_stage(
                start=next_stage_timedelta.isoformat(),
                stage="pause"
            )
            self.auction_document['stages'].append(pause_stage)
            # Schedule BIDS Stages
            for index in xrange(self.bidders_count):
                bid_stage = prepare_bids_stage({
                    'start': next_stage_timedelta.isoformat(),
                    'bidder_id': '',
                    'bidder_name': '',
                    'amount': '0',
                    "contractDurationDays": "0",
                    "contractDurationYears": "0",
                    "yearlyPaymentsPercentage": "0",
                    'time': '',
                })
                self.auction_document['stages'].append(bid_stage)
                next_stage_timedelta += timedelta(seconds=BIDS_SECONDS)

        self.auction_document['stages'].append(
            prepare_service_stage(
                start=next_stage_timedelta.isoformat(),
                type="pre_announcement"
            )
        )
        self.auction_document['stages'].append(
            prepare_service_stage(
                start="",
                type="announcement"
            )
        )
        all_bids = deepcopy(self.auction_document["initial_bids"])
        minimal_bids = []
        for bid_info in self.bidders_data:
            minimal_bids.append(get_latest_bid_for_bidder(
                all_bids, str(bid_info['id'])
            ))

        minimal_bids = self.filter_bids_keys(sorting_by_amount(minimal_bids, reverse=False))
        self.update_future_bidding_orders(minimal_bids)

        self.auction_document['endDate'] = next_stage_timedelta.isoformat()
        self.auction_document["current_stage"] = len(self.auction_document["stages"]) - 2

    def end_bids_stage(self, switch_to_round=None):
        self.generate_request_id()
        self.bids_actions.acquire()
        self.get_auction_document()
        LOGGER.info(
            '---------------- End Bids Stage ----------------',
            extra={"JOURNAL_REQUEST_ID": self.request_id,
                   "MESSAGE_ID": AUCTION_WORKER_SERVICE_END_BID_STAGE}
        )

        self.current_round = self.get_round_number(
            self.auction_document["current_stage"]
        )
        self.current_stage = self.auction_document["current_stage"]

        if self.approve_bids_information():
            LOGGER.info("Approved bid on current stage")
            start_stage, end_stage = self.get_round_stages(self.current_round)
            all_bids = deepcopy(
                self.auction_document["stages"][start_stage:end_stage]
            )
            minimal_bids = []
            for bid_info in self.bidders_data:
                minimal_bids.append(
                    get_latest_bid_for_bidder(all_bids, bid_info['id'])
                )
            minimal_bids = self.filter_bids_keys(
                sorting_by_amount(minimal_bids, reverse=False)
            )
            self.update_future_bidding_orders(minimal_bids)

        self.approve_audit_info_on_bid_stage()

        if isinstance(switch_to_round, int):
            self.auction_document["current_stage"] = switch_to_round
        else:
            self.auction_document["current_stage"] += 1

        LOGGER.info('---------------- Start stage {0} ----------------'.format(
            self.auction_document["current_stage"]),
            extra={"JOURNAL_REQUEST_ID": self.request_id,
                   "MESSAGE_ID": AUCTION_WORKER_SERVICE_START_STAGE}
        )
        self.save_auction_document()
        if self.auction_document["stages"][self.auction_document["current_stage"]]['type'] == 'pre_announcement':
            self.end_auction()
        self.bids_actions.release()
        if self.auction_document["current_stage"] == (len(self.auction_document["stages"]) - 1):
            self._end_auction_event.set()

    def update_future_bidding_orders(self, bids):
        current_round = self.get_round_number(
            self.auction_document["current_stage"]
        )
        for round_number in range(current_round + 1, ROUNDS + 1):
            for index, stage in enumerate(
                    range(*self.get_round_stages(round_number))):

                self.auction_document["stages"][stage] = prepare_bids_stage(
                    self.auction_document["stages"][stage],
                    bids[index]
                )

        self.auction_document["results"] = []
        for item in bids:
            self.auction_document["results"].append(prepare_results_stage(**item))

    def prepare_auction_stages(self):
        # Initital Bids
        self.auction_document['auction_type'] = 'meat' if self.features else 'default'

        for bid_info in self.bidders_data:
            self.auction_document["initial_bids"].append(
                prepare_initial_bid_stage(
                    time="",
                    bidder_id=bid_info["id"],
                    bidder_name=self.mapping[bid_info["id"]],
                    amount="0",
                    yearlyPaymentsPercentage="0",
                    contractDurationYears="0",
                    contractDurationDays="0",
                    annualCostsReduction=[]
                )
            )
        self.auction_document['stages'] = []
        next_stage_timedelta = self.startDate
        for round_id in xrange(ROUNDS):
            # Schedule PAUSE Stage
            pause_stage = prepare_service_stage(
                start=next_stage_timedelta.isoformat(),
                stage="pause"
            )
            self.auction_document['stages'].append(pause_stage)
            if round_id == 0:
                next_stage_timedelta += timedelta(seconds=FIRST_PAUSE_SECONDS)
            else:
                next_stage_timedelta += timedelta(seconds=PAUSE_SECONDS)

            # Schedule BIDS Stages
            for index in xrange(self.bidders_count):
                bid_stage = prepare_bids_stage({
                    'start': next_stage_timedelta.isoformat(),
                    'bidder_id': '',
                    'bidder_name': '',
                    'amount': '0',
                    'contractDurationDays': '0',
                    'contractDurationYears': '0',
                    'yearlyPaymentsPercentage': '0',
                    'time': '',
                })

                self.auction_document['stages'].append(bid_stage)
                next_stage_timedelta += timedelta(seconds=BIDS_SECONDS)

        self.auction_document['stages'].append(
            prepare_service_stage(
                start=next_stage_timedelta.isoformat(),
                type="pre_announcement"
            )
        )
        self.auction_document['stages'].append(
            prepare_service_stage(
                start="",
                type="announcement"
            )
        )

        self.auction_document['endDate'] = next_stage_timedelta.isoformat()


class EscoAuditServiceMixin(AuditServiceMixin):

    def approve_audit_info_on_announcement(self, approved={}):
        self.audit['timeline']['results'] = {
            "time": datetime.now(tzlocal()).isoformat(),
            "bids": []
        }
        for bid in self.auction_document['results']:
            bid_result_audit = {
                'bidder': bid['bidder_id'],
                'amount': bid['amount'],
                "contractDuration": {
                    "years": bid["contractDurationYears"],
                    "days": bid["contractDurationDays"]
                },
                "yearlyPaymentsPercentage": bid["yearlyPaymentsPercentage"],
                'time': bid['time']
            }
            if approved:
                bid_result_audit["identification"] = approved[bid['bidder_id']]
            self.audit['timeline']['results']['bids'].append(bid_result_audit)

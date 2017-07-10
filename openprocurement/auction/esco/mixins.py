from openprocurement.auction.esco.auctions import simple, multilot
from openprocurement.auction.worker.mixins import DBServiceMixin,\
    PostAuctionServiceMixin, StagesServiceMixin


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
                if hasattr(self, 'lot_id'):
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
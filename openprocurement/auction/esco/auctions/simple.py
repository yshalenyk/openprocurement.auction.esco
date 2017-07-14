from openprocurement.auction.worker.auctions import simple
from openprocurement.auction.worker.utils import prepare_service_stage

FORMATTER = lambda **kw: "{}".format(kw.get('tender_id'))
MULTILINGUAL_FIELDS = ["title", "description"]
ADDITIONAL_LANGUAGES = ["ru", "en"]
ROUNDS = 3

# Indentical methods
get_auction_info = simple.get_auction_info
prepare_auction_and_participation_urls = simple.prepare_auction_and_participation_urls
announce_results_data = simple.announce_results_data

# auction_document['value'] ??
# auction_document['items'] ??
# auction_document['minimalStep'] ??
# TODO:
def prepare_auction_document(self):
    self.auction_document.update(
        {"_id": self.auction_doc_id,
         "stages": [],
         "tenderID": self._auction_data["data"].get("tenderID", ""),
         "procurementMethodType": self._auction_data["data"].get("procurementMethodType", "default"),
         "TENDERS_API_VERSION": self.worker_defaults["TENDERS_API_VERSION"],
         "initial_bids": [],
         "current_stage": -1,
         "NBUdiscountRate": self._auction_data["data"].get("NBUdiscountRate"),
         "results": [],
         "minimalStep": self._auction_data["data"].get("minimalStep", {}),
         "procuringEntity": self._auction_data["data"].get("procuringEntity", {}),
         "items": self._auction_data["data"].get("items", []),
         "value": self._auction_data["data"].get("value", {})}
    )
    if self.features:
        self.auction_document["auction_type"] = "meat"
    else:
        self.auction_document["auction_type"] = "default"

    for key in MULTILINGUAL_FIELDS:
        for lang in ADDITIONAL_LANGUAGES:
            lang_key = "{}_{}".format(key, lang)
            if lang_key in self._auction_data["data"]:
                self.auction_document[lang_key] = self._auction_data["data"][lang_key]
        self.auction_document[key] = self._auction_data["data"].get(key, "")

    self.auction_document['stages'].append(
        prepare_service_stage(
            start=self.startDate.isoformat(),
            type="pause"
        )
    )

    return self.auction_document

# bid["value"] ??
post_results_data = simple.post_results_data

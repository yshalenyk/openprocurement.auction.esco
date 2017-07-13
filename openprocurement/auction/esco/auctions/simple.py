from openprocurement.auction.worker.auctions import simple

FORMATTER = lambda **kw: "{}".format(kw.get('tender_id'))

# Indentical methods
get_auction_info = simple.get_auction_info
prepare_auction_and_participation_urls = simple.prepare_auction_and_participation_urls
announce_results_data = simple.announce_results_data

# auction_document['value'] ??
# auction_document['items'] ??
# auction_document['minimalStep'] ??
# TODO:
prepare_auction_document = simple.prepare_auction_document


# bid["value"] ??
post_results_data = simple.post_results_data

FORMATTER = lambda **kw: "{}_{}".format(kw.get('tender_id'), kw.get('lot_id'))

# Indentical methods
get_auction_info = multilot.get_auction_info
prepare_auction_and_participation_urls = multilot.prepare_auction_and_participation_urls
announce_results_data = multilot.announce_results_data

# auction_document['value'] ??
# auction_document['items'] ??
# auction_document['minimalStep'] ??
prepare_auction_document = multilot.prepare_auction_document
# bid["value"] ??
post_results_data = multilot.post_results_data
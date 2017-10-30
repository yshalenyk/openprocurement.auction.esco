# -*- coding: utf-8 -*-
from openprocurement.auction.esco.tests.unit.constants import AUCTIONS


def test_set_auction_and_participation_urls(universal_auction, mocker):
    mock_prepare_auction_and_participation_urls = mocker.MagicMock()
    base = 'openprocurement.auction.worker.auctions.{}.prepare_auction_and_participation_urls'
    mocker.patch(base.format('simple'),
                 mock_prepare_auction_and_participation_urls)
    mocker.patch(base.format('multilot'),
                 mock_prepare_auction_and_participation_urls)

    universal_auction.set_auction_and_participation_urls()

    mock_prepare_auction_and_participation_urls.assert_called_once_with(universal_auction)
    assert mock_prepare_auction_and_participation_urls.call_count == 1

# -*- coding: utf-8 -*-
import pytest

AUCTIONS = {
    'simple': 'openprocurement.auction.esco.auctions.simple',
    'multilot': 'openprocurement.auction.esco.auctions.multilot',
}


def test_get_auction_info(universal_auction, mocker):
    mock_get_auction_info = mocker.MagicMock()
    mocker.patch('{}.get_auction_info'.format(AUCTIONS['simple']), mock_get_auction_info)
    mocker.patch('{}.get_auction_info'.format(AUCTIONS['multilot']), mock_get_auction_info)

    universal_auction.get_auction_info()

    mock_get_auction_info.assert_called_once_with(universal_auction, False)

    universal_auction.get_auction_info(prepare=True)

    assert mock_get_auction_info.call_count == 2
    assert mock_get_auction_info.call_args[0] == (universal_auction, True)


@pytest.mark.parametrize(
    'get_result,document_keys',
    [(None, {'mode', 'test_auction_data', 'prepare_auction_document'}),
     ({'_rev': 'pub doc rev'}, {'mode', 'test_auction_data', 'prepare_auction_document', '_rev'})],
    ids=['without public document', 'with public document']
)
def test_prepare_auction_document_public_doc(universal_auction, mocker, get_result, document_keys):
    mocker.spy(universal_auction, 'generate_request_id')
    mocker.spy(universal_auction, 'get_auction_info')

    def mock_prepare_auction_document(auction_obj):
        auction_obj.auction_document['prepare_auction_document'] = 'called'
        return auction_obj.auction_document
    mocker.patch('{}.prepare_auction_document'.format(AUCTIONS['simple']), mock_prepare_auction_document)
    mocker.patch('{}.prepare_auction_document'.format(AUCTIONS['multilot']), mock_prepare_auction_document)

    mock_save_auction_document = mocker.patch.object(universal_auction, 'save_auction_document', autospec=True)

    mock_get_auction_document = mocker.patch.object(universal_auction, 'get_auction_document', autospec=True)
    mock_get_auction_document.return_value = get_result

    universal_auction.prepare_auction_document()

    assert universal_auction.generate_request_id.call_count == 1
    assert mock_get_auction_document.call_count == 1
    assert set(universal_auction.auction_document.keys()) == document_keys
    assert universal_auction.auction_document['mode'] == 'test'
    assert universal_auction.auction_document['test_auction_data'] == universal_auction._auction_data
    assert universal_auction.auction_document['prepare_auction_document'] == 'called'
    if get_result:
        assert universal_auction.auction_document['_rev'] == get_result['_rev']
    universal_auction.get_auction_info.assert_called_once_with(prepare=True)
    assert mock_save_auction_document.call_count == 1


@pytest.mark.parametrize(
    'debug,set_urls_count',
    [(True, 0),
     (False, 1)],
    ids=['with debug', 'without debug']
)
def test_prepare_auction_document_debug(universal_auction, mocker, debug, set_urls_count):
    universal_auction.debug = debug

    mocker.patch('{}.prepare_auction_document'.format(AUCTIONS['simple']), mocker.MagicMock())
    mocker.patch('{}.prepare_auction_document'.format(AUCTIONS['multilot']), mocker.MagicMock())
    mocker.patch.object(universal_auction, 'get_auction_info', autospec=True)

    mock_save_auction_document = mocker.patch.object(universal_auction, 'save_auction_document', autospec=True)
    mock_set_auction_and_participation_urls = mocker.patch.object(universal_auction, 'set_auction_and_participation_urls', autospec=True)

    universal_auction.prepare_auction_document()

    assert mock_save_auction_document.call_count == 1
    assert mock_set_auction_and_participation_urls.call_count == set_urls_count


def test_prepare_auction_document_smd_no_auction(universal_auction, mocker):
    mocker.spy(universal_auction, 'generate_request_id')
    mocker.spy(universal_auction, 'get_auction_info')

    mock_post_results_data = mocker.MagicMock()

    mocker.patch('{}.post_results_data'.format(AUCTIONS['simple']), mock_post_results_data)
    mocker.patch('{}.post_results_data'.format(AUCTIONS['multilot']), mock_post_results_data)

    universal_auction._auction_data['data']['submissionMethodDetails'] = 'quick(mode:no-auction)'
    result = universal_auction.prepare_auction_document()

    assert result == 0
    mock_post_results_data.assert_called_once_with(universal_auction, with_auctions_results=False)
    assert universal_auction.generate_request_id.call_count == 1
    universal_auction.get_auction_info.assert_called_once_with(prepare=True)


@pytest.mark.parametrize(
    'debug,set_urls_count,doc_keys',
    [(True, 0, {'mode', 'test_auction_data', 'prepare_auction_document'}),
     (False, 1, {'prepare_auction_document'})],
    ids=['with debug', 'without debug']
)
def test_prepare_auction_document_smd_fast_forward(universal_auction, mocker, debug, set_urls_count, doc_keys):
    mocker.patch.object(universal_auction, 'get_auction_info', autospec=True)

    def mock_prepare_auction_document(auction_obj):
        auction_obj.auction_document['prepare_auction_document'] = 'called'
        return auction_obj.auction_document
    mocker.patch('{}.prepare_auction_document'.format(AUCTIONS['simple']), mock_prepare_auction_document)
    mocker.patch('{}.prepare_auction_document'.format(AUCTIONS['multilot']), mock_prepare_auction_document)

    mock_post_results_data = mocker.MagicMock()
    mocker.patch('{}.post_results_data'.format(AUCTIONS['simple']), mock_post_results_data)
    mocker.patch('{}.post_results_data'.format(AUCTIONS['multilot']), mock_post_results_data)

    mock_announce_results_data = mocker.MagicMock()
    mocker.patch('{}.announce_results_data'.format(AUCTIONS['simple']), mock_announce_results_data)

    mock_save_auction_document = mocker.patch.object(universal_auction, 'save_auction_document', autospec=True)
    mock_prepare_auction_stages_fast_forward = mocker.patch.object(universal_auction, 'prepare_auction_stages_fast_forward', autospec=True)

    mock_set_auction_and_participation_urls = mocker.patch.object(universal_auction, 'set_auction_and_participation_urls', autospec=True)

    universal_auction._auction_data['data']['submissionMethodDetails'] = 'quick(mode:fast-forward)'
    universal_auction.debug = debug
    result = universal_auction.prepare_auction_document()

    assert result is None
    assert universal_auction.get_auction_info.call_count == 2
    assert mock_prepare_auction_stages_fast_forward.call_count == 1
    assert mock_save_auction_document.call_count == 2

    assert set(universal_auction.auction_document.keys()) == doc_keys
    if debug:
        assert universal_auction.auction_document['mode'] == 'test'
        assert universal_auction.auction_document['test_auction_data'] == universal_auction._auction_data
    assert universal_auction.auction_document['prepare_auction_document'] == 'called'

    mock_post_results_data.assert_called_once_with(universal_auction, with_auctions_results=False)
    assert mock_set_auction_and_participation_urls.call_count == set_urls_count

    if not universal_auction.lot_id:
        mock_announce_results_data.assert_called_once_with(universal_auction, None)

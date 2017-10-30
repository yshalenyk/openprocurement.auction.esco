# -*- coding: utf-8 -*-
from openprocurement.auction.esco.auctions import simple, multilot
from openprocurement.auction.esco.tests.unit.constants import AUCTIONS


def test_put_auction_data_without_dc(universal_auction, logger, mocker):
    # TODO: find out what actually '_type' field serves for
    if universal_auction.lot_id:
        universal_auction._type = multilot
    else:
        universal_auction._type = simple

    mock_upload_audit_file_without_document_service = mocker.patch.object(universal_auction,
                                                                          'upload_audit_file_without_document_service',
                                                                          autospec=True)
    mock_upload_audit_file_without_document_service.return_value = 'doc_id'

    mock_post_results_data = mocker.MagicMock(return_value=None)
    mocker.patch('{}.post_results_data'.format(AUCTIONS['simple']), mock_post_results_data)
    mocker.patch('{}.post_results_data'.format(AUCTIONS['multilot']), mock_post_results_data)

    result = universal_auction.put_auction_data()
    log_strings = logger.log_capture_string.getvalue().split('\n')

    assert result is None
    assert mock_upload_audit_file_without_document_service.call_count == 1
    mock_post_results_data.assert_called_once_with(universal_auction)
    assert log_strings[-2] == "Auctions results not approved"

    mock_post_results_data.return_value = 'results from post_results_data'

    mock_announce_results_data = mocker.MagicMock(return_value='bids_information')
    mocker.patch('{}.announce_results_data'.format(AUCTIONS['simple']), mock_announce_results_data)

    mock_approve_audit_info_on_announcement = mocker.patch.object(universal_auction,
                                                                  'approve_audit_info_on_announcement',
                                                                  autospec=True)
    result = universal_auction.put_auction_data()
    if universal_auction.lot_id:
        assert result is None
    else:
        assert result is True
        mock_announce_results_data.assert_called_once_with(universal_auction,
                                                           'results from post_results_data')
        mock_approve_audit_info_on_announcement.assert_called_once_with(approved='bids_information')
        assert mock_upload_audit_file_without_document_service.call_count == 3
        assert mock_upload_audit_file_without_document_service.call_args[0] == ('doc_id',)


def test_put_auction_data_with_dc(universal_auction, logger, mocker):
    universal_auction.worker_defaults['with_document_service'] = True
    # TODO: find out what actually '_type' field serves for
    if universal_auction.lot_id:
        universal_auction._type = multilot
    else:
        universal_auction._type = simple

    mock_upload_audit_file_with_document_service = mocker.patch.object(universal_auction,
                                                                       'upload_audit_file_with_document_service',
                                                                       autospec=True)
    mock_upload_audit_file_with_document_service.return_value = 'doc_id'

    mock_post_results_data = mocker.MagicMock(return_value=None)
    mocker.patch('{}.post_results_data'.format(AUCTIONS['simple']), mock_post_results_data)
    mocker.patch('{}.post_results_data'.format(AUCTIONS['multilot']), mock_post_results_data)

    result = universal_auction.put_auction_data()
    log_strings = logger.log_capture_string.getvalue().split('\n')

    assert result is None
    assert mock_upload_audit_file_with_document_service.call_count == 1
    mock_post_results_data.assert_called_once_with(universal_auction)
    assert log_strings[-2] == "Auctions results not approved"

    mock_post_results_data.return_value = 'results from post_results_data'

    mock_announce_results_data = mocker.MagicMock(return_value='bids_information')
    mocker.patch('{}.announce_results_data'.format(AUCTIONS['simple']), mock_announce_results_data)

    mock_approve_audit_info_on_announcement = mocker.patch.object(universal_auction,
                                                                  'approve_audit_info_on_announcement',
                                                                  autospec=True)
    result = universal_auction.put_auction_data()
    if universal_auction.lot_id:
        assert result is None
    else:
        assert result is True
        mock_announce_results_data.assert_called_once_with(universal_auction, 'results from post_results_data')
        mock_approve_audit_info_on_announcement.assert_called_once_with(approved='bids_information')
        assert mock_upload_audit_file_with_document_service.call_count == 3
        assert mock_upload_audit_file_with_document_service.call_args[0] == ('doc_id',)


def test_post_announce(universal_auction, mocker):
    mocker.spy(universal_auction, 'generate_request_id')
    mock_get_auction_document = mocker.patch.object(universal_auction, 'get_auction_document', autospec=True)
    mock_save_auction_document = mocker.patch.object(universal_auction, 'save_auction_document', autospec=True)
    mock_announce_results_data = mocker.MagicMock()
    base = 'openprocurement.auction.worker.auctions.{}.announce_results_data'
    mocker.patch(base.format('simple'), mock_announce_results_data)
    mocker.patch(base.format('multilot'), mock_announce_results_data)

    universal_auction.post_announce()

    assert universal_auction.generate_request_id.call_count == 1
    assert mock_get_auction_document.call_count == 1
    assert mock_save_auction_document.call_count == 1
    mock_announce_results_data.assert_called_once_with(universal_auction, None)

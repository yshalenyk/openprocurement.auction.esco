# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime, timedelta

from gevent.lock import BoundedSemaphore


from openprocurement.auction.esco.tests.data.data import tender_data, features_tender_data
from openprocurement.auction.esco import mixins


def test_prepare_auction_stages_fast_forward_no_features(auction, mocker):
    auction.auction_document = {"current_stage": -1}
    auction.bidders_count = 2
    auction.mapping = {u'5675acc9232942e8940a034994ad883e': '2', u'd3ba84c66c9e4f34bfb33cc3c686f137': '1'}
    auction.bidders_data = [
        {'date': u'2017-09-19T08:22:21.726234+00:00', 'id': u'd3ba84c66c9e4f34bfb33cc3c686f137', 'value': {
            u'yearlyPaymentsPercentage': 0.85, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9752.643835616438,
            u'contractDuration': {'years': 12, 'days': 200},
            u'amountPerformance': 850.1281928765416,
            u'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                      900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0]}},
        {'date': u'2017-09-19T08:22:24.038426+00:00', 'id': u'5675acc9232942e8940a034994ad883e', 'value': {
            u'yearlyPaymentsPercentage': 0.86, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9023.638356164383,
            u'contractDuration': {'years': 13, 'days': 40},
            u'amountPerformance': 672.4650719957199,
            u'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                      800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]}}]

    mock_prepare_initial_bid_stage = mocker.MagicMock(side_effect=[
        {'amount': 9023.638356164383,
         'yearlyPaymentsPercentage': 0.85,
         'contractDurationDays': 200,
         'contractDurationYears': 12,
         'annualCostsReduction': [200.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0],
         'bidder_id': u'5675acc9232942e8940a034994ad883e',
         'label': {'en': 'Bidder #2',
                   'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962',
                   'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962'},
         'time': '2017-09-19T08:22:24.038426+00:00'},
        {'amount': 9752.643835616438,
         'yearlyPaymentsPercentage': 0.86,
         'contractDurationDays': 40,
         'contractDurationYears': 13,
         'annualCostsReduction': [400.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0],
         'bidder_id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
         'label': {'en': 'Bidder #1',
                   'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961',
                   'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961'},
         'time': '2017-09-19T08:22:21.726234+00:00'}
    ])
    mocker.patch('openprocurement.auction.esco.mixins.prepare_initial_bid_stage', mock_prepare_initial_bid_stage)
    mock_datetime = mocker.MagicMock()
    mock_datetime.now.return_value = datetime(2017, 10, 10, 0, 0)
    mocker.patch('openprocurement.auction.esco.mixins.datetime', mock_datetime)

    mocker.spy(mixins, 'prepare_service_stage')
    mocker.spy(mixins, 'prepare_bids_stage')
    mocker.spy(auction, 'update_future_bidding_orders')
    auction.prepare_auction_stages_fast_forward()

    assert auction.auction_document['auction_type'] == 'default'
    assert mock_prepare_initial_bid_stage.call_count == len(features_tender_data['data']['bids'])
    assert len(auction.auction_document['initial_bids']) == len(features_tender_data['data']['bids'])
    # 3 rounds with stage for each bid and pause stage. And 2 stages at the end.
    assert len(auction.auction_document['stages']) == (len(features_tender_data['data']['bids']) + 1) * 3 + 2
    assert mixins.prepare_service_stage.call_count == 5
    assert mixins.prepare_bids_stage.call_count == 6
    auction.update_future_bidding_orders.assert_called_once_with(
        [{'amount': 9023.638356164383,
          'yearlyPaymentsPercentage': 0.85,
          'contractDurationDays': 200,
          'contractDurationYears': 12,
          'bidder_id': u'5675acc9232942e8940a034994ad883e',
          'bidder_name': '2',
          'time': '2017-09-19T08:22:24.038426+00:00'},
         {'amount': 9752.643835616438,
          'yearlyPaymentsPercentage': 0.86,
          'contractDurationDays': 40,
          'contractDurationYears': 13,
          'bidder_id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
          'bidder_name': '1',
          'time': '2017-09-19T08:22:21.726234+00:00'}
         ]
    )


def test_prepare_auction_stages_fast_forward_features(features_auction, db, mocker):
    # features_auction.get_auction_info()
    # import pdb; pdb.set_trace()
    features_auction.features = deepcopy(features_tender_data['data']['features'])
    features_auction.auction_document = {"current_stage": -1}
    features_auction.bidders_count = 2
    features_auction.mapping = {u'5675acc9232942e8940a034994ad883e': '2', u'd3ba84c66c9e4f34bfb33cc3c686f137': '1'}
    features_auction.bidders_coeficient = {u'5675acc9232942e8940a034994ad883e': 150, u'd3ba84c66c9e4f34bfb33cc3c686f137': 170}

    features_auction.bidders_data = [
        {'date': u'2017-09-19T08:22:21.726234+00:00', 'id': u'd3ba84c66c9e4f34bfb33cc3c686f137', 'value': {
            u'yearlyPaymentsPercentage': 0.85, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9752.643835616438,
            u'contractDuration': {'years': 12, 'days': 200},
            u'amountPerformance': 850.1281928765416,
            u'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                      900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0]}},
        {'date': u'2017-09-19T08:22:24.038426+00:00', 'id': u'5675acc9232942e8940a034994ad883e', 'value': {
            u'yearlyPaymentsPercentage': 0.86, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9023.638356164383,
            u'contractDuration': {'years': 13, 'days': 40},
            u'amountPerformance': 672.4650719957199,
            u'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                      800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]}}]
    features_auction.bidders_features = {
        u'5675acc9232942e8940a034994ad883e': [{u'code': u'OCDS-123454-AIR-INTAKE', u'value': 0.07},
                                              {u'code': u'OCDS-123454-YEARS', u'value': 0.07}],
        u'd3ba84c66c9e4f34bfb33cc3c686f137': [{u'code': u'OCDS-123454-AIR-INTAKE', u'value': 0.03},
                                              {u'code': u'OCDS-123454-YEARS', u'value': 0.03}]
    }

    mock_prepare_initial_bid_stage = mocker.MagicMock(side_effect=[
        {'amount': 9023.638356164383,
         'annualCostsReduction': [200.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0,
                                  800.0],
         'bidder_id': u'5675acc9232942e8940a034994ad883e',
         'label': {'en': 'Bidder #2',
                   'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962',
                   'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962'},
         'time': '2017-09-19T08:22:24.038426+00:00'},
        {'amount': 9752.643835616438,
         'annualCostsReduction': [400.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0,
                                  900.0],
         'bidder_id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
         'label': {'en': 'Bidder #1',
                   'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961',
                   'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961'},
         'time': '2017-09-19T08:22:21.726234+00:00'}
    ])
    mocker.patch('openprocurement.auction.esco.mixins.prepare_initial_bid_stage', mock_prepare_initial_bid_stage)
    mock_datetime = mocker.MagicMock()
    mock_datetime.now.return_value = datetime(2017, 10, 10, 0, 0)
    mocker.patch('openprocurement.auction.esco.mixins.datetime', mock_datetime)

    mocker.spy(mixins, 'prepare_service_stage')
    mocker.spy(mixins, 'prepare_bids_stage')
    mock_update_future_bidding_orders = mocker.MagicMock()
    mocker.patch.object(features_auction, 'update_future_bidding_orders', mock_update_future_bidding_orders)

    mock_cooking = mocker.MagicMock()
    mocker.patch('openprocurement.auction.esco.mixins.cooking', mock_cooking)
    mock_filter_bids_keys = mocker.MagicMock(return_value='sorted_bids')
    mocker.patch.object(features_auction, 'filter_bids_keys', mock_filter_bids_keys)

    features_auction.prepare_auction_stages_fast_forward()

    assert features_auction.auction_document['auction_type'] == 'meat'
    assert mock_prepare_initial_bid_stage.call_count == len(tender_data['data']['bids'])
    assert len(features_auction.auction_document['initial_bids']) == len(tender_data['data']['bids'])
    # 3 rounds with stage for each bid and pause stage. And 2 stages at the end.
    assert len(features_auction.auction_document['stages']) == (len(tender_data['data']['bids']) + 1) * 3 + 2
    assert mixins.prepare_service_stage.call_count == 5
    assert mixins.prepare_bids_stage.call_count == 6
    mock_update_future_bidding_orders.assert_called_once_with('sorted_bids')
    assert mock_cooking.call_count == 2


def test_end_bids_stage(auction, mocker, logger):
    auction.bidders_data = [
        {'date': u'2017-09-19T08:22:21.726234+00:00', 'id': u'd3ba84c66c9e4f34bfb33cc3c686f137', 'value': {
            u'yearlyPaymentsPercentage': 0.85, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9752.643835616438, u'contractDuration': {u'days': 200, u'years': 12},
            u'amountPerformance': 850.1281928765416,
            u'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                      900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0]}},
        {'date': u'2017-09-19T08:22:24.038426+00:00', 'id': u'5675acc9232942e8940a034994ad883e', 'value': {
            u'yearlyPaymentsPercentage': 0.86, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9023.638356164383, u'contractDuration': {u'days': 40, u'years': 13},
            u'amountPerformance': 672.4650719957199,
            u'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                      800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]}}]
    auction.auction_document = {'current_stage': 0, 'stages': [
        {'type': 'bid_stage'}, {'type': 'bid_stage'}, {'type': 'pre_announcement'}, {'type': 'announcement'}
    ]}
    mocker.spy(auction, 'generate_request_id')
    mock_bids_actions = mocker.patch.object(auction, 'bids_actions', autospec=True)

    mock_get_auction_document = mocker.patch.object(auction, 'get_auction_document', autospec=True)
    mock_save_auction_document = mocker.patch.object(auction, 'save_auction_document', autospec=True)
    mock_approve_audit_info_on_bid_stage = mocker.patch.object(auction, 'approve_audit_info_on_bid_stage', autospec=True)
    mock_update_future_bidding_orders = mocker.patch.object(auction, 'update_future_bidding_orders', autospec=True)
    mock_filter_bids_keys = mocker.patch.object(auction, 'filter_bids_keys', autospec=True)
    mock_filter_bids_keys.return_value = 'minimal_bid'
    mocker.patch('openprocurement.auction.esco.mixins.sorting_by_amount', mocker.MagicMock())

    mock_approve_bids_information = mocker.patch.object(auction, 'approve_bids_information', autospec=True)
    mock_approve_bids_information.return_value = True

    mock_get_latest_bid_for_bidder = mocker.MagicMock(return_value='latest bidder bid')
    mocker.patch('openprocurement.auction.esco.mixins.get_latest_bid_for_bidder', mock_get_latest_bid_for_bidder)

    auction.end_bids_stage()
    log_strings = logger.log_capture_string.getvalue().split('\n')

    assert log_strings[-4] == '---------------- End Bids Stage ----------------'
    assert auction.generate_request_id.call_count == 1
    assert mock_bids_actions.acquire.call_count == 1
    assert mock_get_auction_document.call_count == 1
    assert mock_approve_bids_information.call_count == 1
    assert log_strings[-3] == 'Approved bid on current stage'
    assert mock_get_latest_bid_for_bidder.call_count == 2
    assert mock_filter_bids_keys.call_count == 1
    mock_update_future_bidding_orders.assert_called_once_with('minimal_bid')
    assert mock_approve_audit_info_on_bid_stage.call_count == 1
    assert log_strings[-2] == '---------------- Start stage 1 ----------------'
    assert mock_save_auction_document.call_count == 1

    mock_end_auction = mocker.patch.object(auction, 'end_auction', autospec=True)

    auction.auction_document['current_stage'] = 1
    auction.end_bids_stage()

    assert mock_end_auction.call_count == 1

    mock_end_auction_event = mocker.patch.object(auction, '_end_auction_event', autospec=True)

    auction.end_bids_stage(3)

    assert mock_end_auction_event.set.call_count == 1


def test_update_future_bidding_orders(auction, mocker):
    auction.auction_document = {"current_stage": -1, 'initial_bids': [], 'stages': ['','','','','','','','','','','']}
    auction.bidders_count = 2
    auction.mapping = {u'5675acc9232942e8940a034994ad883e': '2', u'd3ba84c66c9e4f34bfb33cc3c686f137': '1'}
    auction.bidders_data = [
        {'date': u'2017-09-19T08:22:21.726234+00:00', 'id': u'd3ba84c66c9e4f34bfb33cc3c686f137', 'value': {
            u'yearlyPaymentsPercentage': 0.85, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9752.643835616438, u'contractDuration': {u'days': 200, u'years': 12},
            u'amountPerformance': 850.1281928765416,
            u'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                      900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0]}},
        {'date': u'2017-09-19T08:22:24.038426+00:00', 'id': u'5675acc9232942e8940a034994ad883e', 'value': {
            u'yearlyPaymentsPercentage': 0.86, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9023.638356164383, u'contractDuration': {u'days': 40, u'years': 13},
            u'amountPerformance': 672.4650719957199,
            u'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                      800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]}}]

    mock_prepare_bids_stage = mocker.MagicMock(return_value='prepared_bids_stage')
    mocker.patch('openprocurement.auction.esco.mixins.prepare_bids_stage', mock_prepare_bids_stage)
    mock_prepare_results_stage = mocker.MagicMock(return_value='prepared_results_stage')
    mocker.patch('openprocurement.auction.esco.mixins.prepare_results_stage', mock_prepare_results_stage)

    mock_get_round_number = mocker.patch.object(auction, 'get_round_number', autospec=True)
    mock_get_round_number.return_value = 2

    mocker.spy(auction, 'get_round_stages')

    auction.update_future_bidding_orders([{'bid_1': 'bid_1'}, {'bid_2': 'bid_2'}])

    assert auction.auction_document['results'] == ['prepared_results_stage', 'prepared_results_stage']
    assert auction.auction_document['stages'][7] == 'prepared_bids_stage'
    assert auction.auction_document['stages'][8] == 'prepared_bids_stage'

    mock_get_round_number.assert_called_once_with(-1)
    assert auction.get_round_stages.call_count == 1
    assert mock_prepare_bids_stage.call_count == 2
    assert mock_prepare_results_stage.call_count == 2


def test_prepare_auction_stages(auction, mocker):
    auction.startDate = datetime(2017, 10, 10, 0, 0)
    auction.auction_document = {"current_stage": -1, 'initial_bids': []}
    auction.bidders_count = 2
    auction.mapping = {u'5675acc9232942e8940a034994ad883e': '2', u'd3ba84c66c9e4f34bfb33cc3c686f137': '1'}
    auction.bidders_data = [
        {'date': u'2017-09-19T08:22:21.726234+00:00', 'id': u'd3ba84c66c9e4f34bfb33cc3c686f137', 'value': {
            u'yearlyPaymentsPercentage': 0.85, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9752.643835616438, u'contractDuration': {u'days': 200, u'years': 12},
            u'amountPerformance': 850.1281928765416,
            u'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                      900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0]}},
        {'date': u'2017-09-19T08:22:24.038426+00:00', 'id': u'5675acc9232942e8940a034994ad883e', 'value': {
            u'yearlyPaymentsPercentage': 0.86, u'valueAddedTaxIncluded': True, u'currency': u'UAH',
            u'amount': 9023.638356164383, u'contractDuration': {u'days': 40, u'years': 13},
            u'amountPerformance': 672.4650719957199,
            u'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                      800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]}}]

    mock_prepare_initial_bid_stage = mocker.MagicMock(side_effect=[
        {'amount': '0',
         'annualCostsReduction': '0',
         'bidder_id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
         'label': {'en': 'Bidder #1',
                   'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961',
                   'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961'},
         'time': ''},
        {'amount': '0',
         'annualCostsReduction': '0',
         'bidder_id': u'5675acc9232942e8940a034994ad883e',
         'label': {'en': 'Bidder #2',
                   'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962',
                   'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962'},
         'time': ''}])
    mocker.patch('openprocurement.auction.esco.mixins.prepare_initial_bid_stage', mock_prepare_initial_bid_stage)
    mocker.spy(mixins, 'prepare_service_stage')
    mocker.spy(mixins, 'prepare_bids_stage')

    auction.prepare_auction_stages()

    assert auction.auction_document['auction_type'] == 'default'
    assert mock_prepare_initial_bid_stage.call_count == len(tender_data['data']['bids'])
    assert len(auction.auction_document['initial_bids']) == len(tender_data['data']['bids'])
    # 3 rounds with stage for each bid and pause stage. And 2 stages at the end.
    assert len(auction.auction_document['stages']) == (len(tender_data['data']['bids']) + 1) * 3 + 2
    assert mixins.prepare_service_stage.call_count == 5
    assert mixins.prepare_bids_stage.call_count == 6

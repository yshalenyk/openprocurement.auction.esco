# -*- coding: utf-8 -*-
import pytest

from datetime import datetime


@pytest.mark.parametrize(
    'input, expected', [
        (
            {
                'results': [
                    {
                        'bidder_id': '5675acc9232942e8940a034994ad883e',
                        'time': '2017-09-19T08:22:24.038426+00:00',
                        'amount': 9023.638356164383,
                        'contractDurationYears': 12,
                        'contractDurationDays': 256,
                        'yearlyPaymentsPercentage': 0.65,
                    },
                    {
                        'bidder_id': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                        'time': '2017-09-19T08:25:24.038426+00:00',
                        'amount': 8567.638356164383,
                        'contractDurationYears': 10,
                        'contractDurationDays': 186,
                        'yearlyPaymentsPercentage': 0.80,
                    },
                ],
                'approved': None

            },
            {'timeline': {
                'results': {'bids': [
                    {'amount': 9023.638356164383,
                     'bidder': '5675acc9232942e8940a034994ad883e',
                     'contractDuration': {'days': 256,
                                          'years': 12},
                     'time': '2017-09-19T08:22:24.038426+00:00',
                     'yearlyPaymentsPercentage': 0.65},
                    {'amount': 8567.638356164383,
                     'bidder': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                     'contractDuration': {'days': 186,
                                          'years': 10},
                     'time': '2017-09-19T08:25:24.038426+00:00',
                     'yearlyPaymentsPercentage': 0.8}
                ],
                          'time': '2017-10-10T00:00:00'}
            }}

        ),
        (
            {
                'results': [
                    {
                        'bidder_id': '5675acc9232942e8940a034994ad883e',
                        'time': '2017-09-19T08:22:24.038426+00:00',
                        'amount': 9023.638356164383,
                        'contractDurationYears': 12,
                        'contractDurationDays': 256,
                        'yearlyPaymentsPercentage': 0.65,
                    },
                    {
                        'bidder_id': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                        'time': '2017-09-19T08:25:24.038426+00:00',
                        'amount': 8567.638356164383,
                        'contractDurationYears': 10,
                        'contractDurationDays': 186,
                        'yearlyPaymentsPercentage': 0.80,
                    },
                ],
                'approved': {
                    '5675acc9232942e8940a034994ad883e': 'info from approved dict',
                    'd3ba84c66c9e4f34bfb33cc3c686f137': 'info from approved dict'
                }

            },
            {'timeline': {
                'results': {'bids': [
                    {'amount': 9023.638356164383,
                     'identification': 'info from approved dict',
                     'bidder': '5675acc9232942e8940a034994ad883e',
                     'contractDuration': {'days': 256,
                                          'years': 12},
                     'time': '2017-09-19T08:22:24.038426+00:00',
                     'yearlyPaymentsPercentage': 0.65},
                    {'amount': 8567.638356164383,
                     'identification': 'info from approved dict',
                     'bidder': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                     'contractDuration': {'days': 186,
                                          'years': 10},
                     'time': '2017-09-19T08:25:24.038426+00:00',
                     'yearlyPaymentsPercentage': 0.8}
                ],
                          'time': '2017-10-10T00:00:00'}
            }}

        ),

    ], ids=['not approved', 'approved']
)
def test_approve_audit_info_on_announcement(auction, mocker, input, expected):
    mock_datetime = mocker.MagicMock()
    mock_datetime.now.return_value = datetime(2017, 10, 10, 0, 0)
    mocker.patch('openprocurement.auction.esco.mixins.datetime', mock_datetime)

    auction.auction_document = {'results': input['results']}
    auction.audit = {'timeline': {}}

    auction.approve_audit_info_on_announcement(approved=input['approved'])

    assert auction.audit == expected

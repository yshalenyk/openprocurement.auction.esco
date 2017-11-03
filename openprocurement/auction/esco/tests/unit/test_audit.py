# -*- coding: utf-8 -*-
import pytest

from datetime import datetime
from fractions import Fraction


@pytest.mark.parametrize(
    'input, expected', [
        (
            {
                'results': [
                    {
                        'bidder_id': '5675acc9232942e8940a034994ad883e',
                        'time': '2017-09-19T08:22:24.038426+00:00',
                        'amount': Fraction(9023.638356164383),
                        'contractDurationYears': 12,
                        'contractDurationDays': 256,
                        'yearlyPaymentsPercentage': 0.65,
                    },
                    {
                        'bidder_id': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                        'time': '2017-09-19T08:25:24.038426+00:00',
                        'amount': Fraction(8567.638356164383),
                        'contractDurationYears': 10,
                        'contractDurationDays': 186,
                        'yearlyPaymentsPercentage': 0.80,
                    },
                ],
                'approved': None

            },
            {'timeline': {
                'results': {'bids': [
                    {'amount': '4960797648724125/549755813888',
                     'bidder': '5675acc9232942e8940a034994ad883e',
                     'contractDuration': {'days': 256,
                                          'years': 12},
                     'time': '2017-09-19T08:22:24.038426+00:00',
                     'yearlyPaymentsPercentage': 0.65},
                    {'amount': '4710108997591197/549755813888',
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
                        'amount': Fraction(9023.638356164383),
                        'contractDurationYears': 12,
                        'contractDurationDays': 256,
                        'yearlyPaymentsPercentage': 0.65,
                    },
                    {
                        'bidder_id': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                        'time': '2017-09-19T08:25:24.038426+00:00',
                        'amount': Fraction(8567.638356164383),
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
                    {'amount': '4960797648724125/549755813888',
                     'identification': 'info from approved dict',
                     'bidder': '5675acc9232942e8940a034994ad883e',
                     'contractDuration': {'days': 256,
                                          'years': 12},
                     'time': '2017-09-19T08:22:24.038426+00:00',
                     'yearlyPaymentsPercentage': 0.65},
                    {'amount': '4710108997591197/549755813888',
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


@pytest.mark.parametrize(
    'stage_data,features,expected_result',
    [
        (
            {
                'bidder_id': '5675acc9232942e8940a034994ad883e',
                'time': '2017-09-19T08:22:24.038426+00:00',
                'amount': Fraction(9023.638356164383),
                'contractDurationYears': 12,
                'contractDurationDays': 256,
                'yearlyPaymentsPercentage': 0.65,
            },

            None,

            {'timeline': {'round_2': {'turn_1': {
                 'amount': '4960797648724125/549755813888',
                 'bid_time': '2017-09-19T08:22:24.038426+00:00',
                 'bidder': '5675acc9232942e8940a034994ad883e',
                 'contractDurationDays': 256,
                 'contractDurationYears': 12,
                 'time': '2017-10-10T00:00:00',
                 'yearlyPaymentsPercentage': 0.65}}}}
        ),
        (
            {
                'bidder_id': '5675acc9232942e8940a034994ad883e',
                'time': '2017-09-19T08:22:24.038426+00:00',
                'amount': Fraction(9023.638356164383),
                'amount_features': '126079764343212387212341252323/549751235813882328',
                'coeficient': '4818851601286431/4503599627370496',
                'contractDurationYears': 12,
                'contractDurationDays': 256,
                'yearlyPaymentsPercentage': 0.65,
            },

            [
                {
                    "code": "OCDS-123454-AIR-INTAKE",
                    "description": "Ефективна потужність всмоктування пилососа, в ватах (аероватах)",
                    "title": "Потужність всмоктування",
                    "enum": [
                        {
                            "value": 0.03,
                            "title": "До 1000 Вт"
                        },
                        {
                            "value": 0.07,
                            "title": "Більше 1000 Вт"
                        }
                    ],
                    "title_en": "Air Intake",
                    "relatedItem": "c990f6a7918e4fb495a913db51284af3",
                    "featureOf": "item"
                },
                {
                    "code": "OCDS-123454-YEARS",
                    "description": "Кількість років, які організація учасник працює на ринку",
                    "title": "Років на ринку",
                    "enum": [
                        {
                            "value": 0.03,
                            "title": "До 3 років"
                        },
                        {
                            "value": 0.05,
                            "title": "Більше 3 років, менше 5 років"
                        },
                        {
                            "value": 0.07,
                            "title": "Більше 5 років"
                        }
                    ],
                    "title_en": "Years trading",
                    "featureOf": "tenderer"
                }
            ],

            {'timeline': {'round_2': {'turn_1': {
                 'amount': '4960797648724125/549755813888',
                 'amount_features': '126079764343212387212341252323/549751235813882328',
                 'coeficient': '4818851601286431/4503599627370496',
                 'bid_time': '2017-09-19T08:22:24.038426+00:00',
                 'bidder': '5675acc9232942e8940a034994ad883e',
                 'contractDurationDays': 256,
                 'contractDurationYears': 12,
                 'time': '2017-10-10T00:00:00',
                 'yearlyPaymentsPercentage': 0.65}}}}
        ),

    ]
)
def test_approve_audit_info_on_bid_stage(auction, mocker, stage_data, features, expected_result):
    auction.current_round = 2
    auction.bidders_count = 2
    auction.current_stage = 4

    mock_datetime = mocker.MagicMock()
    mock_datetime.now.return_value = datetime(2017, 10, 10, 0, 0)
    mocker.patch('openprocurement.auction.esco.mixins.datetime', mock_datetime)

    auction.auction_document = {'stages': {auction.current_stage: {'changed': True}}}
    auction.auction_document['stages'][auction.current_stage].update(stage_data)
    auction.audit = {'timeline': {'round_2': {'turn_1': {}}}}

    auction.features = features

    auction.approve_audit_info_on_bid_stage()
    assert auction.audit == expected_result

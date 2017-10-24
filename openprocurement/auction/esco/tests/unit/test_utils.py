# -*- coding: utf-8 -*-
import pytest

from fractions import Fraction

from openprocurement.auction.esco.utils import prepare_initial_bid_stage


@pytest.mark.parametrize(
    'input,expected', [
        (
            {
                'bidder_name': '2',
                'bidder_id': '5675acc9232942e8940a034994ad883e',
                'time': '2017-09-19T08:22:24.038426+00:00',
                'contractDurationDays': 252,
                'contractDurationYears': 8,
                'amount': 9023.638356164383,
                'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                         800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]
            },
            {
                'amount': 9023.638356164383,
                'contractDurationDays': 252,
                'contractDurationYears': 8,
                'yearlyPaymentsPercentage': 0,
                'annualCostsReduction': [200.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0,
                                         800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0],
                'bidder_id': u'5675acc9232942e8940a034994ad883e',
                'label': {'en': 'Bidder #2',
                          'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962',
                          'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962'},
                'time': '2017-09-19T08:22:24.038426+00:00'
             }
        ),
        (
            {
                'bidder_name': '1',
                'bidder_id': 'd3ba84c66c9e4f34bfb33cc3c686f137',
                'time': '2017-09-19T08:22:21.726234+00:00',
                'amount_features': Fraction(41531767727917712194043060279553, 4555619344570199334662963200),
                'coeficient': Fraction(16573246628723425, 15492382718154506),
                'amount': 9752.643835616438,
                'yearlyPaymentsPercentage': 0.82,
                'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                         900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0]
            },
            {
                'amount': 9752.643835616438,
                'contractDurationDays': 0,
                'contractDurationYears': 0,
                'yearlyPaymentsPercentage': 0.82,
                'annualCostsReduction': [400.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0,
                                         900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0, 900.0],
                'bidder_id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
                'label': {'en': 'Bidder #1',
                          'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961',
                          'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x961'},
                'amount_features': '41531767727917712194043060279553/4555619344570199334662963200',
                'coeficient': '16573246628723425/15492382718154506',
                'time': '2017-09-19T08:22:21.726234+00:00'
            }
        ),
        (
            {
                'bidder_name': '2',
                'bidder_id': '5675acc9232942e8940a034994ad883e',
                'time': '2017-09-19T08:22:24.038426+00:00',
                'amount': 9023.638356164383,
                'contractDurationDays': 252,
                'contractDurationYears': 8,
                'yearlyPaymentsPercentage': 0.65,
            },
            {
                'amount': 9023.638356164383,
                'contractDurationDays': 252,
                'contractDurationYears': 8,
                'yearlyPaymentsPercentage': 0.65,
                'annualCostsReduction': [],
                'bidder_id': u'5675acc9232942e8940a034994ad883e',
                'label': {'en': 'Bidder #2',
                          'ru': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962',
                          'uk': '\xd0\xa3\xd1\x87\xd0\xb0\xd1\x81\xd0\xbd\xd0\xb8\xd0\xba \xe2\x84\x962'},
                'time': '2017-09-19T08:22:24.038426+00:00'
             }
        ),


    ], ids=['without features', 'with features', 'without annualCostsReduction']
)
def test_prepare_initial_bid_stage(input, expected):
    result = prepare_initial_bid_stage(**input)
    assert result == expected

# -*- coding: utf-8 -*-

from fractions import Fraction

from openprocurement.auction.esco.constants import NPV_CALCULATION_DURATION, DAYS_IN_YEAR

def prepare_initial_bid_stage(bidder_name="", bidder_id="", time="",
                              amount_features="", coeficient="", amount="", annualCostsReduction=[]):
    stage = dict(bidder_id=bidder_id, time=str(time))
    stage["label"] = dict(
        en="Bidder #{}".format(bidder_name),
        uk="Учасник №{}".format(bidder_name),
        ru="Участник №{}".format(bidder_name)
    )
    stage['amount'] = amount if amount else 0
    stage['annualCostsReduction'] = annualCostsReduction
    if amount_features is not None and amount_features != "":
        stage['amount_features'] = str(amount_features)
    if coeficient:
        stage['coeficient'] = str(coeficient)
    return stage

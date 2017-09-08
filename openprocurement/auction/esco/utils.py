# -*- coding: utf-8 -*-

from fractions import Fraction

from openprocurement.auction.esco.constants import NPV_CALCULATION_DURATION, DAYS_IN_YEAR

def prepare_initial_bid_stage(bidder_name="", bidder_id="", time="",
                              amount_features="", coeficient="", amount="", annualCostsReduction=""):
    stage = dict(bidder_id=bidder_id, time=str(time))
    stage["label"] = dict(
        en="Bidder #{}".format(bidder_name),
        uk="Учасник №{}".format(bidder_name),
        ru="Участник №{}".format(bidder_name)
    )
    stage['amount'] = amount if amount else 0
    stage['annualCostsReduction'] = annualCostsReduction if annualCostsReduction else 0
    if amount_features is not None and amount_features != "":
        stage['amount_features'] = str(amount_features)
    if coeficient:
        stage['coeficient'] = str(coeficient)
    return stage


def calculate_npv(nbu_rate,
                  annual_costs_reduction,
                  contract_duration,
                  yearlyPaymentsPercentage=0.0,
                  contractDurationDays=0):
    yearly_payments = calculate_yearly_payments(annual_costs_reduction, yearlyPaymentsPercentage)
    if contractDurationDays:
        CF_incomplete = lambda n: Fraction(Fraction("{}/{}".format(contractDurationDays, DAYS_IN_YEAR)) * yearly_payments) if n == int(contract_duration + 1) else 0
    else:
        CF_incomplete = lambda n: 0
    CF = lambda n: yearly_payments if n <= int(contract_duration) else CF_incomplete(n)
    return sum([
        Fraction(annual_costs_reduction - CF(n)) / (Fraction(1 + nbu_rate) ** n)
        for n in range(1, int(NPV_CALCULATION_DURATION) + 1)
    ])


def calculate_yearly_payments(annual_costs_reduction, yearlyPaymentsPercentage):
    return Fraction(annual_costs_reduction) * Fraction(yearlyPaymentsPercentage)


def post_results_data(self, with_auctions_results=True):
    """TODO: make me work"""


def announce_results_data(self, results=None):
    """TODO: make me work"""

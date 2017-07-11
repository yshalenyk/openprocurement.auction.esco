from fractions import Fraction

from openprocurement.auction.esco.constants import NPV_CALCULATION_DURATION, DAYS_IN_YEAR


def calculate_npv(nbu_rate,
                  annual_costs_reduction,
                  yearlyPayments,
                  contractDuration,
                  yearlyPaymentsPercentage=0.0,
                  contractDurationDays=0
                 ):
    assert not (yearlyPayments and yearlyPaymentsPercentage)
    if yearlyPaymentsPercentage:
        yearlyPayments = calculate_yearly_payments(annual_costs_reduction, yearlyPaymentsPercentage)
    if contract_duration_days:
        CF_incomplete = lambda n: Fraction(Fraction("{}/{}".format(contract_duration_days, DAYS_IN_YEAR)) * yearly_payments) if n == int(contract_duration + 1) else 0
    else:
        CF_incomplete = lambda n: 0
    CF = lambda n: yearly_payments if n <= int(contract_duration) else CF_incomplete(n)
    return sum([
        Fraction(annual_costs_reduction - CF(n)) / (Fraction(1 + nbu_rate) ** n)
        for n in range(1, int(NPV_CALCULATION_DURATION) + 1)
    ])


def calculate_yearly_payments(annual_costs_reduction, yearlyPaymentsPercentage):
    return Fraction(annual_costs_reduction * yearlyPaymentsPercentage)

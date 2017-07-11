from fractions import Fraction

from openprocurement.auction.esco.constants import NPV_CALCULATION_DURATION, DAYS_IN_YEAR


def calculate_npv(nbu_rate,
                  annual_costs_reduction,
                  yearly_payments,
                  contract_duration,
                  contract_duration_days=0
                 ):
    if contract_duration_days:
        CF_incomplete = lambda n: Fraction(Fraction("{}/{}".format(contract_duration_days, DAYS_IN_YEAR)) * yearly_payments) if n == int(contract_duration + 1) else 0
    else:
        CF_incomplete = lambda n: 0
    CF = lambda n: yearly_payments if n <= int(contract_duration) else CF_incomplete(n)
    return sum([
        Fraction(annual_costs_reduction - CF(n)) / (Fraction(1 + nbu_rate) ** n)
        for n in range(1, int(NPV_CALCULATION_DURATION) + 1)
    ])

#
# def sorting_by_amount(bids, reverse=True):
#     def bids_compare(left, right):
#         if "amount_features" in bid1 and "amount_features" in bid2:
#             full_amount_bid1 = Fraction(bid1["amount_features"])
#             full_amount_bid2 = Fraction(bid2["amount_features"])
#         else:
#             full_amount_bid1 = Fraction(bid1["amount"])
#             full_amount_bid2 = Fraction(bid2["amount"])
#         if full_amount_bid1 == full_amount_bid2:
#             time_of_bid1 = get_time(bid1)
#             time_of_bid2 = get_time(bid2)
#             return - cmp(time_of_bid2, time_of_bid1)
#         else:
#             return cmp(full_amount_bid1, full_amount_bid2)
#      return sorted(bids, reverse=reverse, cmp=bids_compare)

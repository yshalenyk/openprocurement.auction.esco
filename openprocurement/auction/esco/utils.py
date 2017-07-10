from fractions import Fraction

NPV_CALCULATION_DURATION = 20  # accounting period, years
MAX_CONTRACT_DURATION = 15  # maximum duration of contract, years
DAYS_IN_YEAR = 365  # number days in one year, used for calculation
ROUNDNESS = 3  # NPV accuracy level


def calculate_npv(nbu_rate, annualCostsReduction, yearlyPayments,
                  contractDurationYears, contractDurationDays=0):
    contract_duration = Fraction((contractDurationYears * DAYS_IN_YEAR + contractDurationDays), DAYS_IN_YEAR)
    if contract_duration > MAX_CONTRACT_DURATION:
        return False
    cf_free = annualCostsReduction
    cf = cf_free - yearlyPayments
    cf_days = cf_free - (yearlyPayments/DAYS_IN_YEAR)*contractDurationDays
    value = sum([(cf if i <= contract_duration else
                  cf_days if contract_duration < i < contract_duration + 1 else
                  cf_free)
                 / (1 + nbu_rate)**i for i in range(1, NPV_CALCULATION_DURATION + 1)])
    return round(value, ROUNDNESS)

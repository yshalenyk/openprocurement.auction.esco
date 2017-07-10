NPV_CALCULATION_DURATION = 20  # accounting period, years


def calculate_npv(nbu_rate, annualCostsReduction, yearlyPayments,
                  contractDurationYears, contractDurationDays=0):
    contract_duration = (contractDurationYears * 365 + contractDurationDays)/365.0
    if contract_duration > 15:
        return False
    cf_free = annualCostsReduction
    cf = cf_free - yearlyPayments
    cf_days = cf_free - (yearlyPayments/365)*contractDurationDays
    value = sum([(cf if i <= contract_duration else
                  cf_days if contract_duration < i < contract_duration + 1 else
                  cf_free)
                 / (1 + nbu_rate)**i for i in range(1, NPV_CALCULATION_DURATION + 1)])
    return round(value, 3)

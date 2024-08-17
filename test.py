from tax_information import *

#Testing the TREATMENT of LT and ST CGs
# long_term_capital_gains = -500
# short_term_capital_gains = -2000

# capital_gains_as_ordinary_income = 0
# capital_gains_as_LT = 0
# net_capital_gains = long_term_capital_gains + short_term_capital_gains

# if long_term_capital_gains >= 0 and short_term_capital_gains >= 0:
#     capital_gains_as_LT = long_term_capital_gains
#     capital_gains_as_ordinary_income = short_term_capital_gains
# elif long_term_capital_gains >= 0 and short_term_capital_gains <= 0 and net_capital_gains < 0:
#     capital_gains_as_ordinary_income = max(net_capital_gains, -3000)
# elif long_term_capital_gains >= 0 and short_term_capital_gains <= 0 and net_capital_gains >= 0:
#     capital_gains_as_LT = net_capital_gains
# else:
#     capital_gains_as_ordinary_income = max(net_capital_gains, -3000)

# print("LT Capital Gains:", long_term_capital_gains)
# print("ST Capital Gains:", short_term_capital_gains)
# print("Net Capital Gains:", net_capital_gains)
# print("Taxed as Ordinary Income:", capital_gains_as_ordinary_income)
# print("Taxed as Capital Gains", capital_gains_as_LT)


#Testing LTCGs

# def calculate_capital_gains_tax(filing_status, adjusted_gross_income, capital_gains_as_LT):
#     total_income = adjusted_gross_income + capital_gains_as_LT

#     capital_gains_brackets = capital_gains_tax_brackets.get(filing_status)
    
#     if capital_gains_brackets is None:
#         raise ValueError("Invalid filing status provided.")

#     for CG_income_limit, CG_tax_rate in capital_gains_brackets:
#         if total_income <= CG_income_limit:
#             return capital_gains_as_LT * CG_tax_rate
    
#print(calculate_capital_gains_tax('single', 60000000, 500000))

# def calculate_federal_tax(adjusted_gross_income, filing_status):
#     if adjusted_gross_income < 0:
#         raise ValueError("Adjusted gross income cannot be negative.")
    
#     brackets = federal_tax_brackets.get(filing_status)

#     if brackets is None:
#         raise ValueError("Invalid filing status provided.")
    
#     federal_tax = 0
#     previous_limit = 0

#     # Calculate federal tax AND rate based on the brackets
#     for limit, rate in brackets:
#         if adjusted_gross_income > limit:
#             # Apply tax to the portion within this bracket
#             federal_tax += (limit - previous_limit) * rate
#             previous_limit = limit
#         else:
#             # Apply tax to the remaining income and stop
#             federal_tax += (adjusted_gross_income - previous_limit) * rate
#             break

#     return max(0, federal_tax)

# print(calculate_federal_tax(84632.72,"married_filing_jointly"))

# def calculate_self_employment_tax(other_income):
#     return other_income * self_employment_tax_rate

# print(calculate_self_employment_tax(16520))


from tax_information import federal_tax_brackets, capital_gains_tax_brackets, deductions, self_employment_tax_rate

#2024 standard deduction
def get_standard_deduction(filing_status):
    return deductions.get(filing_status)

#Identify treatment of capital gains income / losses
def capital_gains_treatment(long_term_capital_gains, short_term_capital_gains):
    capital_gains_as_ordinary_income = 0
    capital_gains_as_LT = 0
    net_capital_gains = long_term_capital_gains + short_term_capital_gains

    if long_term_capital_gains >= 0 and short_term_capital_gains >= 0:
        capital_gains_as_LT = long_term_capital_gains
        capital_gains_as_ordinary_income = short_term_capital_gains
    elif long_term_capital_gains >= 0 and short_term_capital_gains <= 0 and net_capital_gains < 0:
        capital_gains_as_ordinary_income = max(net_capital_gains, -3000)
    elif long_term_capital_gains >= 0 and short_term_capital_gains <= 0 and net_capital_gains >= 0:
        capital_gains_as_LT = net_capital_gains
    else:
        capital_gains_as_ordinary_income = max(net_capital_gains, -3000)

    return capital_gains_as_ordinary_income, capital_gains_as_LT

#Calculate the capital gains tax rate on capital gains treated as long-term
def calculate_capital_gains_tax(filing_status, total_taxable_income, capital_gains_as_LT):
    total_income = total_taxable_income + capital_gains_as_LT

    capital_gains_brackets = capital_gains_tax_brackets.get(filing_status)
    
    if capital_gains_brackets is None:
        raise ValueError("Invalid filing status provided.")

    for CG_income_limit, CG_tax_rate in capital_gains_brackets:
        if total_income <= CG_income_limit:
            return capital_gains_as_LT * CG_tax_rate

#Placeholder to include NIIT (Net Income Investment Tax) at some point

def calculate_federal_tax(total_taxable_income, filing_status):
    if total_taxable_income < 0:
        raise ValueError("Adjusted gross income cannot be negative.")
    
    brackets = federal_tax_brackets.get(filing_status)

    if brackets is None:
        raise ValueError("Invalid filing status provided.")
    
    federal_tax = 0
    previous_limit = 0

    # Calculate federal tax AND rate based on the brackets
    for limit, rate in brackets:
        if total_taxable_income > limit:
            # Apply tax to the portion within this bracket
            federal_tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            # Apply tax to the remaining income and stop
            federal_tax += (total_taxable_income - previous_limit) * rate
            break

    return max(0, federal_tax)

def calculate_self_employment_tax(other_income):
    return other_income * self_employment_tax_rate

#SCHEDULE 8812 - "Credits for Qualifying Children and Other Dependents"
def calculate_child_tax_credit_and_other_dependends(num_qualifying_children, num_other_dependents, federal_tax_before_credits, filing_status, adjusted_gross_income):
    if num_qualifying_children < 0 or num_other_dependents < 0:
        raise ValueError("Number of dependents cannot be negative.")
    
    child_tax_credit = 0
    tax_liability_updated_for_child_tax_credit = federal_tax_before_credits

    for _ in range(num_qualifying_children):
        if tax_liability_updated_for_child_tax_credit >= 2000:
            child_tax_credit += 2000
            tax_liability_updated_for_child_tax_credit -= 2000
        elif tax_liability_updated_for_child_tax_credit >= 1700:
            child_tax_credit += tax_liability_updated_for_child_tax_credit
            tax_liability_updated_for_child_tax_credit = 0
        elif tax_liability_updated_for_child_tax_credit > 0:
            child_tax_credit += 1700
            tax_liability_updated_for_child_tax_credit -= tax_liability_updated_for_child_tax_credit
        else:
            child_tax_credit += 1700
    
    child_tax_credit += num_other_dependents * 500

    #Apply the phase out restriction for both child tax credit and other dependents credit
    if filing_status == 'married_filing_jointly':
        phase_out_threshold = 400000
    else:
        phase_out_threshold = 200000

    if adjusted_gross_income > phase_out_threshold:
        phase_out_amount = ((adjusted_gross_income - phase_out_threshold) // 1000) * 50
        child_tax_credit = max(0, child_tax_credit - phase_out_amount)
    
    return child_tax_credit
   
# def calculate_state_tax(total_taxable_income):
#     if total_taxable_income < 0:
#         raise ValueError("Income cannot be negative.")
#     return total_taxable_income * 0.0315

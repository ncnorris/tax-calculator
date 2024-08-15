def get_standard_deduction(filing_status):
    deductions = {
        'single': 12550,
        'married-joint': 25100,
        'married-separate': 12550,
        'head-household': 18800,
        'widow': 25100
    }
    return deductions.get(filing_status, 0)

def calculate_child_tax_credit(ordinary_income, num_qualifying_children, num_other_dependents, filing_status):
    if num_qualifying_children < 0 or num_other_dependents < 0:
        raise ValueError("Number of dependents cannot be negative.")
    
    # Base amounts
    child_tax_credit_per_child = 2000
    refundable_child_tax_credit_per_child = 1700
    other_dependents_credit_per_person = 500

    # Total credits
    total_child_tax_credit = child_tax_credit_per_child * num_qualifying_children
    refundable_child_tax_credit = min(refundable_child_tax_credit_per_child * num_qualifying_children, total_child_tax_credit)
    non_refundable_child_tax_credit = total_child_tax_credit - refundable_child_tax_credit
    total_other_dependents_credit = other_dependents_credit_per_person * num_other_dependents
    
    # Phase-out thresholds
    if filing_status == 'married-joint':
        phase_out_threshold = 400000
    else:
        phase_out_threshold = 200000
    
    if ordinary_income > phase_out_threshold:
        phase_out_amount = ((ordinary_income - phase_out_threshold) // 1000) * 50
        total_child_tax_credit = max(0, total_child_tax_credit - phase_out_amount)
        refundable_child_tax_credit = min(refundable_child_tax_credit, total_child_tax_credit)
        non_refundable_child_tax_credit = total_child_tax_credit - refundable_child_tax_credit
        total_other_dependents_credit = max(0, total_other_dependents_credit - phase_out_amount)
    
    total_credit = total_child_tax_credit + total_other_dependents_credit

    return {
        'total_credit': total_credit,
        'refundable_credit': refundable_child_tax_credit,
        'non_refundable_credit': non_refundable_child_tax_credit + total_other_dependents_credit
    }

def calculate_federal_tax(ordinary_income, short_term_capital_gains, long_term_capital_gains, num_qualifying_children, num_other_dependents, filing_status):
    if ordinary_income < 0:
        raise ValueError("Taxable income cannot be negative.")
    
    # Net short-term and long-term capital gains/losses
    net_capital_gain = short_term_capital_gains + long_term_capital_gains
    
    if net_capital_gain > 0:
        if short_term_capital_gains > 0:
            total_income = ordinary_income + net_capital_gain
        else:
            total_income = ordinary_income
    else:
        total_income = ordinary_income + min(net_capital_gain, -3000)

    # Tax calculation for ordinary income and short-term capital gains (losses)
    tax = 0
    if total_income <= 9875:
        tax += total_income * 0.10
    elif total_income <= 40125:
        tax += 987.5 + (total_income - 9875) * 0.12
    elif total_income <= 85525:
        tax += 4617.5 + (total_income - 40125) * 0.22
    elif total_income <= 163300:
        tax += 14605.5 + (total_income - 85525) * 0.24
    elif total_income <= 207350:
        tax += 33271.5 + (total_income - 163300) * 0.32
    elif total_income <= 518400:
        tax += 47367.5 + (total_income - 207350) * 0.35
    else:
        tax += 156235 + (total_income - 518400) * 0.37

    # Apply long-term capital gain rates if applicable
    if net_capital_gain > 0 and short_term_capital_gains <= 0:
        if net_capital_gain <= 40000:
            tax += net_capital_gain * 0.0
        elif net_capital_gain <= 441450:
            tax += (net_capital_gain - 40000) * 0.15
        else:
            tax += (441450 - 40000) * 0.15 + (net_capital_gain - 441450) * 0.20

    # Calculate the Child Tax Credit
    credits = calculate_child_tax_credit(ordinary_income, num_qualifying_children, num_other_dependents, filing_status)

    # Initialize tracking for refundable and non-refundable credits
    non_refundable_credit_used = 0
    refundable_credit_applied = 0

    for _ in range(num_qualifying_children):
        if tax > 0:
            # Apply the non-refundable portion ($2,000 per child)
            if tax >= 2000:
                tax -= 2000
                non_refundable_credit_used += 2000
            else:
                non_refundable_credit_used += tax
                tax = 0
        else:
            # Apply the refundable portion ($1,700 per child)
            refundable_credit_applied += 1700

    return max(0, tax), refundable_credit_applied

def calculate_state_tax(income):
    if income < 0:
        raise ValueError("Income cannot be negative.")
    return income * 0.05

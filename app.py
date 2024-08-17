from flask import Flask, render_template, request, jsonify
from calculator import capital_gains_treatment, get_standard_deduction, calculate_federal_tax, calculate_capital_gains_tax, calculate_self_employment_tax, calculate_child_tax_credit_and_other_dependends

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    
    def parse_float(value):
        try:
            if value is None or value.strip() == '':
                return 0.0
            return float(value.replace(',', ''))
        except (ValueError, AttributeError):
            return 0.0

    try:
        # Calculate taxable income
        wages = parse_float(data.get('wages', '0'))
        interest = parse_float(data.get('interest', '0'))
        dividends = parse_float(data.get('dividends', '0'))
        short_term_capital_gains = parse_float(data.get('short-term-capital-gains', '0'))
        long_term_capital_gains = parse_float(data.get('long-term-capital-gains', '0'))
        ira_distributions = parse_float(data.get('ira-distributions', '0'))
        pensions_annuities = parse_float(data.get('pensions-annuities', '0'))
        social_security = parse_float(data.get('social-security', '0'))
        other_income = parse_float(data.get('other-income', '0'))

        capital_gains_as_ordinary_income, capital_gains_as_LT = capital_gains_treatment(long_term_capital_gains, short_term_capital_gains)
        
        #Calculate AGI
        adjusted_gross_income = (wages + interest + dividends + ira_distributions +
        pensions_annuities + social_security + other_income + capital_gains_as_ordinary_income)

        # Calculate deductions  
        filing_status = data.get('filing-status', 'single')
        itemized_deduction = parse_float(data.get('itemized_deduction', '0'))
        standard_deduction = get_standard_deduction(filing_status)
        federal_tax_deduction = max(standard_deduction, itemized_deduction)

        # Qualified business income
        qualified_business_income = parse_float(data.get('qualified-business-income', '0'))
        
        # Calculate taxable income
        total_taxable_income = max(0, adjusted_gross_income - federal_tax_deduction - qualified_business_income)
        
        # Calculate federal taxes owed
        federal_tax = (
            calculate_federal_tax(total_taxable_income, filing_status) +
            calculate_capital_gains_tax(filing_status, total_taxable_income, capital_gains_as_LT) +
            calculate_self_employment_tax(other_income)
        )

        #Calculate tax credits
        american_opportunity_tax_credit = parse_float(data.get('american_opportunity_tax_credit', '0'))
        lifetime_learning_credit = parse_float(data.get('lifetime_learning_credit', '0'))
        total_credits = american_opportunity_tax_credit + lifetime_learning_credit
        federal_tax_before_credits = max(0, federal_tax - total_credits)
        num_qualifying_children = int(data.get('num-qualifying-children', 0))
        num_other_dependents = int(data.get('num-other-dependents', 0))
        child_tax_credit = calculate_child_tax_credit_and_other_dependends(num_qualifying_children, num_other_dependents, federal_tax_before_credits, filing_status, adjusted_gross_income)
        federal_tax_after_credits = federal_tax_before_credits - child_tax_credit
        
        #Pull federal tax withheld and tax payments already made
        federal_income_tax_withheld = parse_float(data.get('federal-income-tax-withheld', '0'))
        estimated_tax_payments = parse_float(data.get('estimated-tax-payments', '0'))

        #Calculate total federal tax liability or refund owed
        total_tax_payments = federal_income_tax_withheld + estimated_tax_payments
        tax_liability = max(0, federal_tax_after_credits - total_tax_payments)
        tax_refund = max(0, total_tax_payments - federal_tax_after_credits)

        return jsonify(tax_liability=tax_liability, tax_refund=tax_refund)
    
    except ValueError as e:
        print(f"ValueError occurred: {e}")
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from calculator import get_standard_deduction, calculate_federal_tax, calculate_state_tax

app = Flask(__name__, static_folder='static')

# making this change to see commits

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    
    # Remove commas from numeric values
    def parse_float(value):
        try:
            return float(value.replace(',', ''))
        except (ValueError, AttributeError):
            return 0.0

    try:
        wages = parse_float(data.get('wages'))
        interest = parse_float(data.get('interest'))
        dividends = parse_float(data.get('dividends'))
        short_term_capital_gains = parse_float(data.get('short-term-capital-gains'))
        long_term_capital_gains = parse_float(data.get('long-term-capital-gains'))
        ira_distributions = parse_float(data.get('ira-distributions'))
        pensions_annuities = parse_float(data.get('pensions-annuities'))
        social_security = parse_float(data.get('social-security'))
        other_income = parse_float(data.get('other-income'))
        filing_status = data.get('filing-status', 'single')
        qualified_business_income = parse_float(data.get('qualified-business-income'))
        federal_income_tax_withheld = parse_float(data.get('federal-income-tax-withheld'))
        estimated_tax_payments = parse_float(data.get('estimated-tax-payments'))
        num_qualifying_children = int(data.get('num-qualifying-children', 0))
        num_other_dependents = int(data.get('num-other-dependents', 0))
        
        total_income = (wages + interest + dividends + ira_distributions +
                        pensions_annuities + social_security + other_income)
        standard_deduction = get_standard_deduction(filing_status)
        ordinary_income = max(0, total_income - standard_deduction - qualified_business_income)
        
        # Calculate federal tax
        federal_tax, refundable_child_tax_credit = calculate_federal_tax(
            ordinary_income, short_term_capital_gains, long_term_capital_gains,
            num_qualifying_children, num_other_dependents, filing_status
        )
        state_tax = calculate_state_tax(ordinary_income + short_term_capital_gains + long_term_capital_gains)
        total_tax = federal_tax + state_tax
        total_payments_and_credits = (federal_income_tax_withheld + estimated_tax_payments + refundable_child_tax_credit)
        tax_liability = max(0, total_tax - total_payments_and_credits)
        tax_savings = max(0, total_payments_and_credits - total_tax)
    
        return jsonify(tax_liability=tax_liability, tax_savings=tax_savings)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

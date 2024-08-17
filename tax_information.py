#2024 standard deduction
deductions = {
    'single': 14600,
    'married_filing_jointly': 29200,
    'married_filing_separately': 14600,
    'head_of_household': 21900,
    'widow': 29200
}

#2024 tax brackets
federal_tax_brackets = {
    'single': [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ],
    'married_filing_jointly': [
        (23200, 0.10),
        (94300, 0.12),
        (201050, 0.22),
        (383900, 0.24),
        (487450, 0.32),
        (731200, 0.35),
        (float('inf'), 0.37)
    ],
    'married_filing_separately': [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (365600, 0.35),
        (float('inf'), 0.37)
    ],
    'head_of_household': [
        (16550, 0.10),
        (63100, 0.12),
        (100500, 0.22),
        (191950, 0.24),
        (243700, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ]
}

#2024 capital gains tax brackets
capital_gains_tax_brackets = {
    'single': [
        (47025, 0.00),
        (518900, 0.15),
        (float('inf'), 0.20)
    ],
    'married_filing_jointly': [
        (94050, 0.00),
        (583750, 0.15),
        (float('inf'), 0.20)
    ],
    'married_filing_separately': [
        (47025, 0.00),
        (291850, 0.15),
        (float('inf'), 0.20)
    ],
    'head_of_household': [
        (63000, 0.00),
        (551350, 0.15),
        (float('inf'), 0.20)
    ]
}

#2024 Self-Employement Rate
self_employment_tax_rate = .153
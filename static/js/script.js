// Function to format the number with commas
function formatNumberWithCommas(value) {
    // Remove any non-digit characters except for periods and hyphens
    value = value.replace(/[^0-9.-]/g, '');
    // Add commas as thousand separators
    return value.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Function to handle formatting when input loses focus or changes
function formatNumberInput(event) {
    const input = event.target;
    let value = input.value.replace(/,/g, ''); // Remove existing commas for re-formatting
    if (value) {
        input.value = formatNumberWithCommas(value);
    }
}

// Function to remove commas from input values before submission
function sanitizeInputValues(formData) {
    for (const [key, value] of formData.entries()) {
        formData.set(key, value.replace(/,/g, '')); // Remove commas for form data submission
    }
    return formData;
}

document.getElementById('num-qualifying-children').addEventListener('change', function() {
    const select = document.getElementById('num-qualifying-children');
    const customInput = document.getElementById('custom-qualifying-children');
    customInput.style.display = select.value === 'custom' ? 'block' : 'none';
    if (select.value !== 'custom') {
        customInput.value = '';
    }
});

document.getElementById('num-other-dependents').addEventListener('change', function() {
    const select = document.getElementById('num-other-dependents');
    const customInput = document.getElementById('custom-other-dependents');
    customInput.style.display = select.value === 'custom' ? 'block' : 'none';
    if (select.value !== 'custom') {
        customInput.value = '';
    }
});

document.getElementById('tax-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const sanitizedFormData = sanitizeInputValues(formData);

    const numQualifyingChildren = sanitizedFormData.get('num-qualifying-children');
    if (numQualifyingChildren === 'custom') {
        sanitizedFormData.set('num-qualifying-children', sanitizedFormData.get('custom-qualifying-children') || '0');
    }

    const numOtherDependents = sanitizedFormData.get('num-other-dependents');
    if (numOtherDependents === 'custom') {
        sanitizedFormData.set('num-other-dependents', sanitizedFormData.get('custom-other-dependents') || '0');
    }

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Object.fromEntries(sanitizedFormData.entries())),
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        let resultMessage = '';
        let resultNumber = '';
    
        const formatNumber = (number) => {
            return number.toLocaleString(); // Formats number with commas
        };
    
        if (data.tax_liability && data.tax_liability > 0) {
            resultNumber = `$${formatNumber(Math.round(data.tax_liability))}`;
            resultMessage = `We estimate a tax liability of   <span class="result-number" style="color: maroon;">${resultNumber}</span>`;
        } else if (data.tax_refund && data.tax_refund > 0) {
            resultNumber = `$${formatNumber(Math.round(data.tax_refund))}`;
            resultMessage = `We estimate a tax refund of   <span class="result-number" style="color: #00796b;">${resultNumber}</span>`;
        } else {
            resultMessage = 'We estimate no tax liability or refund.';
        }
    
        resultsDiv.innerHTML = `<p class="result-message" style="color: black;">${resultMessage}</p>`;
    })
    
    .catch(error => console.error('Error:', error));
});

// Add event listeners to all number inputs
document.querySelectorAll('input[type="text"]').forEach(input => {
    input.addEventListener('input', formatNumberInput); // Format as user types
    input.addEventListener('blur', formatNumberInput); // Format on blur
});
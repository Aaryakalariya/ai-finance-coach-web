// income.js - income page interactions
document.addEventListener('DOMContentLoaded', () => {
    const addIncomeForm = document.querySelector('#addIncomeModal form');
    if (addIncomeForm) {
        addIncomeForm.addEventListener('submit', (e) => {
            const amountInput = addIncomeForm.querySelector('[name="amount"]');
            if (amountInput && parseFloat(amountInput.value) <= 0) {
                e.preventDefault();
                alert('Amount must be greater than zero.');
            }
        });
        const dateInput = addIncomeForm.querySelector('[name="date"]');
        if (dateInput && !dateInput.value) {
            dateInput.value = new Date().toISOString().split('T')[0];
        }
    }
});
// expense.js - expense page interactions
document.addEventListener('DOMContentLoaded', () => {
    const addExpenseForm = document.querySelector('#addExpenseModal form');
    if (addExpenseForm) {
        addExpenseForm.addEventListener('submit', (e) => {
            const amountInput = addExpenseForm.querySelector('[name="amount"]');
            if (amountInput && parseFloat(amountInput.value) <= 0) {
                e.preventDefault();
                alert('Amount must be greater than zero.');
            }
        });
    }

    // Auto-fill today's date on the date input if empty
    const dateInput = addExpenseForm && addExpenseForm.querySelector('[name="date"]');
    if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }
});
// budget.js - budget page interactions
document.addEventListener('DOMContentLoaded', () => {
    const addBudgetForm = document.querySelector('#addBudgetModal form');
    if (addBudgetForm) {
        addBudgetForm.addEventListener('submit', (e) => {
            const limitInput = addBudgetForm.querySelector('[name="limit"]');
            if (limitInput && parseFloat(limitInput.value) <= 0) {
                e.preventDefault();
                alert('Budget limit must be greater than zero.');
            }
        });
    }

    // Highlight budgets nearing their limit
    document.querySelectorAll('.progress-bar').forEach((bar) => {
        const width = parseFloat(bar.style.width);
        if (width >= 90) {
            bar.closest('.glass-card')?.classList.add('border', 'border-danger');
        }
    });
});
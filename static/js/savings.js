// savings.js - savings goal page interactions
document.addEventListener('DOMContentLoaded', () => {
    const addGoalForm = document.querySelector('#addGoalModal form');
    if (addGoalForm) {
        addGoalForm.addEventListener('submit', (e) => {
            const targetInput = addGoalForm.querySelector('[name="target_amount"]');
            const dateInput = addGoalForm.querySelector('[name="target_date"]');
            if (targetInput && parseFloat(targetInput.value) <= 0) {
                e.preventDefault();
                alert('Target amount must be greater than zero.');
                return;
            }
            if (dateInput && new Date(dateInput.value) < new Date()) {
                e.preventDefault();
                alert('Target date must be in the future.');
            }
        });
    }
});
// reports.js - report generation page interactions
document.addEventListener('DOMContentLoaded', () => {
    const reportForm = document.querySelector('form[action*="generate_report"], form[action*="generate-report"]');
    if (!reportForm) return;

    reportForm.addEventListener('submit', (e) => {
        const from = reportForm.querySelector('[name="from_date"]');
        const to = reportForm.querySelector('[name="to_date"]');
        if (from && to && from.value && to.value && new Date(from.value) > new Date(to.value)) {
            e.preventDefault();
            alert('"From" date must be before "To" date.');
        }
    });
});
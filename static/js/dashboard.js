// dashboard.js - dashboard-specific interactions
document.addEventListener('DOMContentLoaded', () => {
    const refreshInterval = 5 * 60 * 1000; // 5 minutes

    async function refreshStats() {
        try {
            const res = await fetch('/api/dashboard/stats');
            if (!res.ok) return;
            const data = await res.json();
            const map = {
                total_income: '.stat-value.text-success',
                total_expenses: '.stat-value.text-danger',
                total_savings: '.stat-value.text-primary'
            };
            Object.keys(map).forEach((key) => {
                const el = document.querySelector(map[key]);
                if (el && data[key] !== undefined) {
                    el.textContent = '₹' + Number(data[key]).toFixed(2);
                }
            });
        } catch (err) {
            console.error('Failed to refresh dashboard stats', err);
        }
    }

    if (document.querySelector('.stat-card')) {
        setInterval(refreshStats, refreshInterval);
    }
});
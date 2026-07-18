// charts.js - Chart.js setup for dashboard and analytics pages
document.addEventListener('DOMContentLoaded', () => {
    const chartDefaults = {
        color: getComputedStyle(document.body).getPropertyValue('--text-secondary') || '#6b7280',
        borderColor: '#e5e7eb'
    };

    function makeLineChart(canvasId, labels, data, label) {
        const el = document.getElementById(canvasId);
        if (!el || typeof Chart === 'undefined') return;
        new Chart(el, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    tension: 0.35,
                    fill: true
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    function makePieChart(canvasId, labels, data) {
        const el = document.getElementById(canvasId);
        if (!el || typeof Chart === 'undefined') return;
        new Chart(el, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#4f46e5', '#818cf8', '#16a34a', '#f59e0b', '#dc2626', '#0891b2']
                }]
            },
            options: { plugins: { legend: { position: 'bottom' } } }
        });
    }

    function makeBarChart(canvasId, labels, incomeData, expenseData) {
        const el = document.getElementById(canvasId);
        if (!el || typeof Chart === 'undefined') return;
        new Chart(el, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    { label: 'Income', data: incomeData, backgroundColor: '#16a34a' },
                    { label: 'Expenses', data: expenseData, backgroundColor: '#dc2626' }
                ]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });
    }

    // Dashboard charts (data would be injected via data attributes or a script tag from the template)
    if (document.getElementById('spendingTrendChart')) {
        const trend = window.dashboardData && window.dashboardData.spendingTrend;
        if (trend) {
            makeLineChart('spendingTrendChart', trend.labels, trend.values, 'Spending');
        }
    }
    if (document.getElementById('categoryPieChart')) {
        const cats = window.dashboardData && window.dashboardData.categoryBreakdown;
        if (cats) {
            makePieChart('categoryPieChart', cats.labels, cats.values);
        }
    }

    // Analytics page charts
    if (document.getElementById('incomeExpenseChart') && window.analyticsData) {
        const d = window.analyticsData.incomeExpense;
        if (d && d.labels) {
            makeBarChart('incomeExpenseChart', d.labels, d.income, d.expenses);
        }
    }
    if (document.getElementById('categoryBreakdownChart') && window.analyticsData) {
        const d = window.analyticsData.categoryBreakdown;
        if (d && d.labels) {
            makePieChart('categoryBreakdownChart', d.labels, d.values);
        }
    }
    if (document.getElementById('savingsGrowthChart') && window.analyticsData) {
        const d = window.analyticsData.savingsGrowth;
        if (d && d.labels) {
            makeLineChart('savingsGrowthChart', d.labels, d.values, 'Savings');
        }
    }
});
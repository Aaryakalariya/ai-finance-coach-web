// admin.js - admin panel interactions
document.addEventListener('DOMContentLoaded', () => {
    // Confirm suspend/activate actions
    document.querySelectorAll('form[action*="toggle_user_status"], form[action*="toggle-status"]').forEach((form) => {
        form.addEventListener('submit', (e) => {
            const btnText = form.querySelector('button')?.textContent.trim();
            if (!confirm(`Are you sure you want to ${btnText?.toLowerCase()} this user?`)) {
                e.preventDefault();
            }
        });
    });

    // Maintenance mode warning
    const maintenanceToggle = document.querySelector('[name="maintenance_mode"]');
    if (maintenanceToggle) {
        maintenanceToggle.addEventListener('change', () => {
            if (maintenanceToggle.checked) {
                alert('Enabling maintenance mode will log out all non-admin users.');
            }
        });
    }
});
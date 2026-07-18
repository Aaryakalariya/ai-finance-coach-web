// app.js - global app behaviors: sidebar toggle, password visibility, auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', () => {
    // Sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('appSidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
        document.addEventListener('click', (e) => {
            if (window.innerWidth < 992 &&
                sidebar.classList.contains('show') &&
                !sidebar.contains(e.target) &&
                !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }

    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach((btn) => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (!input) return;
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = isPassword ? 'bi bi-eye-slash' : 'bi bi-eye';
            }
        });
    });

    // Auto-dismiss flash messages after 5 seconds
    document.querySelectorAll('.flash-message').forEach((msg) => {
        setTimeout(() => {
            msg.classList.remove('show');
            msg.addEventListener('transitionend', () => msg.remove());
        }, 5000);
    });
});
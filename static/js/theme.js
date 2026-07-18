// theme.js - handles dark/light mode toggle
(function () {
    const root = document.documentElement;
    const toggleBtn = document.getElementById('themeToggle');
    const STORAGE_KEY = 'afc_theme';

    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
            }
        }
    }

    function getSavedTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch (e) {
            return null;
        }
    }

    function saveTheme(theme) {
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) { /* ignore */ }
    }

    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = getSavedTheme() || (prefersDark ? 'dark' : 'light');
    applyTheme(initialTheme);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const current = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            applyTheme(current);
            saveTheme(current);
        });
    }
})();
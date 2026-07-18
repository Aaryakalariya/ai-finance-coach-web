// validation.js - client-side form validation for auth pages
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.querySelector('form[action*="register"]');
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');
    const strengthBar = document.getElementById('passwordStrength');

    function scorePassword(pwd) {
        let score = 0;
        if (!pwd) return score;
        if (pwd.length >= 8) score++;
        if (/[A-Z]/.test(pwd)) score++;
        if (/[0-9]/.test(pwd)) score++;
        if (/[^A-Za-z0-9]/.test(pwd)) score++;
        return score;
    }

    if (passwordInput && strengthBar) {
        passwordInput.addEventListener('input', () => {
            const score = scorePassword(passwordInput.value);
            const colors = ['#dc2626', '#dc2626', '#f59e0b', '#16a34a', '#16a34a'];
            const widths = ['10%', '25%', '55%', '80%', '100%'];
            strengthBar.style.background = colors[score];
            strengthBar.style.width = widths[score];
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            if (passwordInput && confirmInput && passwordInput.value !== confirmInput.value) {
                e.preventDefault();
                confirmInput.classList.add('is-invalid');
                alert('Passwords do not match.');
            }
        });
    }

    // Simple required-field highlighting for all forms
    document.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', () => {
            form.querySelectorAll('[required]').forEach((field) => {
                if (!field.value) {
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
        });
    });
});
// notifications.js - notification bell & notifications page interactions
document.addEventListener('DOMContentLoaded', () => {
    const markAllForm = document.querySelector('form[action*="mark_all_read"], form[action*="mark-all-read"]');
    if (markAllForm) {
        markAllForm.addEventListener('submit', () => {
            document.querySelectorAll('.notif-unread').forEach((item) => {
                item.classList.remove('notif-unread');
            });
            const badge = document.querySelector('.notif-badge');
            if (badge) badge.remove();
        });
    }

    // Poll for new notification count periodically
    async function pollNotificationCount() {
        try {
            const res = await fetch('/api/notifications/unread-count');
            if (!res.ok) return;
            const data = await res.json();
            const badge = document.querySelector('.notif-badge');
            if (data.count > 0) {
                if (badge) {
                    badge.textContent = data.count;
                } else {
                    const bellBtn = document.querySelector('.btn.position-relative');
                    if (bellBtn) {
                        const span = document.createElement('span');
                        span.className = 'badge rounded-pill bg-danger notif-badge';
                        span.textContent = data.count;
                        bellBtn.appendChild(span);
                    }
                }
            } else if (badge) {
                badge.remove();
            }
        } catch (err) {
            console.error('Failed to poll notifications', err);
        }
    }

    if (document.querySelector('.app-navbar')) {
        setInterval(pollNotificationCount, 60 * 1000);
    }
});
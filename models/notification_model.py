"""
notification_model.py - In-app notification data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class NotificationModel:

    @staticmethod
    def create(user_id: int, title: str, message: str, icon: str = "bi-info-circle") -> int:
        query = """
            INSERT INTO notifications (user_id, title, message, icon)
            VALUES (%s, %s, %s, %s)
        """
        return execute(query, (user_id, title, message, icon))

    @staticmethod
    def get_for_user(user_id: int, limit: int = 50) -> list:
        query = """
            SELECT * FROM notifications WHERE user_id = %s
            ORDER BY created_at DESC LIMIT %s
        """
        return fetch_all(query, (user_id, limit))

    @staticmethod
    def count_unread(user_id: int) -> int:
        row = fetch_one(
            "SELECT COUNT(*) AS total FROM notifications WHERE user_id = %s AND is_read = FALSE",
            (user_id,),
        )
        return row["total"] if row else 0

    @staticmethod
    def mark_all_read(user_id: int) -> None:
        execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", (user_id,))

    @staticmethod
    def mark_read(notification_id: int) -> None:
        execute("UPDATE notifications SET is_read = TRUE WHERE id = %s", (notification_id,))

    @staticmethod
    def broadcast(title: str, message: str, icon: str = "bi-megaphone", user_ids: list = None) -> int:
        """
        Send a notification to multiple users. If user_ids is None, sends to all users.
        Returns the count of notifications created.
        """
        if user_ids is None:
            rows = fetch_all("SELECT id FROM users WHERE status = 'active'")
            user_ids = [r["id"] for r in rows]

        for uid in user_ids:
            NotificationModel.create(uid, title, message, icon)
        return len(user_ids)
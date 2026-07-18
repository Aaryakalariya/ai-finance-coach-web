"""
ai_log_model.py - AI chat message log data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class AiLogModel:

    @staticmethod
    def log_message(user_id: int, sender: str, message: str, tokens_used: int = 0) -> int:
        query = """
            INSERT INTO ai_logs (user_id, sender, message, tokens_used)
            VALUES (%s, %s, %s, %s)
        """
        return execute(query, (user_id, sender, message, tokens_used))

    @staticmethod
    def get_chat_history(user_id: int, limit: int = 50) -> list:
        query = """
            SELECT * FROM ai_logs WHERE user_id = %s
            ORDER BY created_at ASC
            LIMIT %s
        """
        return fetch_all(query, (user_id, limit))

    @staticmethod
    def count_requests_today(user_id: int) -> int:
        query = """
            SELECT COUNT(*) AS total FROM ai_logs
            WHERE user_id = %s AND sender = 'user' AND DATE(created_at) = CURDATE()
        """
        row = fetch_one(query, (user_id,))
        return row["total"] if row else 0

    @staticmethod
    def count_all_requests_today() -> int:
        row = fetch_one(
            "SELECT COUNT(*) AS total FROM ai_logs WHERE sender = 'user' AND DATE(created_at) = CURDATE()"
        )
        return row["total"] if row else 0

    @staticmethod
    def get_all_for_admin(limit: int = 100) -> list:
        query = """
            SELECT al.*, u.full_name AS user_name,
                al.message AS prompt,
                al.message AS response_summary
            FROM ai_logs al
            JOIN users u ON u.id = al.user_id
            WHERE al.sender = 'user'
            ORDER BY al.created_at DESC
            LIMIT %s
        """
        return fetch_all(query, (limit,))
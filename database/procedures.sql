-- procedures.sql - Stored procedures for AI Finance Coach
USE finance_coach;

DELIMITER $$

-- Get monthly summary (income, expenses, savings) for a given user and month
CREATE PROCEDURE IF NOT EXISTS sp_get_monthly_summary(
    IN p_user_id INT,
    IN p_month_year VARCHAR(7)
)
BEGIN
    SELECT
        (SELECT COALESCE(SUM(amount), 0) FROM income
            WHERE user_id = p_user_id AND DATE_FORMAT(date, '%Y-%m') = p_month_year) AS total_income,
        (SELECT COALESCE(SUM(amount), 0) FROM expenses
            WHERE user_id = p_user_id AND DATE_FORMAT(date, '%Y-%m') = p_month_year) AS total_expenses,
        (SELECT COALESCE(SUM(current_amount), 0) FROM savings_goals
            WHERE user_id = p_user_id) AS total_savings;
END$$

-- Get budget utilization per category for a given user and month
CREATE PROCEDURE IF NOT EXISTS sp_get_budget_utilization(
    IN p_user_id INT,
    IN p_month_year VARCHAR(7)
)
BEGIN
    SELECT
        b.id AS budget_id,
        c.name AS category_name,
        b.monthly_limit,
        COALESCE((
            SELECT SUM(e.amount) FROM expenses e
            WHERE e.user_id = p_user_id
              AND e.category_id = b.category_id
              AND DATE_FORMAT(e.date, '%Y-%m') = p_month_year
        ), 0) AS spent
    FROM budgets b
    JOIN categories c ON c.id = b.category_id
    WHERE b.user_id = p_user_id AND b.month_year = p_month_year;
END$$

-- Purge expired, unused OTP codes (run periodically via a scheduled job)
CREATE PROCEDURE IF NOT EXISTS sp_purge_expired_otps()
BEGIN
    DELETE FROM otp_codes WHERE expires_at < NOW() AND used = FALSE;
END$$

DELIMITER ;
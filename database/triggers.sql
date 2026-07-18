-- triggers.sql - Database triggers for AI Finance Coach
USE finance_coach;

DELIMITER $$

-- Automatically create default preferences row when a new user registers
CREATE TRIGGER IF NOT EXISTS trg_create_user_preferences
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_preferences (user_id, email_notifications, budget_alerts, dark_mode)
    VALUES (NEW.id, TRUE, TRUE, FALSE);
END$$

-- Update savings_goals.current_amount whenever a contribution is added
CREATE TRIGGER IF NOT EXISTS trg_update_savings_on_contribution
AFTER INSERT ON savings_contributions
FOR EACH ROW
BEGIN
    UPDATE savings_goals
    SET current_amount = current_amount + NEW.amount
    WHERE id = NEW.goal_id;
END$$

-- Log an activity entry whenever a user's status changes (suspended/activated)
CREATE TRIGGER IF NOT EXISTS trg_log_user_status_change
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status THEN
        INSERT INTO activity_logs (user_id, action, ip_address)
        VALUES (NEW.id, CONCAT('Account status changed from ', OLD.status, ' to ', NEW.status), NULL);
    END IF;
END$$

DELIMITER ;
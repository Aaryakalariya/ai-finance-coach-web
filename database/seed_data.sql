-- seed_data.sql - Default categories, platform settings, and a demo admin account
USE finance_coach;

INSERT INTO categories (name, icon, type, is_default) VALUES
('Groceries', 'bi-cart', 'expense', TRUE),
('Rent', 'bi-house-door', 'expense', TRUE),
('Utilities', 'bi-lightning-charge', 'expense', TRUE),
('Transportation', 'bi-car-front', 'expense', TRUE),
('Dining Out', 'bi-cup-straw', 'expense', TRUE),
('Entertainment', 'bi-film', 'expense', TRUE),
('Healthcare', 'bi-heart-pulse', 'expense', TRUE),
('Shopping', 'bi-bag', 'expense', TRUE),
('Education', 'bi-book', 'expense', TRUE),
('Insurance', 'bi-shield-check', 'expense', TRUE),
('Other Expense', 'bi-three-dots', 'expense', TRUE),
('Salary', 'bi-cash-coin', 'income', TRUE),
('Freelance', 'bi-laptop', 'income', TRUE),
('Investments', 'bi-graph-up-arrow', 'income', TRUE),
('Gifts', 'bi-gift', 'income', TRUE),
('Other Income', 'bi-three-dots', 'income', TRUE);

INSERT INTO platform_settings (id, platform_name, support_email, maintenance_mode, allow_registrations, ai_daily_limit, ai_model)
VALUES (1, 'AI Finance Coach', 'support@aifinancecoach.com', FALSE, TRUE, 20, 'gemini-pro')
ON DUPLICATE KEY UPDATE platform_name = VALUES(platform_name);

-- Demo super admin account (password: ChangeMe123! -- hash generated with werkzeug.security)
-- IMPORTANT: change this password immediately after first login in a real deployment.
INSERT INTO admins (full_name, email, password_hash, role) VALUES
('System Administrator', 'admin@aifinancecoach.com',
 'pbkdf2:sha256:600000$REPLACE_WITH_REAL_HASH$0000000000000000000000000000000000000000000000000000000000000000',
 'super_admin');
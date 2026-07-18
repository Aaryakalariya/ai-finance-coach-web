-- finance_coach.sql - Master database file for AI Finance Coach
-- Run this single file to set up the entire database from scratch, OR
-- run schema.sql, seed_data.sql, triggers.sql, procedures.sql separately in that order.
--
-- Usage:
--   mysql -u root -p < database/finance_coach.sql

SOURCE schema.sql;
SOURCE triggers.sql;
SOURCE procedures.sql;
SOURCE seed_data.sql;
-- Add user_id and type to emergencies
ALTER TABLE emergencies ADD COLUMN IF NOT EXISTS user_id INT;
ALTER TABLE emergencies ADD COLUMN IF NOT EXISTS emergency_type ENUM('Accident', 'Medical', 'Cardiac', 'Trauma', 'Other') DEFAULT 'Other';
ALTER TABLE emergencies ADD FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE users MODIFY COLUMN role ENUM('admin', 'hospital_admin', 'driver', 'user') NOT NULL DEFAULT 'user';
ALTER TABLE users ADD COLUMN otp_code VARCHAR(6);
ALTER TABLE users ADD COLUMN otp_expiry TIMESTAMP NULL;

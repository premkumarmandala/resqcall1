-- Database Schema for Emergency Rescue & Hospital Management System

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'hospital_admin', 'driver') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address TEXT NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    total_beds INT DEFAULT 0,
    icu_beds INT DEFAULT 0,
    oxygen_status ENUM('Available', 'Low', 'Critical') DEFAULT 'Available',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ambulances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) UNIQUE NOT NULL,
    driver_user_id INT,
    status ENUM('Available', 'On Duty', 'Offline', 'Maintenance') DEFAULT 'Offline',
    current_lat DECIMAL(10, 8),
    current_lng DECIMAL(11, 8),
    FOREIGN KEY (driver_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS emergencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    contact_number VARCHAR(20),
    location_address TEXT NOT NULL,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    severity ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    status ENUM('Pending', 'Assigned', 'Resolved', 'Cancelled') DEFAULT 'Pending',
    assigned_ambulance_id INT,
    assigned_hospital_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (assigned_ambulance_id) REFERENCES ambulances(id),
    FOREIGN KEY (assigned_hospital_id) REFERENCES hospitals(id)
);

CREATE TABLE IF NOT EXISTS emergency_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emergency_id INT NOT NULL,
    action_text VARCHAR(255) NOT NULL,
    performed_by_user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (emergency_id) REFERENCES emergencies(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by_user_id) REFERENCES users(id)
);

-- Sample Data

-- Users (Password: password123)
INSERT INTO users (name, email, phone, password_hash, role) VALUES 
('System Admin', 'admin@resq.com', '1234567890', '$2b$12$OzQjujWnmwTISxE/ekZ0wO4YyFplyGvuko8ka5MgmteAmUxny.oIe', 'admin'),
('City General Admin', 'city_gen@resq.com', '0987654321', '$2b$12$OzQjujWnmwTISxE/ekZ0wO4YyFplyGvuko8ka5MgmteAmUxny.oIe', 'hospital_admin'),
('John Driver', 'john@resq.com', '1122334455', '$2b$12$OzQjujWnmwTISxE/ekZ0wO4YyFplyGvuko8ka5MgmteAmUxny.oIe', 'driver');

-- Hospitals
INSERT INTO hospitals (name, address, contact_phone, total_beds, icu_beds, oxygen_status) VALUES
('City General Hospital', '123 Main St, Downtown', '555-0101', 150, 20, 'Available'),
('Westside Trauma Center', '456 West Ave', '555-0102', 80, 10, 'Low');

-- Ambulances
INSERT INTO ambulances (vehicle_number, driver_user_id, status) VALUES
('XZ-9900', 3, 'Available'),
('XZ-8800', NULL, 'Offline');

-- Emergencies
INSERT INTO emergencies (patient_name, contact_number, location_address, severity, status, assigned_hospital_id) VALUES
('Jane Doe', '9988776655', 'Corner of 5th and Elm', 'Critical', 'Pending', NULL),
('Bob Smith', '8877665544', 'Highway 101, mile marker 45', 'High', 'Assigned', 1);

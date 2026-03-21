from flask import Flask
from backend.db import mysql
from backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql.init_app(app)

with app.app_context():
    cursor = mysql.connection.cursor()
    
    new_columns = [
        ("reg_number", "VARCHAR(100)"),
        ("hospital_type", "ENUM('Government', 'Private', 'Trust', 'Corporate')"),
        ("city", "VARCHAR(100)"),
        ("district", "VARCHAR(100)"),
        ("state", "VARCHAR(100)"),
        ("pin_code", "VARCHAR(20)"),
        ("alternate_phone", "VARCHAR(20)"),
        ("official_email", "VARCHAR(100)"),
        ("available_beds", "INT DEFAULT 0"),
        ("available_icu_beds", "INT DEFAULT 0"),
        ("ventilators_count", "INT DEFAULT 0"),
        ("has_emergency", "BOOLEAN DEFAULT FALSE"),
        ("has_trauma", "BOOLEAN DEFAULT FALSE"),
        ("has_cardiac", "BOOLEAN DEFAULT FALSE"),
        ("has_burn", "BOOLEAN DEFAULT FALSE"),
        ("has_blood_bank", "BOOLEAN DEFAULT FALSE"),
        ("has_ambulance", "BOOLEAN DEFAULT FALSE"),
        ("ambulance_count", "INT DEFAULT 0"),
        ("doctors_on_duty", "INT DEFAULT 0"),
        ("nurses_on_duty", "INT DEFAULT 0"),
        ("is_24_7", "BOOLEAN DEFAULT TRUE"),
        ("working_hours", "VARCHAR(100)"),
        ("status", "ENUM('Active', 'Inactive', 'Temporarily Full') DEFAULT 'Active'"),
        ("medicine_readiness", "JSON")
    ]
    
    # Get current columns
    cursor.execute("DESCRIBE hospitals")
    existing_cols = [row['Field'] for row in cursor.fetchall()]
    
    for col_name, col_type in new_columns:
        if col_name not in existing_cols:
            print(f"Adding column {col_name}...")
            cursor.execute(f"ALTER TABLE hospitals ADD COLUMN {col_name} {col_type}")
    
    # Modify existing oxygen_status if it exists
    if 'oxygen_status' in existing_cols:
         print("Updating oxygen_status ENUM...")
         cursor.execute("ALTER TABLE hospitals MODIFY COLUMN oxygen_status ENUM('Available', 'Limited', 'Not Available', 'Low', 'Critical') DEFAULT 'Available'")

    # Ensure lat/long exist (might have been missing in some turns)
    if 'latitude' not in existing_cols:
        cursor.execute("ALTER TABLE hospitals ADD COLUMN latitude DECIMAL(10, 8)")
    if 'longitude' not in existing_cols:
        cursor.execute("ALTER TABLE hospitals ADD COLUMN longitude DECIMAL(11, 8)")

    mysql.connection.commit()
    cursor.close()
    print("Hospital table schema updated successfully.")

from flask import Flask
from backend.db import mysql
from backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql.init_app(app)

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("DESCRIBE emergencies")
    columns = [row['Field'] for row in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id column...")
        cursor.execute("ALTER TABLE emergencies ADD COLUMN user_id INT")
        cursor.execute("ALTER TABLE emergencies ADD FOREIGN KEY (user_id) REFERENCES users(id)")
    
    if 'emergency_type' not in columns:
        print("Adding emergency_type column...")
        cursor.execute("ALTER TABLE emergencies ADD COLUMN emergency_type ENUM('Accident', 'Medical', 'Cardiac', 'Trauma', 'Other') DEFAULT 'Other'")
    
    mysql.connection.commit()
    cursor.close()
    print("Emergencies table updated.")

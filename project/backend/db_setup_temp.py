from flask import Flask
from backend.config import Config
from backend.db import mysql
import sys

def init_db():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    
    with app.app_context():
        try:
            print("Creating call_logs table...")
            cur = mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS call_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NULL,
                    call_sid VARCHAR(255) NOT NULL,
                    status VARCHAR(50) DEFAULT 'queued',
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME NULL,
                    duration INT DEFAULT 0,
                    recording_url VARCHAR(512) NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB;
            """)
            mysql.connection.commit()
            print("Table created successfully!")
            cur.close()
        except Exception as e:
            print(f"Error creating table: {e}")

if __name__ == '__main__':
    init_db()

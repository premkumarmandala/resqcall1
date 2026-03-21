import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-dev'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root' # Update if needed
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Jesus143' # Update if needed
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'resq_db'
    MYSQL_CURSORCLASS = 'DictCursor' 
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Email Settings (Update these to send real emails)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@gmail.com'  # REPLACE THIS
    MAIL_PASSWORD = 'your-app-password'     # REPLACE THIS

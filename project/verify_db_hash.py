import bcrypt
from backend.app import create_app
from backend.db import mysql

app = create_app()
with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email='admin@resq.com'")
    row = cursor.fetchone()
    if row:
        stored_hash = row['password_hash']
        password = 'password123'
        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print("SUCCESS: Password matches hash in DB")
            else:
                print("FAILURE: Password does NOT match hash in DB")
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print("ERROR: Admin user not found in DB")

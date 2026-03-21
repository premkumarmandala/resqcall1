import bcrypt
from backend.app import create_app
from backend.db import mysql

app = create_app()
password = 'password123'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET password_hash=%s WHERE email='admin@resq.com'", (hashed.decode('utf-8'),))
    mysql.connection.commit()
    cursor.close()
    print(f"Successfully updated admin@resq.com with hash: {hashed.decode('utf-8')}")

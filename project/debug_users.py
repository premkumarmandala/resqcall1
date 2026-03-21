from backend.db import mysql
from backend.app import app

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()
    for u in users:
        print(u)

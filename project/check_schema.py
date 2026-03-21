from backend.db import mysql
from backend.app import app

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("DESCRIBE hospitals")
    columns = cursor.fetchall()
    for col in columns:
        print(f"{col['Field']}: {col['Type']}")

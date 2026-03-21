from backend.app import app
from backend.db import mysql

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("DESC hospitals")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns in hospitals table:")
    print(columns)
    cursor.close()

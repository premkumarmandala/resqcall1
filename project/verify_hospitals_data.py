import pymysql
import os

from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB', 'resq_db'),
    'cursorclass': pymysql.cursors.DictCursor
}

try:
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        print("--- Checking Columns ---")
        cursor.execute("DESC hospitals")
        rows = cursor.fetchall()
        cols = [r['Field'] for r in rows]
        print(f"Columns: {cols}")
        
        if 'latitude' in cols and 'longitude' in cols:
            print("✅ Latitude/Longitude columns exist.")
        else:
            print("❌ MISSING Latitude/Longitude columns.")

        print("\n--- Checking Data ---")
        cursor.execute("SELECT name, latitude, longitude FROM hospitals LIMIT 5")
        hospitals = cursor.fetchall()
        for h in hospitals:
            print(h)
        
        cursor.execute("SELECT COUNT(*) as count FROM hospitals")
        count = cursor.fetchone()['count']
        print(f"\nTotal Hospitals: {count}")

    connection.close()

except Exception as e:
    print(f"Error: {e}")

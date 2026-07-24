import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('MYSQL_HOST', 'localhost')
port = int(os.getenv('MYSQL_PORT', 3306))
user = os.getenv('MYSQL_USER', 'root')
password = os.getenv('MYSQL_PASSWORD', '')
db = os.getenv('MYSQL_DB', 'defaultdb')

print(f"Connecting to {host}:{port}...")

connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=db,
    cursorclass=pymysql.cursors.DictCursor
)

sql_files = [
    'database/update_hospital_schema.sql',
    'database/update_otp.sql',
    'database/update_emergencies_user.sql',
    'database/update_hospital_full_details.sql'
]

with connection:
    with connection.cursor() as cursor:
        for f in sql_files:
            print(f"Running {f}...")
            if not os.path.exists(f): continue
            with open(f, 'r') as file:
                content = file.read()
                # Remove IF NOT EXISTS for ADD COLUMN, which often fails in MySQL
                content = content.replace("ADD COLUMN IF NOT EXISTS", "ADD COLUMN")
                statements = content.split(';')
                for stmt in statements:
                    stmt = stmt.strip()
                    if stmt:
                        try:
                            cursor.execute(stmt)
                        except pymysql.err.OperationalError as e:
                            if getattr(e, 'args', [0])[0] == 1060:
                                pass # Column already exists
                            else:
                                print(f"Error: {e}")
                        except Exception as e:
                            print(f"Error: {e}")
    connection.commit()
print("Updates done!")

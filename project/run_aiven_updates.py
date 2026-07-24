import os
import pymysql

# Hardcoded Aiven DB credentials
host = 'mysql-5e2f1d3-premkumarmandala123-60de.b.aivencloud.com'
port = 14962
user = 'avnadmin'
password = 'AVNS_atDQUv-7b_APooFrmLV'
db = 'defaultdb'

print(f"Connecting to Aiven Cloud at {host}:{port}...")

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
            print(f"Running {f} on AIVEN...")
            if not os.path.exists(f): continue
            with open(f, 'r') as file:
                content = file.read()
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
print("Cloud Database Updates Done!")

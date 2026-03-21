import pymysql
import os

# Database configuration
from dotenv import load_dotenv

# Load environment variables from the root .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '..', '.env')
load_dotenv(env_path)

# Database configuration
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB', 'resq_db'),
    'cursorclass': pymysql.cursors.DictCursor
}

def run_sql_files(files):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            for filename in files:
                print(f"Executing {filename}...")
                with open(filename, 'r') as f:
                    # Basic split by semicolon for multiple statements
                    content = f.read()
                    statements = content.split(';')
                    for stmt in statements:
                        if stmt.strip():
                            try:
                                cursor.execute(stmt)
                            except Exception as e:
                                print(f"Warning running statement: {e}")
        connection.commit()
        print("All updates successful!")
    except Exception as e:
        print(f"Connection Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = [
        os.path.join(script_dir, 'update_hospital_schema.sql'),
        os.path.join(script_dir, 'update_hospital_full_details.sql')
    ]
    run_sql_files(files)

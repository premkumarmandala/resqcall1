import os
import pymysql

def init_db():
    from dotenv import load_dotenv
    load_dotenv()
    
    host = os.getenv('MYSQL_HOST')
    port = int(os.getenv('MYSQL_PORT', 3306))
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    db = os.getenv('MYSQL_DB')
    
    print(f"Connecting to {host}:{port}...")
    
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with connection:
        with connection.cursor() as cursor:
            with open('database/schema.sql', 'r') as f:
                schema_sql = f.read()
                
            statements = schema_sql.split(';')
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        print("Executed a statement.")
                    except Exception as e:
                        print(f"Error executing statement: {e}")
                        
        connection.commit()
    print("Database schema loaded successfully.")

if __name__ == '__main__':
    init_db()

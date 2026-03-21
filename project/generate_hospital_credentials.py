import pymysql
import os
import bcrypt
import re
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB', 'resq_db'),
    'cursorclass': pymysql.cursors.DictCursor
}

OUTPUT_FILE = "HOSPITAL_CREDENTIALS.txt"
DEFAULT_PASS = "ResQ@123"

def generate_credentials():
    try:
        connection = pymysql.connect(**db_config)
        print("Connected to database.")
        
        # Generate Hash
        hashed = bcrypt.hashpw(DEFAULT_PASS.encode('utf-8'), bcrypt.gensalt())
        
        credentials_list = []
        
        with connection.cursor() as cursor:
            # 1. Fetch all hospitals
            cursor.execute("SELECT id, name FROM hospitals")
            hospitals = cursor.fetchall()
            
            print(f"Found {len(hospitals)} hospitals. Generating accounts...")
            
            for h in hospitals:
                # Generate clean slug for email
                slug = re.sub(r'[^a-zA-Z0-9]', '', h['name'].lower())
                email = f"admin@{slug}.com"
                phone = f"9{str(h['id']).zfill(9)}" # Dummy unique phone
                
                # 2. Check if user already exists (by email) to avoid duplicates
                cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
                existing = cursor.fetchone()
                
                user_id = None
                
                if existing:
                    user_id = existing['id']
                    # Optional: Reset password to ensure we know it
                    cursor.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hashed, user_id))
                else:
                    # Create new user
                    cursor.execute("""
                        INSERT INTO users (name, email, phone, password_hash, role)
                        VALUES (%s, %s, %s, %s, 'hospital_admin')
                    """, (h['name'] + " Admin", email, phone, hashed))
                    user_id = cursor.lastrowid
                
                # 3. Link Hospital to User
                # Check if 'admin_user_id' column exists first? Assuming schema is consistent with previous tasks.
                # If column might not exist, we'll error. Assuming it exists based on routes/hospitals.py usage.
                try:
                    cursor.execute("UPDATE hospitals SET admin_user_id=%s WHERE id=%s", (user_id, h['id']))
                except Exception as link_err:
                    print(f"Warning: Could not link user to hospital {h['name']}. Column admin_user_id might be missing? Error: {link_err}")
                
                credentials_list.append(f"Hospital: {h['name']}\nURL: http://localhost:8080/hospital_login.html\nEmail: {email}\nPassword: {DEFAULT_PASS}\n-----------------------------------\n")

            connection.commit()
            
        # Write to file
        with open(OUTPUT_FILE, 'w') as f:
            f.write("RESQ APPLICATION - HOSPITAL LOGIN CREDENTIALS\n")
            f.write("=============================================\n\n")
            f.writelines(credentials_list)
            
        print(f"Successfully generated credentials for {len(hospitals)} hospitals.")
        print(f"Saved to {os.path.abspath(OUTPUT_FILE)}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    generate_credentials()

import pymysql
import os
import random
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

def randomize_hospitals():
    try:
        connection = pymysql.connect(**db_config)
        print("Connected to database.")
        
        with connection.cursor() as cursor:
            # Fetch all hospitals
            cursor.execute("SELECT id, total_beds, icu_beds FROM hospitals")
            hospitals = cursor.fetchall()
            
            print(f"Found {len(hospitals)} hospitals. Updating with random data...")
            
            for h in hospitals:
                # Logic:
                # If total_beds is 0, assign a random total between 50 and 500
                total = h['total_beds']
                if total == 0:
                    total = random.randint(50, 500)
                
                # Randomize available beds (0 to total)
                # Skew towards having some availability usually
                avail = random.randint(int(total * 0.1), int(total * 0.9))
                
                # ICU Beds
                total_icu = h['icu_beds']
                if total_icu == 0:
                    total_icu = random.randint(5, 50)
                avail_icu = random.randint(0, total_icu)
                
                # Oxygen Status (Weighted)
                # 70% Available, 20% Low, 10% Critical
                oxy_stat = random.choices(['Available', 'Low', 'Critical'], weights=[70, 20, 10], k=1)[0]
                
                # Staffing
                docs = random.randint(2, 20)
                nurses = random.randint(5, 50)
                amb_count = random.randint(1, 10)
                
                # Update Query
                update_query = """
                    UPDATE hospitals 
                    SET 
                        total_beds = %s,
                        available_beds = %s,
                        icu_beds = %s,
                        available_icu_beds = %s,
                        oxygen_status = %s,
                        doctors_on_duty = %s,
                        nurses_on_duty = %s,
                        ambulance_count = %s
                    WHERE id = %s
                """
                cursor.execute(update_query, (
                    total, avail, total_icu, avail_icu, oxy_stat, docs, nurses, amb_count, h['id']
                ))
                
            connection.commit()
            print("Successfully randomized hospital data.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    randomize_hospitals()

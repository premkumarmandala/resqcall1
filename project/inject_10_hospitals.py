import pymysql
import os
import random
import math
from dotenv import load_dotenv

load_dotenv()

# Center locations corresponding to user external IP loc (India center approximately/Hyderabad)
center_lat_deg = 17.3840
center_lng_deg = 78.4564

# DB Config
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB', 'resq_db'),
}

def get_random_coord(c_lat, c_lng, min_km, max_km):
    r_earth = 6371.0
    # Random distance between min_km and max_km
    r = random.uniform(min_km, max_km)
    # Random angle in radians
    theta = random.uniform(0, 2 * math.pi)
    
    # Offsets in radians
    dy = r * math.cos(theta)
    dx = r * math.sin(theta)
    
    new_lat = c_lat + (dy / r_earth) * (180 / math.pi)
    new_lng = c_lng + (dx / r_earth) * (180 / math.pi) / math.cos(c_lat * math.pi/180)
    
    return new_lat, new_lng

hospitals_50km = [
    "Apollo Health City",
    "KIMS Hospitals Secunderabad",
    "Yashoda Hospitals Somajiguda",
    "CARE Hospitals Banjara Hills",
    "AIG Hospitals Gachibowli",
]

hospitals_100km = [
    "District General Hospital Sangareddy",
    "Mamata General Hospital",
    "SVS Medical College Hospital",
    "Kamineni Hospitals Narketpally",
    "Medicover Hospitals Nizamabad"
]

def inject():
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cur:
            all_hospitals = [(n, 5.0, 48.0) for n in hospitals_50km] + [(n, 52.0, 98.0) for n in hospitals_100km]
            
            for (name, min_km, max_km) in all_hospitals:
                lat, lng = get_random_coord(center_lat_deg, center_lng_deg, min_km, max_km)
                
                total_beds = random.randint(100, 600)
                avail_beds = random.randint(10, int(total_beds*0.8))
                icu_beds = int(total_beds * 0.15)
                avail_icu = random.randint(2, icu_beds)
                phone = f"98765{random.randint(10000, 99999)}"
                email = f"{name.split()[0].lower().replace(' ', '')}@example.com"
                
                cur.execute("""
                    INSERT INTO hospitals 
                    (name, address, contact_phone, latitude, longitude,
                     total_beds, available_beds, icu_beds, available_icu_beds,
                     oxygen_status, has_emergency, has_trauma, has_cardiac,
                     status, official_email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    name,
                    f"Main Road, Near {lat:.2f}, {lng:.2f}",
                    phone,
                    lat,
                    lng,
                    total_beds,
                    avail_beds,
                    icu_beds,
                    avail_icu,
                    'Available',
                    1, 1, 1,
                    'Active',
                    email
                ))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    inject()
    print("Successfully added 10 hospitals.")

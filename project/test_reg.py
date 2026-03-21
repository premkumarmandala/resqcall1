import requests
import json

data = {
    "admin_name": "Test Admin",
    "email": f"test_{int(__import__('time').time())}@hospital.com",
    "admin_phone": "1234567890",
    "password": "password123",
    "hospital_name": "Debug Hospital",
    "reg_number": "REG123",
    "hospital_type": "Private",
    "hospital_phone": "0987654321",
    "address": "123 Test St",
    "city": "Test City",
    "state": "TS",
    "pin_code": "500001",
    "latitude": 17.3850,
    "longitude": 78.4867,
    "total_beds": 100,
    "icu_beds": 20,
    "available_beds": 100,
    "available_icu_beds": 20,
    "ventilators_count": 5,
    "oxygen_status": "Available",
    "doctors_on_duty": 10,
    "nurses_on_duty": 20,
    "is_24_7": True,
    "has_emergency": True,
    "has_trauma": True,
    "has_cardiac": False,
    "has_burn": False,
    "has_blood_bank": True,
    "has_ambulance": True,
    "ambulance_count": 2,
    "medicine_readiness": {"pain_mgt": "Available"}
}

res = requests.post('http://127.0.0.1:5000/hospitals/register', json=data)
print(f"Status: {res.status_code}")
print(f"Response: {res.text}")

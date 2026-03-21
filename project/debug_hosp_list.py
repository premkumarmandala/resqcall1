import jwt
import datetime
import requests
from backend.config import Config

# Generate token for admin
token = jwt.encode({
    'user_id': 1,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
}, Config.SECRET_KEY, algorithm="HS256")

headers = {'Authorization': f'Bearer {token}'}
try:
    res = requests.get('http://127.0.0.1:5000/hospitals/', headers=headers)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"Count: {len(data)}")
        if len(data) > 0:
            print(f"First Hospital: {data[0]['name']}")
    else:
        print(f"Body: {res.text}")
except Exception as e:
    print(f"Error: {e}")

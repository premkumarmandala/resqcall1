import requests

try:
    # Try to login first to get a token
    # But I don't know the password.
    # I'll just try to hit the endpoint with NO token to see if at least I get a 401.
    # If I get 401, the server is UP.
    res = requests.get('http://127.0.0.1:5000/hospitals/')
    print(f"Status: {res.status_code}")
    print(f"Body: {res.text}")
except Exception as e:
    print(f"Error: {e}")

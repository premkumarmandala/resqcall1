import requests

url = "http://localhost:5000/api/ai/analyze"
payload = {
    "symptoms": "chest pain",
    "latitude": None,
    "longitude": None
}
# Assuming we can mock current_user via a test token or just mock the logic.
# Wait, @token_required needs an Auth header.
# Let's bypass the API and just print round(float('inf'), 2)
try:
    x = round(float('inf'), 2)
except Exception as e:
    print(f"Exception: {type(e).__name__} - {e}")

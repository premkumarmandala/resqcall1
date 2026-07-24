from flask import Flask, jsonify
app = Flask(__name__)
with app.app_context():
    try:
        print(jsonify({'val': float('inf')}).get_data(as_text=True))
    except Exception as e:
        print(f"Exception: {e}")

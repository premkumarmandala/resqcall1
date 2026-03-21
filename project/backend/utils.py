from functools import wraps
from flask import request, jsonify, current_app
import jwt
from backend.db import mysql

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Bearer <token>
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Verify user exists
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
            current_user = cursor.fetchone()
            cursor.close()
            
            if not current_user:
                 return jsonify({'message': 'User invalid!'}), 401
                 
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin privilege required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def send_sms_simulation(phone_number, message):
    """
    Simulates sending an SMS. In a real app, this would use Twilio or SNS.
    returns True if 'sent', False if failed.
    """
    print(f"\\n--- SMS SIMULATION ---")
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print(f"----------------------\\n")
    return True

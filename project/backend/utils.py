from functools import wraps
from flask import request, jsonify, current_app
import jwt
import os
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
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

def token_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = {'id': None, 'name': 'Emergency Guest', 'phone': 'Guest', 'role': 'guest'}
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if token and token != 'null' and token != 'undefined':
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    current_user = user
            except Exception:
                pass
            
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

def send_email_otp(to_email, otp):
    try:
        sender_email = os.environ.get('SMTP_EMAIL')
        sender_password = os.environ.get('SMTP_PASSWORD')
        
        if not sender_email or not sender_password:
            print("SMTP credentials missing. Cannot send email.")
            return False

        msg = MIMEText(f"Your ResQ-call verification code is: {otp}")
        msg['Subject'] = 'ResQ-call Verification Code'
        msg['From'] = sender_email
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email OTP: {e}")
        return False

def send_sms_otp(phone_number, otp):
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_number = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_number]):
            print("Twilio credentials missing. Cannot send SMS.")
            return False

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your ResQ-call verification code is: {otp}",
            from_=twilio_number,
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS OTP: {e}")
        return False

from flask import Blueprint, request, jsonify, current_app
from backend.db import mysql
import jwt
import datetime
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # In a real restricted system, this might be admin-only or have approval.
    # We will allow open registration for demo purposes, or maybe only for 'driver'/'hospital_staff' if we want.
    # The prompt says Admin creates users, maybe this endpoint is used by Admin? 
    # Or self-registration. We will assume self-registration for now or check args.
    
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role', 'driver') # default to driver

    if not all([name, email, phone, password]):
        return jsonify({'message': 'Missing fields'}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, phone, hashed_pw, role))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500
    finally:
        cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Can accept email or phone
    identifier = data.get('email_or_phone')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'message': 'Missing login details'}), 400

    cursor = mysql.connection.cursor()
    # Check email OR phone
    cursor.execute("SELECT * FROM users WHERE email = %s OR phone = %s", (identifier, identifier))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    if not user.get('is_active', True):
        return jsonify({'message': 'Account is disabled'}), 403

    # Verify password (stored as bytes in DB usually, but we stored string?)
    # If stored as string in DB for `password_hash`, we need to encode it to check.
    # The sample data has a bcrypt string.
    
    stored_hash = user['password_hash']
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
        
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        token = jwt.encode({
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    identifier = data.get('identifier')
    if not identifier: return jsonify({'message': 'Phone or Email required'}), 400
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s OR phone=%s", (identifier, identifier))
    user = cursor.fetchone()
    
    import random
    otp = str(random.randint(1000, 9999))
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    
    if not user:
        email = identifier if '@' in identifier else f"{identifier}@temp.com"
        phone = identifier if '@' not in identifier else '0000000000'
        hashed = bcrypt.hashpw(otp.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute("INSERT INTO users (name, email, phone, password_hash, role, otp_code, otp_expiry) VALUES ('Guest User', %s, %s, %s, 'user', %s, %s)", (email, phone, hashed, otp, expiry))
        mysql.connection.commit()
    else:
        cursor.execute("UPDATE users SET otp_code=%s, otp_expiry=%s WHERE id=%s", (otp, expiry, user['id']))
        mysql.connection.commit()
    
    cursor.close()
    return jsonify({'message': 'OTP Sent', 'debug_otp': otp})

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    identifier = data.get('identifier')
    otp = data.get('otp')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s OR phone=%s", (identifier, identifier))
    user = cursor.fetchone()
    cursor.close()
    
    if not user: return jsonify({'message': 'User not found'}), 404
    
    if user['otp_code'] == otp:
        if user['otp_expiry'] and user['otp_expiry'] > datetime.datetime.utcnow():
            token = jwt.encode({
                'user_id': user['id'],
                'role': user['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
            
            return jsonify({
                'token': token,
                'user': {'id': user['id'], 'name': user['name'], 'role': user['role'], 'phone': user['phone']}
            })
        return jsonify({'message': 'OTP Expired'}), 400
        
    return jsonify({'message': 'Invalid OTP'}), 401

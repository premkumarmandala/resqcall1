from flask import Blueprint, request, jsonify
from backend.db import mysql
from backend.utils import token_required, admin_required
import bcrypt

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, name, email, phone, role, is_active, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@users_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_user(current_user):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role')
    
    if not all([name, email, password, role]):
        return jsonify({'message': 'Missing data'}), 400
        
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, phone, hashed, role))
        mysql.connection.commit()
    except Exception as e:
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500
    finally:
        cursor.close()
        
    return jsonify({'message': 'User created'}), 201

@users_bp.route('/<int:id>/status', methods=['PUT'])
@token_required
@admin_required
def toggle_user_status(current_user, id):
    data = request.get_json()
    active = data.get('is_active')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET is_active=%s WHERE id=%s", (active, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User status updated'})

@users_bp.route('/<int:id>/password', methods=['PUT'])
@token_required
@admin_required
def reset_password(current_user, id):
    data = request.get_json()
    new_pass = data.get('password')
    if not new_pass: return jsonify({'message': 'Password required'}), 400
    
    hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hashed, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Password updated'})

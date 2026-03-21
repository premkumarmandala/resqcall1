from flask import Blueprint, request, jsonify
from backend.db import mysql
from backend.utils import token_required, admin_required

hospitals_bp = Blueprint('hospitals', __name__)

@hospitals_bp.route('/', methods=['GET'])
@token_required
def get_hospitals(current_user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hospitals")
    hospitals = cursor.fetchall()
    cursor.close()
    return jsonify(hospitals)

@hospitals_bp.route('/<int:id>', methods=['GET'])
@token_required
@admin_required
def get_hospital_by_id(current_user, id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE id = %s", (id,))
    hospital = cursor.fetchone()
    cursor.close()
    if not hospital: return jsonify({'message': 'Hospital not found'}), 404
    return jsonify(hospital)

@hospitals_bp.route('/', methods=['POST'])
@token_required
@admin_required
def add_hospital(current_user):
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    contact = data.get('contact_phone')
    total_beds = data.get('total_beds', 0)
    icu_beds = data.get('icu_beds', 0)
    
    if not all([name, address, contact]):
        return jsonify({'message': 'Missing required fields'}), 400
        
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO hospitals (name, address, contact_phone, total_beds, icu_beds)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, address, contact, total_beds, icu_beds))
    mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({'message': 'Hospital added', 'id': new_id}), 201

@hospitals_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_hospital(current_user, id):
    data = request.get_json()
    
    # Permission Check
    if current_user['role'] != 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin_user_id FROM hospitals WHERE id=%s", (id,))
        owner = cursor.fetchone()
        cursor.close()
        if not owner or owner['admin_user_id'] != current_user['id']:
             return jsonify({'message': 'Unauthorized'}), 403

    allowed_fields = [
        'name', 'address', 'contact_phone', 'total_beds', 'icu_beds', 'oxygen_status', 
        'medical_equipment', 'doctor_details', 'reg_number', 'hospital_type', 
        'city', 'district', 'state', 'pin_code', 'alternate_phone', 'official_email',
        'available_beds', 'available_icu_beds', 'ventilators_count', 'has_emergency', 
        'has_trauma', 'has_cardiac', 'has_burn', 'has_blood_bank', 'has_ambulance', 
        'ambulance_count', 'doctors_on_duty', 'nurses_on_duty', 'is_24_7', 
        'working_hours', 'status', 'medicine_readiness', 'latitude', 'longitude'
    ]
    fields = []
    values = []
    
    import json
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field}=%s")
            val = data[field]
            if field == 'medicine_readiness' and isinstance(val, (dict, list)):
                val = json.dumps(val)
            values.append(val)
            
    if not fields: return jsonify({'message': 'No changes'}), 400
        
    values.append(id)
    
    cursor = mysql.connection.cursor()
    query = f"UPDATE hospitals SET {', '.join(fields)} WHERE id=%s"
    cursor.execute(query, tuple(values))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Hospital updated'})

@hospitals_bp.route('/invite', methods=['POST'])
@token_required
@admin_required
def invite_hospital(current_user):
    data = request.get_json()
    email_to = data.get('email')
    if not email_to: return jsonify({'message': 'Email required'}), 400
    
    link = "http://127.0.0.1:8000/register_hospital.html"
    
    import smtplib
    from email.mime.text import MIMEText
    from flask import current_app
    
    msg = MIMEText(f"Hello,\n\nYou have been invited to join the ResQ Emergency Network.\n\nRegister your hospital here:\n{link}\n\nRegards,\nResQ Admin")
    msg['Subject'] = "ResQ Partner Invitation"
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = email_to
    
    try:
        username = current_app.config['MAIL_USERNAME']
        password = current_app.config['MAIL_PASSWORD']
        
        if 'your-email' in username:
            return jsonify({'message': 'Email not configured in backend/config.py'}), 500
            
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            if current_app.config['MAIL_USE_TLS']:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)
            
        return jsonify({'message': f'Invite sent to {email_to}'})
    except Exception as e:
        return jsonify({'message': 'Error sending email', 'error': str(e)}), 500

@hospitals_bp.route('/<int:id>/status', methods=['PUT'])
@token_required
@admin_required
def toggle_status(current_user, id):
    data = request.get_json()
    is_active = data.get('is_active')
    
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE hospitals SET is_active=%s WHERE id=%s", (is_active, id))
    mysql.connection.commit()
    cursor.close()
    
    
    return jsonify({'message': 'Status updated'})

@hospitals_bp.route('/register', methods=['POST'])
def register_hospital_public():
    data = request.get_json()
    
    # User Details
    email = data.get('email')
    password = data.get('password')
    admin_phone = data.get('admin_phone')
    admin_name = data.get('admin_name')
    
    # Required Hospital Details
    hosp_name = data.get('hospital_name')
    address = data.get('address')
    hosp_phone = data.get('hospital_phone')
    
    if not all([email, password, hosp_name, address, hosp_phone]):
        return jsonify({'message': 'Missing required fields'}), 400
        
    import bcrypt
    import json
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Medicine Readiness to JSON
    med_readiness = data.get('medicine_readiness')
    if isinstance(med_readiness, (dict, list)):
        med_readiness = json.dumps(med_readiness)

    cursor = mysql.connection.cursor()
    try:
        # Create User
        cursor.execute("INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, %s, %s, 'hospital_admin')",
                       (admin_name, email, admin_phone, hashed))
        user_id = cursor.lastrowid
        
        # New comprehensive fields
        fields = [
            'name', 'address', 'contact_phone', 'admin_user_id', 'reg_number', 'hospital_type',
            'city', 'district', 'state', 'pin_code', 'latitude', 'longitude',
            'alternate_phone', 'official_email', 'total_beds', 'available_beds',
            'icu_beds', 'available_icu_beds', 'ventilators_count', 'oxygen_status',
            'has_emergency', 'has_trauma', 'has_cardiac', 'has_burn', 'has_blood_bank',
            'has_ambulance', 'ambulance_count', 'doctors_on_duty', 'nurses_on_duty',
            'is_24_7', 'working_hours', 'status', 'medicine_readiness'
        ]
        
        placeholders = ", ".join(["%s"] * len(fields))
        columns = ", ".join(fields)
        
        values = [
            hosp_name, address, hosp_phone, user_id, data.get('reg_number'), data.get('hospital_type'),
            data.get('city'), data.get('district'), data.get('state'), data.get('pin_code'), 
            data.get('latitude'), data.get('longitude'),
            data.get('alternate_phone'), data.get('official_email'), data.get('total_beds', 0), data.get('available_beds', 0),
            data.get('icu_beds', 0), data.get('available_icu_beds', 0), data.get('ventilators_count', 0), data.get('oxygen_status', 'Available'),
            data.get('has_emergency', False), data.get('has_trauma', False), data.get('has_cardiac', False), 
            data.get('has_burn', False), data.get('has_blood_bank', False),
            data.get('has_ambulance', False), data.get('ambulance_count', 0), data.get('doctors_on_duty', 0), data.get('nurses_on_duty', 0),
            data.get('is_24_7', True), data.get('working_hours'), 'Active', med_readiness
        ]
        
        cursor.execute(f"INSERT INTO hospitals ({columns}) VALUES ({placeholders})", tuple(values))
        
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error registering hospital', 'error': str(e)}), 500
    finally:
        cursor.close()
        
    return jsonify({'message': 'Hospital Registered Successfully'}), 201

@hospitals_bp.route('/my-hospital', methods=['GET'])
@token_required
def get_my_hospital(current_user):
    if current_user['role'] != 'hospital_admin':
        return jsonify({'message': 'Unauthorized'}), 403
        
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE admin_user_id = %s", (current_user['id'],))
    hospital = cursor.fetchone()
    cursor.close()
    return jsonify(hospital)

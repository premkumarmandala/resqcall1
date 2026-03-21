from flask import Blueprint, request, jsonify
from backend.db import mysql
from backend.utils import token_required

emergencies_bp = Blueprint('emergencies', __name__)

@emergencies_bp.route('/active', methods=['GET'])
@token_required
def get_active_emergency(current_user):
    cursor = mysql.connection.cursor()
    # Find latest pending or assigned emergency for this user
    query = """
        SELECT e.*, 
               h.name as hospital_name, 
               h.contact_phone as hospital_phone,
               h.latitude as hospital_lat,
               h.longitude as hospital_lng,
               a.vehicle_number, 
               u.phone as driver_phone,
               u.name as driver_name,
               a.current_lat as ambulance_lat,
               a.current_lng as ambulance_lng
        FROM emergencies e
        LEFT JOIN hospitals h ON e.assigned_hospital_id = h.id
        LEFT JOIN ambulances a ON e.assigned_ambulance_id = a.id
        LEFT JOIN users u ON a.driver_user_id = u.id
        WHERE e.user_id = %s AND e.status IN ('Pending', 'Assigned')
        ORDER BY e.created_at DESC LIMIT 1
    """
    cursor.execute(query, (current_user['id'],))
    emergency = cursor.fetchone()
    
    # Simulate Tracking via Database
    if emergency and emergency.get('status') == 'Assigned' and emergency.get('assigned_ambulance_id'):
        amb_lat = emergency.get('ambulance_lat')
        amb_lng = emergency.get('ambulance_lng')
        user_lat = emergency.get('location_lat')
        user_lng = emergency.get('location_lng')
        
        # If the ambulance has no initial coordinates, place it approximately 2km away from the user
        if (not amb_lat or not amb_lng) and user_lat and user_lng:
            amb_lat = float(user_lat) + 0.02
            amb_lng = float(user_lng) + 0.02
            
        if amb_lat and amb_lng and user_lat and user_lng:
            # Move 5% closer to the user on each poll to simulate movement
            new_lat = float(amb_lat) + (float(user_lat) - float(amb_lat)) * 0.05
            new_lng = float(amb_lng) + (float(user_lng) - float(amb_lng)) * 0.05
            
            # Use only database to track the simulated moving ambulance
            cursor.execute("UPDATE ambulances SET current_lat=%s, current_lng=%s WHERE id=%s", 
                           (new_lat, new_lng, emergency['assigned_ambulance_id']))
            mysql.connection.commit()
            
            # Immediately provide the new coordinates to the frontend tracking map
            emergency['ambulance_lat'] = new_lat
            emergency['ambulance_lng'] = new_lng

    cursor.close()
    return jsonify(emergency)

@emergencies_bp.route('/history', methods=['GET'])
@token_required
def get_my_history(current_user):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM emergencies WHERE user_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (current_user['id'],))
    history = cursor.fetchall()
    cursor.close()
    return jsonify(history)

@emergencies_bp.route('/', methods=['GET'])
@token_required
def get_emergencies(current_user):
    cursor = mysql.connection.cursor()
    # List all for admin/dispatcher
    query = """
        SELECT e.*, h.name as hospital_name, a.vehicle_number 
        FROM emergencies e
        LEFT JOIN hospitals h ON e.assigned_hospital_id = h.id
        LEFT JOIN ambulances a ON e.assigned_ambulance_id = a.id
        ORDER BY e.created_at DESC
    """
    cursor.execute(query)
    emergencies = cursor.fetchall()
    cursor.close()
    return jsonify(emergencies)

@emergencies_bp.route('/', methods=['POST'])
@token_required
def create_emergency(current_user):
    data = request.get_json()
    patient = data.get('patient_name', current_user['name'])
    contact = data.get('contact_number', current_user['phone'])
    location = data.get('location_address')
    lat = data.get('location_lat')
    lng = data.get('location_lng')
    severity = data.get('severity', 'Medium')
    emergency_type = data.get('emergency_type', 'Other')
    assigned_ambulance_id = data.get('assigned_ambulance_id')
    assigned_hospital_id = data.get('assigned_hospital_id')
    status = 'Assigned' if assigned_ambulance_id else 'Pending'
    
    cursor = mysql.connection.cursor()
    
    # Check if user already has an active emergency
    cursor.execute("SELECT id FROM emergencies WHERE user_id=%s AND status IN ('Pending', 'Assigned')", (current_user['id'],))
    if cursor.fetchone():
        cursor.close()
        return jsonify({'message': 'You already have an active emergency request'}), 400

    cursor.execute("""
        INSERT INTO emergencies (patient_name, contact_number, location_address, location_lat, location_lng, severity, emergency_type, user_id, assigned_ambulance_id, assigned_hospital_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (patient, contact, location, lat, lng, severity, emergency_type, current_user['id'], assigned_ambulance_id, assigned_hospital_id, status))
    
    if assigned_ambulance_id:
        cursor.execute("UPDATE ambulances SET status='On Duty' WHERE id=%s", (assigned_ambulance_id,))
        
    mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({'message': 'Emergency reported', 'id': new_id}), 201

@emergencies_bp.route('/<int:id>/assign', methods=['PUT'])
@token_required
def assign_emergency(current_user, id):
    data = request.get_json()
    ambulance_id = data.get('ambulance_id')
    hospital_id = data.get('hospital_id')
    
    cursor = mysql.connection.cursor()
    # Update status to Assigned
    cursor.execute("""
        UPDATE emergencies 
        SET assigned_ambulance_id=%s, assigned_hospital_id=%s, status='Assigned'
        WHERE id=%s
    """, (ambulance_id, hospital_id, id))
    
    # Also update ambulance status to On Duty
    if ambulance_id:
        cursor.execute("UPDATE ambulances SET status='On Duty' WHERE id=%s", (ambulance_id,))
        
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Emergency assigned'})

@emergencies_bp.route('/<int:id>/resolve', methods=['PUT'])
@token_required
def resolve_emergency(current_user, id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE emergencies SET status='Resolved', resolved_at=NOW() WHERE id=%s", (id,))
    
    # Free up ambulance
    cursor.execute("""
        UPDATE ambulances SET status='Available' 
        WHERE id = (SELECT assigned_ambulance_id FROM emergencies WHERE id=%s)
    """, (id,))
    
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Emergency resolved'})

@emergencies_bp.route('/<int:id>/cancel', methods=['PUT'])
@token_required
def cancel_emergency(current_user, id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_id, assigned_ambulance_id FROM emergencies WHERE id=%s", (id,))
    em = cursor.fetchone()
    if not em or em['user_id'] != current_user['id']:
        cursor.close()
        return jsonify({'message': 'Unauthorized or Not Found'}), 403

    cursor.execute("UPDATE emergencies SET status='Cancelled', resolved_at=NOW() WHERE id=%s", (id,))
    
    if em.get('assigned_ambulance_id'):
        cursor.execute("UPDATE ambulances SET status='Available' WHERE id=%s", (em['assigned_ambulance_id'],))
        
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Emergency cancelled'})

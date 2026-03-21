from flask import Blueprint, request, jsonify
from backend.db import mysql
from backend.utils import token_required, admin_required

ambulances_bp = Blueprint('ambulances', __name__)

@ambulances_bp.route('/', methods=['GET'])
@token_required
def get_ambulances(current_user):
    cursor = mysql.connection.cursor()
    # Join with driver name if needed, but for now raw table
    cursor.execute("""
        SELECT a.*, u.name as driver_name 
        FROM ambulances a 
        LEFT JOIN users u ON a.driver_user_id = u.id
    """)
    ambulances = cursor.fetchall()
    cursor.close()
    return jsonify(ambulances)

@ambulances_bp.route('/', methods=['POST'])
@token_required
@admin_required
def add_ambulance(current_user):
    data = request.get_json()
    vehicle = data.get('vehicle_number')
    driver_id = data.get('driver_user_id')
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO ambulances (vehicle_number, driver_user_id, status) VALUES (%s, %s, 'Available')",
                   (vehicle, driver_id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Ambulance added'}), 201

@ambulances_bp.route('/<int:id>/location', methods=['PUT'])
@token_required
def update_location(current_user, id):
    # Drivers update their own location
    # Or system updates.
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE ambulances SET current_lat=%s, current_lng=%s WHERE id=%s", (lat, lng, id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Location updated'})

from flask import Blueprint, jsonify
from backend.db import mysql
from backend.utils import token_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    cursor = mysql.connection.cursor()
    
    # Active Emergencies
    cursor.execute("SELECT COUNT(*) as count FROM emergencies WHERE status IN ('Pending', 'Assigned')")
    active_emergencies = cursor.fetchone()['count']
    
    # Available Ambulances
    cursor.execute("SELECT COUNT(*) as count FROM ambulances WHERE status = 'Available'")
    available_ambulances = cursor.fetchone()['count']
    
    # Total Hospitals
    cursor.execute("SELECT COUNT(*) as count FROM hospitals WHERE is_active = 1")
    active_hospitals = cursor.fetchone()['count']
    
    cursor.close()
    
    return jsonify({
        'active_emergencies': active_emergencies,
        'available_ambulances': available_ambulances,
        'active_hospitals': active_hospitals
    })

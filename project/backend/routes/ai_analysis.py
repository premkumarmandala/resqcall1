from flask import Blueprint, request, jsonify, current_app
from backend.db import mysql
from backend.utils import token_required, send_sms_simulation
from google import genai
import math
import os
import json

ai_analysis_bp = Blueprint('ai_analysis', __name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    if not lat1 or not lon1 or not lat2 or not lon2:
        return 999999
        
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles.
    return c * r

def get_ai_analysis(symptoms):
    """
    Call Google Gemini to analyze symptoms.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        # Return a mock response if no key is configured, to prevent crashing
        return {
            "urgency": "Medium",
            "speciality": "General",
            "ambulance_needed": False,
            "advice": "Please consult a doctor. (API Key Missing)"
        }
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Analyze the following medical symptoms silently.
    Symptoms: "{symptoms}"
    
    Return ONLY a JSON object with the following fields:
    - urgency: "Low", "Medium", "High", or "Critical"
    - speciality: The medical speciality required (e.g., "Cardiology", "Neurology", "General", "Trauma")
    - ambulance_needed: boolean (true if condition seems life-threatening or mobility is compromised)
    - advice: Detailed step-by-step first-aid and immediate advice for the patient (around 3-4 sentences). Give clear instructions on what to do while waiting for help.
    
    Do not include markdown code blocks, just return the raw JSON string.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(text)
        return result
    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "urgency": "High",
            "speciality": "General",
            "ambulance_needed": True,
            "advice": "System is currently busy due to high traffic. High urgency assumed. Please proceed to the nearest hospital immediately and seek emergency medical help."
        }

@ai_analysis_bp.route('/analyze', methods=['POST'])
@token_required
def analyze_symptoms(current_user):
    data = request.get_json()
    symptoms = data.get('symptoms')
    user_lat = data.get('latitude')
    user_lng = data.get('longitude')
    
    if not symptoms:
        return jsonify({'message': 'Symptoms are required'}), 400

    # 1. AI Analysis
    analysis = get_ai_analysis(symptoms)
    
    # 2. Find Nearest Appropriate Hospital
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE status='Active'")
    hospitals = cursor.fetchall()
    cursor.close()
    
    nearest_hospital = None
    min_dist = float('inf')
    
    required_speciality = analysis.get('speciality', 'General')
    
    capable_hospitals = []
    
    for hosp in hospitals:
        # Check capabilities based on speciality
        capable = True
        if analysis.get('urgency') == 'Critical':
            if hosp.get('has_emergency') is False or hosp.get('has_emergency') == 0: capable = False
        
        if required_speciality == 'Cardiology' and (hosp.get('has_cardiac') is False or hosp.get('has_cardiac') == 0): capable = False
        if required_speciality == 'Trauma' and (hosp.get('has_trauma') is False or hosp.get('has_trauma') == 0): capable = False
        
        # If no specific capability match, fall back to just finding nearest emergency one if critical
        if not capable and analysis.get('urgency') == 'Critical':
             pass

        if capable:
            dist = calculate_distance(user_lat, user_lng, hosp['latitude'], hosp['longitude'])
            capable_hospitals.append({'hospital': hosp, 'dist': dist})
    
    # If no specialized hospital found, just get the absolute nearest with Emergency
    if not capable_hospitals and hospitals:
         for hosp in hospitals:
             if hosp.get('has_emergency', True):
                dist = calculate_distance(user_lat, user_lng, hosp['latitude'], hosp['longitude'])
                capable_hospitals.append({'hospital': hosp, 'dist': dist})

    capable_hospitals.sort(key=lambda x: x['dist'])
    top_hospitals = capable_hospitals[:3]
    
    if top_hospitals:
        nearest_hospital = top_hospitals[0]['hospital']
        min_dist = top_hospitals[0]['dist']

    # 2.5 Find Nearest Available Ambulance
    cursor = mysql.connection.cursor() # Re-open cursor
    cursor.execute("SELECT a.*, u.phone as driver_phone, u.name as driver_name FROM ambulances a LEFT JOIN users u ON a.driver_user_id = u.id WHERE a.status='Available'")
    ambulances = cursor.fetchall()
    cursor.close()
    
    nearest_ambulance = None
    min_amb_dist = 999999
    
    for amb in ambulances:
        if amb.get('current_lat') and amb.get('current_lng'):
            dist = calculate_distance(user_lat, user_lng, amb['current_lat'], amb['current_lng'])
            if dist < min_amb_dist:
                min_amb_dist = dist
                nearest_ambulance = amb
    
    response_data = {
        'analysis': analysis,
        'nearby_hospitals': [],
        'nearest_hospital': None,
        'distance_km': None,
        'nearest_ambulance': None,
        'ambulance_distance_km': None
    }
    
    for item in top_hospitals:
        hosp = item['hospital']
        response_data['nearby_hospitals'].append({
            'id': hosp['id'],
            'name': hosp['name'],
            'address': hosp['address'],
            'phone': hosp['contact_phone'],
            'latitude': hosp['latitude'],
            'longitude': hosp['longitude'],
            'distance_km': round(item['dist'], 2)
        })

    if nearest_hospital:
        response_data['nearest_hospital'] = response_data['nearby_hospitals'][0]
        response_data['distance_km'] = round(min_dist, 2)
        
        # 3. Send SMS (Simulation)
        msg = f"ResQCall Alert: Nearest hospital is {nearest_hospital['name']} ({round(min_dist, 2)}km). Advice: {analysis['advice']}"
        send_sms_simulation(current_user['phone'], msg)
        
    if nearest_ambulance:
        response_data['nearest_ambulance'] = {
            'id': nearest_ambulance['id'],
            'vehicle_number': nearest_ambulance['vehicle_number'],
            'driver_phone': nearest_ambulance.get('driver_phone'),
            'driver_name': nearest_ambulance.get('driver_name'),
            'current_lat': nearest_ambulance.get('current_lat'),
            'current_lng': nearest_ambulance.get('current_lng')
        }
        response_data['ambulance_distance_km'] = round(min_amb_dist, 2)

    return jsonify(response_data)

@ai_analysis_bp.route('/chat', methods=['POST'])
@token_required
def chat_with_bot(current_user):
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'reply': "I am unable to connect to my brain. API Key is missing."})
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are ResQ, an emergency medical assistant AI.
    You provide short, concise, safe first-aid advice.
    Do NOT give definitive medical diagnoses. Always remind the user to seek professional medical help or wait for the ambulance if it's an emergency.
    Keep your response brief (max 3-4 sentences). Do not use markdown backticks unless strictly necessary.
    
    User says: {message}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.replace('*', '').strip() # Strip markdown asterisks to keep formatting simple
        return jsonify({'reply': text})
    except Exception as e:
        print(f"AI Chat Error: {e}")
        return jsonify({'reply': "I'm having trouble thinking right now. Please seek immediate human help."})

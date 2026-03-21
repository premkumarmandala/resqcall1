from flask import Blueprint, jsonify, request, g
import os
import datetime
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client
from backend.db import mysql
from backend.utils import token_required

# Blueprint for Twilio Call Handling and Admin Logs
call_bp = Blueprint('call_bp', __name__)

# --- User Call Logic (In-Browser Phone) ---

@call_bp.route('/token', methods=['POST'])
@token_required
def get_capability_token(current_user):
    """Generates a capability token for the browser client."""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    api_key = os.environ.get('TWILIO_API_KEY')
    api_secret = os.environ.get('TWILIO_API_SECRET')
    twiml_app_sid = os.environ.get('TWILIO_TWIML_APP_SID')
    identity = str(g.user_id) if hasattr(g, 'user_id') else 'guest'

    if not all([account_sid, api_key, api_secret, twiml_app_sid]):
        return jsonify({'error': True, 'message': 'Twilio config missing'}), 500

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    voice_grant = VoiceGrant(
        outgoing_application_sid=twiml_app_sid,
        incoming_allow=True
    )
    token.add_grant(voice_grant)

    return jsonify({'token': token.to_jwt()})

@call_bp.route('/voice', methods=['POST'])
def voice():
    """TwiML callback for outgoing calls."""
    resp = VoiceResponse()
    
    # Enable recording for the call (dual-channel for best quality)
    dial = Dial(
        callerId=os.environ.get('TWILIO_PHONE_NUMBER'),
        record='record-from-ringing-dual',
        recordingStatusCallback='/call/recording-status'
    )
    
    # Retrieve User ID sent from client via custom params if available, else derive from Caller
    # Ideally should pass user info, but for simplicity assuming fixed receiver for now.
    user_id = request.values.get('user_id', None)
    
    # Dial the SOS number
    dial.number('9676097120')
    resp.append(dial)

    # Log initial call attempt (details will update on status callback)
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO call_logs (call_sid, user_id, status, start_time) 
            VALUES (%s, %s, %s, NOW())
        """, (request.values.get('CallSid'), user_id, 'initiated'))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error logging call start: {e}")

    return str(resp)

@call_bp.route('/recording-status', methods=['POST'])
def recording_status():
    """Webhook to receive recording URL when call ends."""
    call_sid = request.values.get('CallSid')
    recording_url = request.values.get('RecordingUrl')
    duration = request.values.get('RecordingDuration')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE call_logs 
            SET recording_url = %s, duration = %s, status = 'completed', end_time = NOW()
            WHERE call_sid = %s
        """, (recording_url, duration, call_sid))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error updating recording: {e}")
        
    return 'OK', 200

@call_bp.route('/log-external', methods=['POST'])
def log_external_call():
    """Logs a call made via the system dialer (tel: link) or simulated calls."""
    user_id = request.json.get('user_id')
    duration = request.json.get('duration', 0)
    status = request.json.get('status', 'completed')
    # Generate a pseudo ID for tracking
    pseudo_sid = f"ext-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO call_logs (call_sid, user_id, status, start_time, duration) 
            VALUES (%s, %s, %s, NOW(), %s)
        """, (pseudo_sid, user_id, status, duration))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True, 'message': 'Logged'}), 200
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500

# --- Admin Dashboard Logic ---

@call_bp.route('/history', methods=['GET'])
def get_call_history():
    """Retrieve call logs for the admin dashboard."""
    # Add admin check here if needed
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, user_id, call_sid, status, start_time, duration, recording_url 
            FROM call_logs 
            ORDER BY start_time DESC 
            LIMIT 50
        """)
        logs = cur.fetchall()
        cur.close()
        
        history = []
        for log in logs:
            history.append({
                'id': log['id'],
                'user_id': log['user_id'],
                'call_sid': log['call_sid'],
                'status': log['status'],
                'start_time': log['start_time'],
                'duration': log['duration'],
                'recording_url': log['recording_url']
            })
            
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500

@call_bp.route('/me', methods=['GET'])
@token_required
def get_my_call_history(current_user):
    """Retrieve call logs for the logged-in user."""
    try:
        user_id = g.user_id
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, call_sid, status, start_time, duration, recording_url 
            FROM call_logs 
            WHERE user_id = %s
            ORDER BY start_time DESC 
            LIMIT 50
        """, (user_id,))
        logs = cur.fetchall()
        cur.close()
        
        history = []
        for log in logs:
            history.append({
                'id': log['id'],
                'call_sid': log['call_sid'],
                'status': log['status'],
                'start_time': log['start_time'],
                'duration': log['duration'],
                'recording_url': log['recording_url']
            })
            
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 500

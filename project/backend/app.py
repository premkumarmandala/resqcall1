import json
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from backend.config import Config
from backend.db import mysql
from backend.routes.auth import auth_bp
from backend.routes.hospitals import hospitals_bp
from backend.routes.ambulances import ambulances_bp
from backend.routes.emergencies import emergencies_bp
from backend.routes.dashboard import dashboard_bp
from backend.routes.users import users_bp
from backend.routes.ai_analysis import ai_analysis_bp

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json_provider_class = UpdatedJSONProvider
    app.json = UpdatedJSONProvider(app)
    
    # Global trailing slash policy: Allow both /route and /route/
    app.url_map.strict_slashes = False
    
    # Initialize extensions
    mysql.init_app(app)
    CORS(app, supports_credentials=True, origins=["*"]) 
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(hospitals_bp, url_prefix='/hospitals')
    app.register_blueprint(ambulances_bp, url_prefix='/ambulances')
    app.register_blueprint(emergencies_bp, url_prefix='/emergencies')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(ai_analysis_bp, url_prefix='/ai')
    
    from backend.routes.call import call_bp
    app.register_blueprint(call_bp, url_prefix='/call')
    


    @app.route('/')
    def index():
        return jsonify({'message': 'Emergency Rescue API is running'})

    @app.route('/config')
    def get_config():
        return jsonify({
            'GOOGLE_MAPS_API_KEY': app.config.get('GOOGLE_MAPS_API_KEY', '')
        })
    @app.errorhandler(Exception)
    def handle_exception(e):
        response = jsonify({"message": "Internal Server Error", "error": str(e)})
        response.status_code = 500
        return response
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

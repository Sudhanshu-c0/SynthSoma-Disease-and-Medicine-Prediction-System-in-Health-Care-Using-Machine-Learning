import os
from flask import Flask, render_template
from flask_login import LoginManager
from config import config_by_name
from database.db import db
from models.database_models import User
from services.auth_service import seed_default_admin
from utils.error_handler import register_error_handlers
from utils.helpers import format_datetime, get_medical_disclaimer
from utils.model_loader import get_model_loader

# Import Blueprints
from routes.home_routes import home_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.disease_routes import disease_bp
from routes.medicine_routes import medicine_bp
from routes.precaution_routes import precaution_bp
from routes.risk_factor_routes import risk_factor_bp
from routes.history_routes import history_bp
from routes.profile_routes import profile_bp
from routes.report_routes import report_bp
from routes.export_routes import export_bp
from routes.admin_routes import admin_bp

def create_app(config_name=None):
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development')
        
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this healthcare module.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(disease_bp)
    app.register_blueprint(medicine_bp)
    app.register_blueprint(precaution_bp)
    app.register_blueprint(risk_factor_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(admin_bp)

    # Register error handlers
    register_error_handlers(app)

    # Template context processors and filters
    @app.context_processor
    def inject_global_template_context():
        return {
            'medical_disclaimer': get_medical_disclaimer(),
            'app_name': 'SynthSoma',
            'current_year': 2026
        }

    app.jinja_env.filters['datetime'] = format_datetime

    # Create tables and seed admin
    with app.app_context():
        db.create_all()
        try:
            seed_default_admin(app)
        except Exception as e:
            app.logger.warning(f"Admin seeding note: {e}")
            
        # Warm-up model loader singleton
        try:
            get_model_loader()
        except Exception as e:
            app.logger.warning(f"Model warm-up note: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    import socket
    def is_port_in_use(p):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', p)) == 0
            
    if is_port_in_use(port) and port == 5000:
        print("Note: Port 5000 is in use (often macOS AirPlay Receiver). Switching to port 5001.")
        port = 5001

    app.run(host='0.0.0.0', port=port, debug=True)


import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'synthsoma-secret-key-production-grade-2026')
    
    # Instance and Database
    INSTANCE_DIR = BASE_DIR / 'instance'
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{INSTANCE_DIR / 'synthsoma.db'}"
    )
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite:///') and not SQLALCHEMY_DATABASE_URI.startswith('sqlite:////'):
        # Normalize relative sqlite path to instance directory
        db_filename = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / db_filename}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds
    
    # Directories
    MODELS_DIR = BASE_DIR / 'models' / 'ml'
    DATASETS_RAW_DIR = BASE_DIR / 'datasets' / 'raw'
    DATASETS_CLEANED_DIR = BASE_DIR / 'datasets' / 'cleaned'
    DATASETS_PROCESSED_DIR = BASE_DIR / 'datasets' / 'processed'
    REPORTS_DIR = BASE_DIR / 'reports'
    EXPORTS_DIR = BASE_DIR / 'exports'
    UPLOADS_DIR = BASE_DIR / 'uploads'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Ensure all runtime output dirs exist
    for directory in [
        REPORTS_DIR / 'disease',
        REPORTS_DIR / 'medicine',
        REPORTS_DIR / 'precaution',
        REPORTS_DIR / 'risk_factor',
        EXPORTS_DIR / 'disease',
        EXPORTS_DIR / 'medicine',
        EXPORTS_DIR / 'precaution',
        EXPORTS_DIR / 'risk_factor',
        EXPORTS_DIR / 'history',
        UPLOADS_DIR / 'temporary',
        LOGS_DIR
    ]:
        directory.mkdir(parents=True, exist_ok=True)
        
    # Admin defaults
    ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@synthsoma.org')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@SynthSoma2026!')
    ADMIN_NAME = os.environ.get('ADMIN_NAME', 'SynthSoma System Administrator')
    ADMIN_PHONE = os.environ.get('ADMIN_PHONE', '+1-800-555-0199')
    ADMIN_LOCATION = os.environ.get('ADMIN_LOCATION', 'Clinical Systems Hub')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

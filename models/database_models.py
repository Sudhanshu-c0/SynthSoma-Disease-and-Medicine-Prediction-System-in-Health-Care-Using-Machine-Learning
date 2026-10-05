from datetime import datetime
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'admin'
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    module = db.Column(db.String(50), nullable=False, index=True)  # 'disease', 'medicine', 'precaution', 'risk_factor'
    input_summary = db.Column(db.Text, nullable=False)
    result_summary = db.Column(db.Text, nullable=False)
    details_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def get_details(self):
        if self.details_json:
            try:
                return json.loads(self.details_json)
            except Exception:
                return {}
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module': self.module,
            'input_summary': self.input_summary,
            'result_summary': self.result_summary,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class DiseasePrediction(db.Model):
    __tablename__ = 'disease_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id', ondelete='CASCADE'), nullable=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    selected_symptoms = db.Column(db.Text, nullable=False)
    predicted_disease = db.Column(db.String(120), nullable=False, index=True)
    confidence = db.Column(db.Float, nullable=True)
    model_used = db.Column(db.String(80), nullable=False)
    risk_factors = db.Column(db.Text, nullable=True)
    precautions = db.Column(db.Text, nullable=True)
    medicines = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

class MedicinePrediction(db.Model):
    __tablename__ = 'medicine_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id', ondelete='CASCADE'), nullable=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    disease_input = db.Column(db.String(120), nullable=False, index=True)
    predicted_medicines = db.Column(db.Text, nullable=False)
    medicine_details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

class PrecautionPrediction(db.Model):
    __tablename__ = 'precaution_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id', ondelete='CASCADE'), nullable=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    disease_input = db.Column(db.String(120), nullable=False, index=True)
    precautions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

class RiskFactorPrediction(db.Model):
    __tablename__ = 'risk_factor_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id', ondelete='CASCADE'), nullable=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    disease_input = db.Column(db.String(120), nullable=False, index=True)
    matched_disease = db.Column(db.String(120), nullable=False)
    risk_factors = db.Column(db.Text, nullable=False)
    occurrence = db.Column(db.String(200), nullable=True)
    clinical_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

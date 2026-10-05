from flask import Blueprint, render_template
from utils.model_loader import get_model_loader

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    loader = get_model_loader()
    stats = {
        'symptoms_count': len(loader.get_disease_symptoms()),
        'diseases_count': len(loader.get_disease_names()),
        'medicines_count': len(loader.medicine_model.get('catalog', {})) if loader.medicine_model else 62,
        'risk_profiles_count': len(loader.get_risk_diseases())
    }
    return render_template('home/index.html', stats=stats)

@home_bp.route('/about')
def about():
    return render_template('home/index.html', section='about')

@home_bp.route('/disclaimer')
def disclaimer():
    return render_template('home/index.html', section='disclaimer')

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.risk_factor_service import analyze_risk_factors
from utils.model_loader import get_model_loader
from services.history_service import get_prediction_by_id

risk_factor_bp = Blueprint('risk_factor', __name__, url_prefix='/risk-factor')

@risk_factor_bp.route('/', methods=['GET'])
@login_required
def risk_factor_form():
    loader = get_model_loader()
    known_diseases = sorted(loader.get_risk_diseases())
    return render_template('risk_factor/risk_factor_form.html', known_diseases=known_diseases)

@risk_factor_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    disease_name = request.form.get('disease_name', '').strip()
    if not disease_name:
        flash("Please enter or select a disease name for risk factor analysis.", "warning")
        return redirect(url_for('risk_factor.risk_factor_form'))

    try:
        result = analyze_risk_factors(user=current_user, disease_name=disease_name, save_history=True)
        return render_template('risk_factor/risk_factor_result.html', result=result)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('risk_factor.risk_factor_form'))
    except Exception as e:
        flash(f"Risk factor analysis failed: {str(e)}", "danger")
        return redirect(url_for('risk_factor.risk_factor_form'))

@risk_factor_bp.route('/result/<int:prediction_id>')
@login_required
def view_result(prediction_id):
    rec = get_prediction_by_id(prediction_id, current_user)
    if not rec or rec.module != 'risk_factor':
        flash("Prediction record not found or unauthorized.", "danger")
        return redirect(url_for('history.history_index'))
    result = rec.get_details()
    result['id'] = rec.id
    return render_template('risk_factor/risk_factor_result.html', result=result)

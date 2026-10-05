from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.precaution_service import predict_precaution
from utils.model_loader import get_model_loader
from services.history_service import get_prediction_by_id

precaution_bp = Blueprint('precaution', __name__, url_prefix='/precaution')

@precaution_bp.route('/', methods=['GET'])
@login_required
def precaution_form():
    loader = get_model_loader()
    known_diseases = sorted(loader.get_precaution_diseases())
    return render_template('precaution/precaution_form.html', known_diseases=known_diseases)

@precaution_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    disease_name = request.form.get('disease_name', '').strip()
    if not disease_name:
        flash("Please enter or select a disease name.", "warning")
        return redirect(url_for('precaution.precaution_form'))

    try:
        result = predict_precaution(user=current_user, disease_name=disease_name, save_history=True)
        return render_template('precaution/precaution_result.html', result=result)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('precaution.precaution_form'))
    except Exception as e:
        flash(f"Precaution suggestion failed: {str(e)}", "danger")
        return redirect(url_for('precaution.precaution_form'))

@precaution_bp.route('/result/<int:prediction_id>')
@login_required
def view_result(prediction_id):
    rec = get_prediction_by_id(prediction_id, current_user)
    if not rec or rec.module != 'precaution':
        flash("Prediction record not found or unauthorized.", "danger")
        return redirect(url_for('history.history_index'))
    result = rec.get_details()
    result['id'] = rec.id
    return render_template('precaution/precaution_result.html', result=result)

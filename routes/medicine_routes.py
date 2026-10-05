from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.medicine_prediction_service import predict_medicine
from utils.model_loader import get_model_loader
from services.history_service import get_prediction_by_id

medicine_bp = Blueprint('medicine', __name__, url_prefix='/medicine')

@medicine_bp.route('/', methods=['GET'])
@login_required
def medicine_form():
    loader = get_model_loader()
    known_diseases = sorted(loader.get_medicine_diseases())
    return render_template('medicine/medicine_form.html', known_diseases=known_diseases)

@medicine_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    disease_name = request.form.get('disease_name', '').strip()
    if not disease_name:
        flash("Please enter or select a disease name.", "warning")
        return redirect(url_for('medicine.medicine_form'))

    try:
        result = predict_medicine(user=current_user, disease_name=disease_name, save_history=True)
        return render_template('medicine/medicine_result.html', result=result)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('medicine.medicine_form'))
    except Exception as e:
        flash(f"Medicine recommendation failed: {str(e)}", "danger")
        return redirect(url_for('medicine.medicine_form'))

@medicine_bp.route('/result/<int:prediction_id>')
@login_required
def view_result(prediction_id):
    rec = get_prediction_by_id(prediction_id, current_user)
    if not rec or rec.module != 'medicine':
        flash("Prediction record not found or unauthorized.", "danger")
        return redirect(url_for('history.history_index'))
    result = rec.get_details()
    result['id'] = rec.id
    return render_template('medicine/medicine_result.html', result=result)

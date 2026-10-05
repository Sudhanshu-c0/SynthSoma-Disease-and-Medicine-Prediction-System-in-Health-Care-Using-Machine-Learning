from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.disease_prediction_service import predict_disease
from utils.symptom_mapper import get_formatted_symptoms
from utils.model_loader import get_model_loader
from services.history_service import get_prediction_by_id

disease_bp = Blueprint('disease', __name__, url_prefix='/disease')

@disease_bp.route('/', methods=['GET'])
@login_required
def disease_form():
    loader = get_model_loader()
    symptoms = get_formatted_symptoms()
    classifiers = loader.get_available_disease_classifiers()
    default_clf = loader.get_default_disease_classifier()
    return render_template(
        'disease/disease_form.html',
        symptoms=symptoms,
        classifiers=classifiers,
        default_classifier=default_clf
    )

@disease_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    # Can receive multiple selected symptoms via checkbox or search input
    selected_symptoms = request.form.getlist('symptoms')
    text_symptoms = request.form.get('symptoms_text', '').strip()
    classifier_name = request.form.get('classifier')

    all_inputs = list(selected_symptoms)
    if text_symptoms:
        all_inputs.extend([s.strip() for s in text_symptoms.split(',') if s.strip()])

    if not all_inputs:
        flash("Please select or enter at least one clinical symptom.", "warning")
        return redirect(url_for('disease.disease_form'))

    try:
        result = predict_disease(
            user=current_user,
            symptom_inputs=all_inputs,
            classifier_name=classifier_name,
            save_history=True
        )
        return render_template('disease/disease_result.html', result=result)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('disease.disease_form'))
    except Exception as e:
        flash(f"Disease prediction failed: {str(e)}", "danger")
        return redirect(url_for('disease.disease_form'))

@disease_bp.route('/result/<int:prediction_id>')
@login_required
def view_result(prediction_id):
    rec = get_prediction_by_id(prediction_id, current_user)
    if not rec or rec.module != 'disease':
        flash("Prediction record not found or unauthorized.", "danger")
        return redirect(url_for('history.history_index'))
    result = rec.get_details()
    result['id'] = rec.id
    return render_template('disease/disease_result.html', result=result)

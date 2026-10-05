import json
import numpy as np
import pandas as pd
from datetime import datetime
from utils.model_loader import get_model_loader
from utils.symptom_mapper import map_user_input_to_features, format_symptom_display
from models.database_models import db, Prediction, DiseasePrediction

def predict_disease(user, symptom_inputs, classifier_name=None, save_history=True):
    loader = get_model_loader()
    
    if not loader.disease_system:
        raise ValueError("Disease Prediction System model artifact is not loaded.")
        
    system = loader.disease_system
    models_dict = system.get('models', {})
    default_model = system.get('default_model', 'K-Nearest Neighbors (Cosine)')
    symptom_features = system.get('symptom_features', [])
    label_encoder = system.get('label_encoder')
    
    if not symptom_features or not label_encoder:
        raise ValueError("Symptom features or label encoder missing in disease system.")
        
    # Model selection
    if not classifier_name or classifier_name not in models_dict:
        classifier_name = default_model
    model = models_dict[classifier_name]
    
    # Map input symptoms to feature space
    if isinstance(symptom_inputs, str):
        raw_list = [s.strip() for s in symptom_inputs.split(',') if s.strip()]
    elif isinstance(symptom_inputs, list):
        raw_list = symptom_inputs
    else:
        raw_list = []
        
    active_features = map_user_input_to_features(raw_list, symptom_features)
    if not active_features:
        raise ValueError("None of the provided symptoms could be mapped to recognized clinical features.")

    # Construct input vector with exact feature ordering
    input_vector = np.zeros((1, len(symptom_features)), dtype=np.float32)
    feature_to_idx = {feat: idx for idx, feat in enumerate(symptom_features)}
    
    for feat in active_features:
        if feat in feature_to_idx:
            input_vector[0, feature_to_idx[feat]] = 1.0

    # Model inference
    pred_idx = model.predict(input_vector)[0]
    predicted_disease = str(label_encoder.inverse_transform([pred_idx])[0])

    # Confidence calculation if available
    confidence = None
    if hasattr(model, 'predict_proba'):
        try:
            probas = model.predict_proba(input_vector)[0]
            confidence = float(np.max(probas))
        except Exception:
            confidence = None

    # Retrieve supporting reference information from model lookups & datasets
    normalized_disease = predicted_disease.lower().strip()
    
    # 1. Precautions lookup
    precautions = []
    if 'precaution_lookup' in system and normalized_disease in system['precaution_lookup']:
        precautions = system['precaution_lookup'][normalized_disease]
    elif loader.precaution_df is not None:
        row = loader.precaution_df[loader.precaution_df['Disease'].str.lower() == normalized_disease]
        if not row.empty:
            prec_cols = [c for c in row.columns if 'precaution' in c.lower()]
            precautions = [str(row.iloc[0][c]) for c in prec_cols if pd.notna(row.iloc[0][c])]

    # 2. Risk factors & Occurrence lookup
    risk_factors = []
    occurrence_info = 'Information not available'
    clinical_note = ''
    if 'risk_lookup' in system and normalized_disease in system['risk_lookup']:
        rinfo = system['risk_lookup'][normalized_disease]
        if isinstance(rinfo, dict):
            rf_val = rinfo.get('risk_factors', '')
            if isinstance(rf_val, str):
                risk_factors = [rf.strip() for rf in rf_val.split(',') if rf.strip()]
            elif isinstance(rf_val, list):
                risk_factors = rf_val
            occurrence_info = rinfo.get('occurrences') or rinfo.get('occurrence_frequency') or 'Reference occurrence profile'
            clinical_note = (rinfo.get('clinical_precaution') or rinfo.get('clinical_precaution_note') or '').strip()
    elif loader.disease_info_df is not None:
        row = loader.disease_info_df[loader.disease_info_df['DNAME'].str.lower() == normalized_disease]
        if not row.empty:
            if 'RISKFAC' in row.columns and pd.notna(row.iloc[0]['RISKFAC']):
                risk_factors = [rf.strip() for rf in str(row.iloc[0]['RISKFAC']).split(',') if rf.strip()]
            if 'OCCUR' in row.columns and pd.notna(row.iloc[0]['OCCUR']):
                occurrence_info = str(row.iloc[0]['OCCUR'])
            if 'PRECAU' in row.columns and pd.notna(row.iloc[0]['PRECAU']):
                clinical_note = str(row.iloc[0]['PRECAU'])

    # 3. Reference medicines lookup
    medicines = []
    if 'medicine_lookup' in system and normalized_disease in system['medicine_lookup']:
        minfo = system['medicine_lookup'][normalized_disease]
        if isinstance(minfo, list):
            medicines = [
                m.get('name', '').replace('\xa0', ' ').strip() if isinstance(m, dict) else str(m).strip()
                for m in minfo
            ]
        elif isinstance(minfo, dict):
            medicines = minfo.get('medicines', [])

    # Formatted display of active symptoms
    formatted_symptoms = [format_symptom_display(s) for s in active_features]

    result_data = {
        'predicted_disease': predicted_disease.title(),
        'confidence': confidence,
        'confidence_percentage': f"{confidence * 100:.1f}%" if confidence is not None else None,
        'model_used': classifier_name,
        'selected_symptoms': formatted_symptoms,
        'symptom_features': active_features,
        'precautions': precautions,
        'risk_factors': risk_factors,
        'occurrence_frequency': occurrence_info,
        'clinical_note': clinical_note,
        'reference_medicines': medicines,
        'disclaimer': (
            "Medical Reference Notice: Disease prediction is generated by statistical machine learning models "
            "for informational support only. Do not use for definitive clinical self-diagnosis."
        )
    }

    # Save to history if user is provided and save_history is True
    if save_history and user:
        prediction_master = Prediction(
            user_id=user.user_id,
            module='disease',
            input_summary=', '.join(formatted_symptoms),
            result_summary=f"{predicted_disease.title()} ({classifier_name})",
            details_json=json.dumps(result_data)
        )
        db.session.add(prediction_master)
        db.session.flush()

        disease_rec = DiseasePrediction(
            prediction_id=prediction_master.id,
            user_id=user.user_id,
            selected_symptoms=', '.join(formatted_symptoms),
            predicted_disease=predicted_disease.title(),
            confidence=confidence,
            model_used=classifier_name,
            risk_factors=json.dumps(risk_factors),
            precautions=json.dumps(precautions),
            medicines=json.dumps(medicines),
            created_at=prediction_master.created_at
        )
        db.session.add(disease_rec)
        db.session.commit()
        result_data['id'] = prediction_master.id
        result_data['disease_prediction_id'] = disease_rec.id

    return result_data

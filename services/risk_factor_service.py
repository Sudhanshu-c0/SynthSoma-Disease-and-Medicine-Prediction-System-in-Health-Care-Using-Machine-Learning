import json
from utils.model_loader import get_model_loader
from models.database_models import db, Prediction, RiskFactorPrediction
from utils.validators import validate_disease_input

def analyze_risk_factors(user, disease_name, save_history=True):
    is_valid, err_or_name = validate_disease_input(disease_name)
    if not is_valid:
        raise ValueError(err_or_name)
        
    loader = get_model_loader()
    if not loader.risk_model or not loader.risk_encoder:
        raise ValueError("Risk Factor Analysis model artifact is not loaded.")
        
    model = loader.risk_model['model']
    vectorizer = loader.risk_encoder['vectorizer']
    disease_names = loader.risk_encoder['disease_names']
    risk_profiles = loader.risk_model.get('risk_profiles', {})
    
    clean_name = err_or_name.lower().strip()
    
    # Transform with character n-gram TF-IDF vectorizer
    X = vectorizer.transform([clean_name])
    distances, indices = model.kneighbors(X, n_neighbors=1)
    
    match_idx = indices[0][0]
    matched_name = disease_names[match_idx]
    distance = float(distances[0][0])
    similarity = max(0.0, 1.0 - distance)
    
    profile = risk_profiles.get(matched_name, {})
    risk_factors = profile.get('risk_factors', [])
    occurrence = profile.get('occurrence_frequency', 'Reference occurrence data unavailable')
    clinical_note = profile.get('clinical_precaution_note', '')
    disease_id = profile.get('disease_id', 'N/A')

    result_data = {
        'disease_input': disease_name.title(),
        'matched_disease': matched_name.title(),
        'similarity_score': f"{similarity * 100:.1f}%",
        'disease_id': disease_id,
        'risk_factors': risk_factors,
        'risk_factor_count': len(risk_factors),
        'occurrence_frequency': occurrence,
        'clinical_note': clinical_note,
        'disclaimer': (
            "Risk Assessment Notice: Risk factor profiles and epidemiological occurrence frequencies are derived from "
            "clinical reference datasets. Individual susceptibility varies significantly with patient history and genetics."
        )
    }

    if save_history and user:
        rf_summary = ', '.join(risk_factors) if risk_factors else 'Standard clinical baseline'
        prediction_master = Prediction(
            user_id=user.user_id,
            module='risk_factor',
            input_summary=disease_name.title(),
            result_summary=f"Matched {matched_name.title()}: {rf_summary}",
            details_json=json.dumps(result_data)
        )
        db.session.add(prediction_master)
        db.session.flush()

        risk_rec = RiskFactorPrediction(
            prediction_id=prediction_master.id,
            user_id=user.user_id,
            disease_input=disease_name.title(),
            matched_disease=matched_name.title(),
            risk_factors=json.dumps(risk_factors),
            occurrence=occurrence,
            clinical_notes=clinical_note,
            created_at=prediction_master.created_at
        )
        db.session.add(risk_rec)
        db.session.commit()
        result_data['id'] = prediction_master.id
        result_data['risk_factor_prediction_id'] = risk_rec.id

    return result_data

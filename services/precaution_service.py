import json
from utils.model_loader import get_model_loader
from models.database_models import db, Prediction, PrecautionPrediction
from utils.validators import validate_disease_input

def predict_precaution(user, disease_name, save_history=True):
    is_valid, err_or_name = validate_disease_input(disease_name)
    if not is_valid:
        raise ValueError(err_or_name)
        
    loader = get_model_loader()
    if not loader.precaution_model or not loader.precaution_encoder:
        raise ValueError("Precaution Prediction model artifact is not loaded.")
        
    model = loader.precaution_model['model']
    vectorizer = loader.precaution_encoder['vectorizer']
    binarizer = loader.precaution_encoder['binarizer']
    prec_db = loader.precaution_model.get('precaution_database', {})
    known_diseases = loader.precaution_encoder.get('known_diseases', [])
    
    clean_name = err_or_name.lower().strip()
    
    # Check if exact or closest match among known diseases
    closest_match = None
    if clean_name in [d.lower() for d in known_diseases]:
        matched_disease = clean_name
    else:
        matches = [d for d in known_diseases if clean_name in d.lower() or d.lower() in clean_name]
        if matches:
            closest_match = matches[0]
            matched_disease = closest_match
        else:
            matched_disease = clean_name

    # Transform with real fitted TF-IDF vectorizer
    X = vectorizer.transform([matched_disease])
    pred = model.predict(X)
    raw_precs = binarizer.inverse_transform(pred)
    
    predicted_precs = list(raw_precs[0]) if raw_precs and len(raw_precs[0]) > 0 else []
    
    # Fallback to database lookup if empty
    if not predicted_precs:
        if matched_disease in prec_db:
            predicted_precs = prec_db[matched_disease]
        elif closest_match and closest_match in prec_db:
            predicted_precs = prec_db[closest_match]

    # Format precautions with bullet points / proper capitalization
    formatted_precs = [p.strip().capitalize() for p in predicted_precs]

    result_data = {
        'disease_input': disease_name.title(),
        'matched_disease': matched_disease.title(),
        'closest_match_used': bool(closest_match and closest_match != clean_name),
        'precautions': formatted_precs,
        'precaution_count': len(formatted_precs),
        'disclaimer': (
            "Precautionary Guidance: These recommended lifestyle and clinical precautions are based on "
            "reference healthcare datasets for general informational purposes. In acute or worsening conditions, "
            "seek immediate clinical evaluation."
        )
    }

    if save_history and user:
        prec_summary = '; '.join(formatted_precs) if formatted_precs else 'No specific precautions predicted'
        prediction_master = Prediction(
            user_id=user.user_id,
            module='precaution',
            input_summary=disease_name.title(),
            result_summary=prec_summary,
            details_json=json.dumps(result_data)
        )
        db.session.add(prediction_master)
        db.session.flush()

        prec_rec = PrecautionPrediction(
            prediction_id=prediction_master.id,
            user_id=user.user_id,
            disease_input=disease_name.title(),
            precautions=json.dumps(formatted_precs),
            created_at=prediction_master.created_at
        )
        db.session.add(prec_rec)
        db.session.commit()
        result_data['id'] = prediction_master.id
        result_data['precaution_prediction_id'] = prec_rec.id

    return result_data

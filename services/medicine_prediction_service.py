import json
from utils.model_loader import get_model_loader
from models.database_models import db, Prediction, MedicinePrediction
from utils.validators import validate_disease_input

def predict_medicine(user, disease_name, save_history=True):
    is_valid, err_or_name = validate_disease_input(disease_name)
    if not is_valid:
        raise ValueError(err_or_name)
        
    loader = get_model_loader()
    if not loader.medicine_model or not loader.medicine_encoder:
        raise ValueError("Medicine Prediction model artifact is not loaded.")
        
    model = loader.medicine_model['model']
    vectorizer = loader.medicine_encoder['vectorizer']
    binarizer = loader.medicine_encoder['binarizer']
    catalog = loader.medicine_model.get('catalog', {})
    known_diseases = loader.medicine_encoder.get('known_diseases', [])
    
    clean_name = err_or_name.lower().strip()
    
    # Check if exact or closest known disease
    closest_match = None
    if clean_name in [d.lower() for d in known_diseases]:
        matched_disease = clean_name
    else:
        # Check substring match
        matches = [d for d in known_diseases if clean_name in d.lower() or d.lower() in clean_name]
        if matches:
            closest_match = matches[0]
            matched_disease = closest_match
        else:
            matched_disease = clean_name

    # Transform using real fitted TF-IDF vectorizer
    X = vectorizer.transform([matched_disease])
    pred = model.predict(X)
    raw_meds = binarizer.inverse_transform(pred)
    
    predicted_med_names = list(raw_meds[0]) if raw_meds and len(raw_meds[0]) > 0 else []
    
    # If 0 predictions and we used original, try with closest match if available
    if not predicted_med_names and closest_match:
        X_close = vectorizer.transform([closest_match])
        raw_meds = binarizer.inverse_transform(model.predict(X_close))
        if raw_meds and len(raw_meds[0]) > 0:
            predicted_med_names = list(raw_meds[0])

    # Enrich with catalog details (composition, description)
    detailed_medicines = []
    for med_name in predicted_med_names:
        # Match med_name in catalog
        info = catalog.get(med_name, {})
        if not info:
            # Try case-insensitive or stripped
            for cat_k, cat_v in catalog.items():
                if cat_k.strip().lower() == med_name.strip().lower():
                    info = cat_v
                    break
                    
        detailed_medicines.append({
            'name': med_name.replace('\xa0', ' '),
            'medicine_id': info.get('medicine_id', 'N/A'),
            'composition': info.get('composition', 'Reference pharmaceutical formulation'),
            'description': info.get('description', 'Consult physician or clinical pharmacist for detailed indications.')
        })

    result_data = {
        'disease_input': disease_name.title(),
        'matched_disease': matched_disease.title(),
        'closest_match_used': bool(closest_match and closest_match != clean_name),
        'medicines': detailed_medicines,
        'medicine_count': len(detailed_medicines),
        'disclaimer': (
            "Reference Medicine Notice: This information is model-based reference intelligence for educational purposes only. "
            "It is NOT a medically validated prescription. Never start, stop, or change any medication or dosage without consulting "
            "a qualified healthcare professional. No dosages are prescribed or implied."
        )
    }

    if save_history and user:
        med_summary = ', '.join([m['name'] for m in detailed_medicines]) if detailed_medicines else 'No direct reference medicines predicted'
        prediction_master = Prediction(
            user_id=user.user_id,
            module='medicine',
            input_summary=disease_name.title(),
            result_summary=med_summary,
            details_json=json.dumps(result_data)
        )
        db.session.add(prediction_master)
        db.session.flush()

        med_rec = MedicinePrediction(
            prediction_id=prediction_master.id,
            user_id=user.user_id,
            disease_input=disease_name.title(),
            predicted_medicines=json.dumps([m['name'] for m in detailed_medicines]),
            medicine_details=json.dumps(detailed_medicines),
            created_at=prediction_master.created_at
        )
        db.session.add(med_rec)
        db.session.commit()
        result_data['id'] = prediction_master.id
        result_data['medicine_prediction_id'] = med_rec.id

    return result_data

from models.database_models import db, User, Prediction, DiseasePrediction, MedicinePrediction, PrecautionPrediction, RiskFactorPrediction
from datetime import datetime, timedelta
from collections import Counter
import json
from sqlalchemy import func
from utils.model_loader import get_model_loader

def get_admin_dashboard_stats():
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)
    
    total_users = User.query.count()
    total_predictions = Prediction.query.count()
    
    # Distinct diseases known across system models
    loader = get_model_loader()
    known_diseases = set(loader.get_disease_names()) | set(loader.get_medicine_diseases()) | set(loader.get_risk_diseases())
    total_known_diseases = len(known_diseases)
    
    # 1. Top Predicted Diseases — Last 7 Days (Querying actual DB records)
    disease_rows = db.session.query(
        DiseasePrediction.predicted_disease,
        func.count(DiseasePrediction.id).label('count')
    ).filter(
        DiseasePrediction.created_at >= seven_days_ago
    ).group_by(
        DiseasePrediction.predicted_disease
    ).order_by(
        func.count(DiseasePrediction.id).desc()
    ).limit(10).all()
    
    top_diseases_7days = [{'disease': r[0], 'count': r[1]} for r in disease_rows]
    
    # 2. Top Predicted Medicines — Last 7 Days (Querying actual DB records)
    med_rows = MedicinePrediction.query.filter(
        MedicinePrediction.created_at >= seven_days_ago
    ).all()
    
    med_counter = Counter()
    for row in med_rows:
        try:
            med_list = json.loads(row.predicted_medicines)
            if isinstance(med_list, list):
                for m in med_list:
                    clean_m = m.replace('\xa0', ' ').strip()
                    if clean_m:
                        med_counter[clean_m] += 1
        except Exception:
            # Fallback for plain text
            for m in row.predicted_medicines.split(','):
                clean_m = m.strip()
                if clean_m:
                    med_counter[clean_m] += 1
                    
    top_medicines_7days = [
        {'medicine': med, 'count': cnt}
        for med, cnt in med_counter.most_common(10)
    ]
    
    # Predictions breakdown by module
    module_breakdown = dict(
        db.session.query(Prediction.module, func.count(Prediction.id)).group_by(Prediction.module).all()
    )

    return {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'total_known_diseases': total_known_diseases,
        'top_diseases_7days': top_diseases_7days,
        'top_medicines_7days': top_medicines_7days,
        'module_breakdown': module_breakdown
    }

def get_all_users(search=None, role=None, limit=50, offset=0):
    query = User.query
    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            (User.user_id.ilike(search_term)) |
            (User.name.ilike(search_term)) |
            (User.email.ilike(search_term)) |
            (User.phone.ilike(search_term)) |
            (User.location.ilike(search_term))
        )
    if role and role != 'all':
        query = query.filter_by(role=role)
        
    total_count = query.count()
    users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    return users, total_count

def get_module_predictions_admin(module, search=None, limit=50, offset=0):
    if module == 'disease':
        query = DiseasePrediction.query
        if search:
            query = query.filter(
                (DiseasePrediction.user_id.ilike(f"%{search}%")) |
                (DiseasePrediction.predicted_disease.ilike(f"%{search}%")) |
                (DiseasePrediction.selected_symptoms.ilike(f"%{search}%"))
            )
        total = query.count()
        records = query.order_by(DiseasePrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    elif module == 'medicine':
        query = MedicinePrediction.query
        if search:
            query = query.filter(
                (MedicinePrediction.user_id.ilike(f"%{search}%")) |
                (MedicinePrediction.disease_input.ilike(f"%{search}%")) |
                (MedicinePrediction.predicted_medicines.ilike(f"%{search}%"))
            )
        total = query.count()
        records = query.order_by(MedicinePrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    elif module == 'precaution':
        query = PrecautionPrediction.query
        if search:
            query = query.filter(
                (PrecautionPrediction.user_id.ilike(f"%{search}%")) |
                (PrecautionPrediction.disease_input.ilike(f"%{search}%")) |
                (PrecautionPrediction.precautions.ilike(f"%{search}%"))
            )
        total = query.count()
        records = query.order_by(PrecautionPrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    elif module == 'risk_factor':
        query = RiskFactorPrediction.query
        if search:
            query = query.filter(
                (RiskFactorPrediction.user_id.ilike(f"%{search}%")) |
                (RiskFactorPrediction.disease_input.ilike(f"%{search}%")) |
                (RiskFactorPrediction.matched_disease.ilike(f"%{search}%"))
            )
        total = query.count()
        records = query.order_by(RiskFactorPrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    return [], 0

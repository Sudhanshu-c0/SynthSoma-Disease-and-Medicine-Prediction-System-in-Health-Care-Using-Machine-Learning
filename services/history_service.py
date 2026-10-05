from models.database_models import db, Prediction, DiseasePrediction, MedicinePrediction, PrecautionPrediction, RiskFactorPrediction, User
from datetime import datetime, timedelta

def get_user_history(user_id, module=None, limit=50, offset=0):
    query = Prediction.query.filter_by(user_id=user_id)
    if module and module != 'all':
        query = query.filter_by(module=module)
    total_count = query.count()
    items = query.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
    return items, total_count

def get_module_specific_history(user_id, module, limit=50, offset=0):
    if module == 'disease':
        query = DiseasePrediction.query.filter_by(user_id=user_id)
        total = query.count()
        records = query.order_by(DiseasePrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    elif module == 'medicine':
        query = MedicinePrediction.query.filter_by(user_id=user_id)
        total = query.count()
        records = query.order_by(MedicinePrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    elif module == 'precaution':
        query = PrecautionPrediction.query.filter_by(user_id=user_id)
        total = query.count()
        records = query.order_by(PrecautionPrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    elif module == 'risk_factor':
        query = RiskFactorPrediction.query.filter_by(user_id=user_id)
        total = query.count()
        records = query.order_by(RiskFactorPrediction.created_at.desc()).offset(offset).limit(limit).all()
        return records, total
    return [], 0

def get_admin_prediction_history(filters=None, limit=50, offset=0):
    filters = filters or {}
    query = Prediction.query.join(User, Prediction.user_id == User.user_id)
    
    # Filter by user_id
    if filters.get('user_id'):
        query = query.filter(Prediction.user_id.ilike(f"%{filters['user_id'].strip()}%"))
        
    # Filter by module
    if filters.get('module') and filters['module'] != 'all':
        query = query.filter(Prediction.module == filters['module'])
        
    # Filter by search query (disease, input, result)
    if filters.get('search'):
        search_term = f"%{filters['search'].strip()}%"
        query = query.filter(
            (Prediction.input_summary.ilike(search_term)) |
            (Prediction.result_summary.ilike(search_term)) |
            (User.name.ilike(search_term)) |
            (User.email.ilike(search_term))
        )
        
    # Filter by date range
    if filters.get('start_date'):
        try:
            start_dt = datetime.strptime(filters['start_date'], '%Y-%m-%d')
            query = query.filter(Prediction.created_at >= start_dt)
        except Exception:
            pass
            
    if filters.get('end_date'):
        try:
            end_dt = datetime.strptime(filters['end_date'], '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Prediction.created_at < end_dt)
        except Exception:
            pass

    total_count = query.count()
    items = query.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
    return items, total_count

def get_prediction_by_id(prediction_id, user=None):
    prediction = Prediction.query.get(prediction_id)
    if not prediction:
        return None
    # Security check: If not admin and not owner, return None
    if user and user.role != 'admin' and prediction.user_id != user.user_id:
        return None
    return prediction

from models.database_models import db, User, Prediction
from sqlalchemy import func
import re

def update_profile(user, data):
    errors = {}
    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    location = (data.get('location') or '').strip()

    if not name or len(name) < 2:
        errors['name'] = 'Full name must be at least 2 characters.'

    phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
    if not phone or len(phone_clean) < 7 or len(phone_clean) > 15:
        errors['phone'] = 'Please enter a valid phone number.'

    if not location:
        errors['location'] = 'Location cannot be empty.'

    if errors:
        return False, errors

    user.name = name
    user.phone = phone
    user.location = location
    db.session.commit()
    return True, {}

def get_user_stats(user_id):
    total = Prediction.query.filter_by(user_id=user_id).count()
    breakdown = dict(
        db.session.query(Prediction.module, func.count(Prediction.id))
        .filter(Prediction.user_id == user_id)
        .group_by(Prediction.module)
        .all()
    )
    return {
        'total_predictions': total,
        'breakdown': breakdown
    }

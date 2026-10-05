import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.risk_factor_service import analyze_risk_factors

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_risk_factor_service(app):
    with app.app_context():
        user = User(
            user_id='risk_tester',
            name='Risk Tester',
            email='risktest@example.com',
            phone='1234567890',
            location='Miami, FL'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        result = analyze_risk_factors(user=user, disease_name='fungal infection', save_history=True)

        assert result is not None
        assert 'matched_disease' in result
        assert result['matched_disease'].lower() == 'fungal infection'
        assert result['risk_factor_count'] > 0
        assert 'occurrence_frequency' in result
        assert 'disclaimer' in result

import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.medicine_prediction_service import predict_medicine

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_medicine_prediction_service(app):
    with app.app_context():
        user = User(
            user_id='med_tester',
            name='Med Tester',
            email='medtest@example.com',
            phone='1234567890',
            location='Denver, CO'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        result = predict_medicine(user=user, disease_name='fungal infection', save_history=True)

        assert result is not None
        assert 'matched_disease' in result
        assert result['matched_disease'].lower() == 'fungal infection'
        assert result['medicine_count'] > 0
        assert 'medicines' in result
        first_med = result['medicines'][0]
        assert 'name' in first_med
        assert 'composition' in first_med
        assert 'description' in first_med
        assert 'disclaimer' in result
        assert 'NOT a medically validated prescription' in result['disclaimer']

import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.precaution_service import predict_precaution

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_precaution_service(app):
    with app.app_context():
        user = User(
            user_id='prec_tester',
            name='Precaution Tester',
            email='prectest@example.com',
            phone='1234567890',
            location='Austin, TX'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        result = predict_precaution(user=user, disease_name='acne', save_history=True)

        assert result is not None
        assert 'matched_disease' in result
        assert result['matched_disease'].lower() == 'acne'
        assert result['precaution_count'] > 0
        assert 'precautions' in result
        assert isinstance(result['precautions'], list)
        assert 'disclaimer' in result

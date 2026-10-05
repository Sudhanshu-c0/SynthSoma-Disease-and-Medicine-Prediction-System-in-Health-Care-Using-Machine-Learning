import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.disease_prediction_service import predict_disease
from services.csv_export_service import export_predictions_to_csv

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_csv_export_content(app):
    with app.app_context():
        user = User(
            user_id='csv_user',
            name='CSV User',
            email='csv@synthsoma.org',
            phone='1234567890',
            location='Atlanta, GA'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        predict_disease(user=user, symptom_inputs=['itching', 'skin_rash'], save_history=True)

        buffer, filename = export_predictions_to_csv(user=user, module='disease', is_admin=False)
        content = buffer.read().decode('utf-8')

        assert 'Prediction ID' in content
        assert 'Predicted Disease' in content
        assert 'csv_user' in content
        assert 'Fungal Infection' in content

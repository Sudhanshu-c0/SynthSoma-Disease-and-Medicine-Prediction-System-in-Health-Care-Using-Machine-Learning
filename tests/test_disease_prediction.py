import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.disease_prediction_service import predict_disease

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_disease_prediction_inference(app):
    with app.app_context():
        user = User(
            user_id='med_user_01',
            name='Clinical Researcher',
            email='research@synthsoma.org',
            phone='1234567890',
            location='Seattle, WA',
            role='user'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        # Run inference with symptoms typical of fungal infection
        symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions']
        result = predict_disease(user=user, symptom_inputs=symptoms, save_history=True)

        assert result is not None
        assert 'predicted_disease' in result
        assert result['predicted_disease'].lower() == 'fungal infection'
        assert result['model_used'] == 'K-Nearest Neighbors (Cosine)'
        assert len(result['selected_symptoms']) == 3
        assert 'precautions' in result
        assert len(result['precautions']) > 0
        assert 'risk_factors' in result
        assert 'occurrence_frequency' in result
        assert 'reference_medicines' in result
        assert 'id' in result

def test_invalid_symptoms_handling(app):
    with app.app_context():
        user = User.query.first()
        with pytest.raises(ValueError) as exc:
            predict_disease(user=user, symptom_inputs=['completely_invented_fake_symptom'], save_history=False)
        assert 'None of the provided symptoms' in str(exc.value)

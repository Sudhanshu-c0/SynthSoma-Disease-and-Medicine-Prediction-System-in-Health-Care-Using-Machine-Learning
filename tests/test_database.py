import pytest
from app import create_app
from database.db import db
from models.database_models import User, Prediction, DiseasePrediction, MedicinePrediction, PrecautionPrediction, RiskFactorPrediction

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_database_tables_and_models(app):
    with app.app_context():
        # Create test user
        user = User(
            user_id='db_tester_01',
            name='Database Tester',
            email='dbtester@example.com',
            phone='1234567890',
            location='San Francisco, CA',
            role='user'
        )
        user.set_password('DbPass123!')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None

        # Create master prediction
        pred = Prediction(
            user_id=user.user_id,
            module='disease',
            input_summary='itching, skin_rash',
            result_summary='Fungal Infection',
            details_json='{"status": "ok"}'
        )
        db.session.add(pred)
        db.session.commit()

        # Create module specific records
        d_pred = DiseasePrediction(
            prediction_id=pred.id,
            user_id=user.user_id,
            selected_symptoms='itching, skin_rash',
            predicted_disease='Fungal Infection',
            confidence=0.98,
            model_used='K-Nearest Neighbors (Cosine)'
        )
        db.session.add(d_pred)
        db.session.commit()

        assert d_pred.id is not None
        assert d_pred.user_id == 'db_tester_01'
        assert d_pred.predicted_disease == 'Fungal Infection'

        # Verify query
        found = DiseasePrediction.query.filter_by(user_id='db_tester_01').first()
        assert found is not None
        assert found.predicted_disease == 'Fungal Infection'

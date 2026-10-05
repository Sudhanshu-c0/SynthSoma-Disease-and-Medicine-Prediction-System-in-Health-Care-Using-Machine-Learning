import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.disease_prediction_service import predict_disease
from services.history_service import get_user_history, get_admin_prediction_history

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_history_isolation(app):
    with app.app_context():
        # User 1
        user1 = User(user_id='user_alpha', name='User Alpha', email='alpha@test.com', phone='1234567890', location='Loc A')
        user1.set_password('Pass1!')
        # User 2
        user2 = User(user_id='user_beta', name='User Beta', email='beta@test.com', phone='1234567890', location='Loc B')
        user2.set_password('Pass2!')
        # Admin
        admin = User(user_id='admin_boss', name='Admin Boss', email='admin@test.com', phone='1234567890', location='HQ', role='admin')
        admin.set_password('AdminPass!')
        
        db.session.add_all([user1, user2, admin])
        db.session.commit()

        # Run predictions for user 1
        predict_disease(user=user1, symptom_inputs=['itching', 'skin_rash'], save_history=True)
        predict_disease(user=user1, symptom_inputs=['high_fever', 'headache'], save_history=True)

        # Run prediction for user 2
        predict_disease(user=user2, symptom_inputs=['joint_pain', 'vomiting'], save_history=True)

        # User 1 history should have exactly 2 records
        u1_history, u1_count = get_user_history('user_alpha')
        assert u1_count == 2
        assert len(u1_history) == 2
        for h in u1_history:
            assert h.user_id == 'user_alpha'

        # User 2 history should have exactly 1 record
        u2_history, u2_count = get_user_history('user_beta')
        assert u2_count == 1
        assert len(u2_history) == 1
        assert u2_history[0].user_id == 'user_beta'

        # Admin history should see all 3 records
        admin_history, admin_count = get_admin_prediction_history()
        assert admin_count == 3
        assert len(admin_history) == 3

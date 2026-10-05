import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.disease_prediction_service import predict_disease
from services.medicine_prediction_service import predict_medicine
from services.admin_service import get_admin_dashboard_stats

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_admin_role_enforcement(client, app):
    with app.app_context():
        # Create normal user
        norm_user = User(user_id='regular_joe', name='Regular Joe', email='joe@test.com', phone='1234567890', location='LA', role='user')
        norm_user.set_password('Pass123!')
        
        # Create admin user
        admin_user = User(user_id='admin_jane', name='Admin Jane', email='jane@test.com', phone='1234567890', location='DC', role='admin')
        admin_user.set_password('Pass123!')

        db.session.add_all([norm_user, admin_user])
        db.session.commit()

    # 1. Unauthenticated request to /admin -> redirected to login
    res = client.get('/admin/', follow_redirects=False)
    assert res.status_code == 302
    assert '/login' in res.headers['Location']

    # 2. Login as regular user and access /admin -> 403 Forbidden!
    client.post('/login', data={'username': 'regular_joe', 'password': 'Pass123!'}, follow_redirects=True)
    res_forbidden = client.get('/admin/')
    assert res_forbidden.status_code == 403

    # 3. Logout and login as admin -> 200 OK!
    client.get('/logout')
    client.post('/login', data={'username': 'admin_jane', 'password': 'Pass123!'}, follow_redirects=True)
    res_admin = client.get('/admin/')
    assert res_admin.status_code == 200
    assert b'Clinical Platform Overview' in res_admin.data

def test_top_7_days_statistics(app):
    with app.app_context():
        user = User(user_id='stat_tester', name='Stat Tester', email='stats@test.com', phone='1234567890', location='Chicago', role='user')
        user.set_password('Pass123!')
        db.session.add(user)
        db.session.commit()

        # Run 2 disease predictions
        predict_disease(user=user, symptom_inputs=['itching', 'skin_rash'], save_history=True)
        predict_disease(user=user, symptom_inputs=['itching', 'skin_rash'], save_history=True)

        # Run 1 medicine prediction
        predict_medicine(user=user, disease_name='fungal infection', save_history=True)

        stats = get_admin_dashboard_stats()
        assert stats['total_users'] >= 1
        assert stats['total_predictions'] == 3
        assert len(stats['top_diseases_7days']) > 0
        assert stats['top_diseases_7days'][0]['disease'] == 'Fungal Infection'
        assert stats['top_diseases_7days'][0]['count'] == 2

        assert len(stats['top_medicines_7days']) > 0
        assert stats['top_medicines_7days'][0]['count'] >= 1

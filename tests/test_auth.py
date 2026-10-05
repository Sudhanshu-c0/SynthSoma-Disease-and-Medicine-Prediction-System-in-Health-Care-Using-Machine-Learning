import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.auth_service import register_user, authenticate_user

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

def test_register_and_authenticate(app):
    with app.app_context():
        form_data = {
            'name': 'Test Physician',
            'user_id': 'testdoc101',
            'email': 'testdoc@synthsoma.org',
            'phone': '1234567890',
            'location': 'New York, NY',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }
        success, errors, user = register_user(form_data)
        assert success is True
        assert user is not None
        assert user.user_id == 'testdoc101'
        assert user.role == 'user'
        assert user.check_password('Password123!') is True
        assert not user.check_password('WrongPass')

        # Test duplicate registration
        success2, errors2, user2 = register_user(form_data)
        assert success2 is False
        assert 'user_id' in errors2 or 'email' in errors2

        # Test authentication
        auth_user, err = authenticate_user('testdoc101', 'Password123!')
        assert auth_user is not None
        assert err is None

        # Test invalid password authentication
        bad_user, err = authenticate_user('testdoc101', 'WrongPassword!')
        assert bad_user is None
        assert err is not None

def test_auth_routes(client, app):
    # Test GET signup
    res = client.get('/signup')
    assert res.status_code == 200
    assert b'Create Your Account' in res.data

    # Test POST signup
    res = client.post('/signup', data={
        'name': 'Route User',
        'user_id': 'routeuser1',
        'email': 'route@example.com',
        'phone': '9876543210',
        'location': 'Chicago, IL',
        'password': 'SecurePass123!',
        'confirm_password': 'SecurePass123!'
    }, follow_redirects=True)
    assert res.status_code == 200

    # Test POST login
    login_res = client.post('/login', data={
        'username': 'routeuser1',
        'password': 'SecurePass123!'
    }, follow_redirects=True)
    assert login_res.status_code == 200
    assert b'Dashboard' in login_res.data

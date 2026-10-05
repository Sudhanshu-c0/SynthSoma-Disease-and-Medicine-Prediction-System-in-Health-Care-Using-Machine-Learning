import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.profile_service import update_profile, get_user_stats

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_profile_update(app):
    with app.app_context():
        user = User(
            user_id='prof_user',
            name='Original Name',
            email='prof@example.com',
            phone='1234567890',
            location='Original City'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        # Update profile
        success, errors = update_profile(user, {
            'name': 'Updated Name',
            'phone': '9876543210',
            'location': 'New City'
        })
        assert success is True
        assert user.name == 'Updated Name'
        assert user.location == 'New City'

        # Invalid phone
        success_bad, errors_bad = update_profile(user, {
            'name': 'Valid Name',
            'phone': '123',
            'location': 'City'
        })
        assert success_bad is False
        assert 'phone' in errors_bad

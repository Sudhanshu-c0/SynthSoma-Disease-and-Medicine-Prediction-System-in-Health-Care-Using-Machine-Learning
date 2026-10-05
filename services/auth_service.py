from models.database_models import User
from database.db import db
from utils.security import hash_password, verify_password, generate_reset_token
from utils.validators import validate_signup_form
from datetime import datetime
from flask import current_app

def register_user(form_data, role='user'):
    is_valid, errors = validate_signup_form(form_data)
    if not is_valid:
        return False, errors, None
        
    user_id = form_data.get('user_id').strip()
    email = form_data.get('email').strip().lower()
    
    # Check uniqueness
    if User.query.filter_by(user_id=user_id).first():
        return False, {'user_id': 'This User ID is already registered.'}, None
        
    if User.query.filter_by(email=email).first():
        return False, {'email': 'An account with this email address already exists.'}, None
        
    user = User(
        user_id=user_id,
        name=form_data.get('name').strip(),
        email=email,
        phone=form_data.get('phone').strip(),
        location=form_data.get('location').strip(),
        role=role
    )
    user.set_password(form_data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    return True, {}, user

def authenticate_user(username_or_email, password):
    if not username_or_email or not password:
        return None, "Please provide both User ID / Email and password."
        
    clean_identifier = username_or_email.strip()
    user = User.query.filter(
        (User.user_id == clean_identifier) | (User.email == clean_identifier.lower())
    ).first()
    
    if not user:
        return None, "Invalid User ID/Email or password."
        
    if not user.check_password(password):
        return None, "Invalid User ID/Email or password."
        
    return user, None

def seed_default_admin(app=None):
    """Ensure default admin account exists in database."""
    config = current_app.config if not app else app.config
    admin_id = config.get('ADMIN_USER_ID', 'admin')
    admin_email = config.get('ADMIN_EMAIL', 'admin@synthsoma.org').lower()
    admin_pass = config.get('ADMIN_PASSWORD', 'Admin@SynthSoma2026!')
    admin_name = config.get('ADMIN_NAME', 'SynthSoma System Administrator')
    admin_phone = config.get('ADMIN_PHONE', '+1-800-555-0199')
    admin_loc = config.get('ADMIN_LOCATION', 'Global Operations HQ')
    
    existing = User.query.filter((User.user_id == admin_id) | (User.email == admin_email)).first()
    if not existing:
        admin = User(
            user_id=admin_id,
            name=admin_name,
            email=admin_email,
            phone=admin_phone,
            location=admin_loc,
            role='admin'
        )
        admin.set_password(admin_pass)
        db.session.add(admin)
        db.session.commit()
        return admin
    else:
        # Ensure role is admin
        if existing.role != 'admin':
            existing.role = 'admin'
            db.session.commit()
        return existing

def request_password_reset(email):
    email = (email or '').strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, "No account found with this email address.", None
        
    token, expiry = generate_reset_token()
    user.reset_token = token
    user.reset_token_expiry = expiry
    db.session.commit()
    return True, "Password reset instructions have been generated.", token

def reset_password_with_token(token, new_password):
    if not token or not new_password:
        return False, "Invalid token or password."
        
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expiry:
        return False, "Invalid or expired reset token."
        
    if datetime.utcnow() > user.reset_token_expiry:
        return False, "This reset token has expired. Please request a new one."
        
    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()
    return True, "Your password has been reset successfully. You can now log in."

def change_password(user, current_password, new_password, confirm_password):
    if not user.check_password(current_password):
        return False, "Incorrect current password."
        
    if not new_password or len(new_password) < 6:
        return False, "New password must be at least 6 characters long."
        
    if new_password != confirm_password:
        return False, "New password and confirmation do not match."
        
    user.set_password(new_password)
    db.session.commit()
    return True, "Password changed successfully."

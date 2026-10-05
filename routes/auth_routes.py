from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import (
    register_user,
    authenticate_user,
    request_password_reset,
    reset_password_with_token
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
        
    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name'),
            'user_id': request.form.get('user_id'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'location': request.form.get('location'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password')
        }
        
        success, errors, user = register_user(form_data)
        if success:
            flash('Your account has been created successfully! Please log in to continue.', 'success')
            return redirect(url_for('auth.login'))
        else:
            for field, err in errors.items():
                flash(err, 'danger')
            return render_template('auth/signup.html', form=form_data, errors=errors)
            
    return render_template('auth/signup.html', form={}, errors={})

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
        
    if request.method == 'POST':
        identifier = request.form.get('username') or request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user, err = authenticate_user(identifier, password)
        if user:
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.name}!", 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(err, 'danger')
            return render_template('auth/login.html', identifier=identifier)
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        success, message, token = request_password_reset(email)
        if success:
            flash(f"{message} For testing/development, your reset link is: {url_for('auth.reset_password', token=token, _external=True)}", 'info')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
            
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash("Passwords do not match.", 'danger')
            return render_template('auth/reset_password.html', token=token)
            
        success, message = reset_password_with_token(token, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
            return render_template('auth/reset_password.html', token=token)
            
    return render_template('auth/reset_password.html', token=token)

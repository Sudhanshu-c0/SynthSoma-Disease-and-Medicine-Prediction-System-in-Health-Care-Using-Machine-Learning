from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.profile_service import update_profile, get_user_stats
from services.auth_service import change_password

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def view_profile():
    stats = get_user_stats(current_user.user_id)
    return render_template('profile/profile.html', user=current_user, stats=stats)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'location': request.form.get('location')
        }
        success, errors = update_profile(current_user, data)
        if success:
            flash("Your profile has been updated successfully!", "success")
            return redirect(url_for('profile.view_profile'))
        else:
            for field, err in errors.items():
                flash(err, "danger")
            return render_template('profile/edit_profile.html', user=current_user, form=data, errors=errors)
            
    return render_template('profile/edit_profile.html', user=current_user, form={}, errors={})

@profile_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_user_password():
    if request.method == 'POST':
        current_p = request.form.get('current_password')
        new_p = request.form.get('new_password')
        confirm_p = request.form.get('confirm_password')

        success, msg = change_password(current_user, current_p, new_p, confirm_p)
        if success:
            flash(msg, "success")
            return redirect(url_for('profile.view_profile'))
        else:
            flash(msg, "danger")
            return render_template('profile/change_password.html')

    return render_template('profile/change_password.html')

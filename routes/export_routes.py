from flask import Blueprint, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from services.csv_export_service import export_predictions_to_csv

export_bp = Blueprint('export', __name__, url_prefix='/export')

@export_bp.route('/csv/<module>')
@login_required
def export_csv(module):
    valid_modules = ['disease', 'medicine', 'precaution', 'risk_factor', 'history', 'all']
    if module not in valid_modules:
        flash("Invalid export module specified.", "danger")
        return redirect(url_for('history.history_index'))

    is_admin = current_user.is_admin
    csv_buffer, filename = export_predictions_to_csv(
        user=current_user,
        module=None if module in ['history', 'all'] else module,
        is_admin=False # Normal user export scope
    )

    return send_file(
        csv_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"{current_user.user_id}_{filename}"
    )

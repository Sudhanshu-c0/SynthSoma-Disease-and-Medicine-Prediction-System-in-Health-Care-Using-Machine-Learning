from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from utils.decorators import admin_required
from services.admin_service import (
    get_admin_dashboard_stats,
    get_all_users,
    get_module_predictions_admin
)
from services.history_service import get_admin_prediction_history
from services.csv_export_service import export_predictions_to_csv

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    stats = get_admin_dashboard_stats()
    recent_predictions, _ = get_admin_prediction_history(limit=10)
    return render_template(
        'admin/admin_dashboard.html',
        stats=stats,
        recent_predictions=recent_predictions
    )

@admin_bp.route('/users')
@admin_required
def user_details():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    role = request.args.get('role', 'all')
    limit = 20
    offset = (page - 1) * limit

    users, total = get_all_users(search=search, role=role, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return render_template(
        'admin/user_details.html',
        users=users,
        search=search,
        role=role,
        page=page,
        total_pages=total_pages,
        total=total
    )

@admin_bp.route('/predictions')
@admin_required
def user_predictions():
    page = request.args.get('page', 1, type=int)
    limit = 25
    offset = (page - 1) * limit
    
    filters = {
        'user_id': request.args.get('user_id', '').strip(),
        'module': request.args.get('module', 'all'),
        'search': request.args.get('search', '').strip(),
        'start_date': request.args.get('start_date', '').strip(),
        'end_date': request.args.get('end_date', '').strip()
    }

    predictions, total = get_admin_prediction_history(filters=filters, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return render_template(
        'admin/user_predictions.html',
        predictions=predictions,
        filters=filters,
        page=page,
        total_pages=total_pages,
        total=total
    )

@admin_bp.route('/top-diseases')
@admin_required
def top_predicted_diseases():
    stats = get_admin_dashboard_stats()
    return render_template('admin/top_predicted_diseases.html', top_diseases=stats['top_diseases_7days'])

@admin_bp.route('/top-medicines')
@admin_required
def top_predicted_medicines():
    stats = get_admin_dashboard_stats()
    return render_template('admin/top_predicted_medicines.html', top_medicines=stats['top_medicines_7days'])

@admin_bp.route('/predictions/disease')
@admin_required
def disease_predictions():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    limit = 25
    offset = (page - 1) * limit
    records, total = get_module_predictions_admin('disease', search=search, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('admin/disease_predictions.html', records=records, search=search, page=page, total_pages=total_pages, total=total)

@admin_bp.route('/predictions/medicine')
@admin_required
def medicine_predictions():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    limit = 25
    offset = (page - 1) * limit
    records, total = get_module_predictions_admin('medicine', search=search, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('admin/medicine_predictions.html', records=records, search=search, page=page, total_pages=total_pages, total=total)

@admin_bp.route('/predictions/precaution')
@admin_required
def precaution_predictions():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    limit = 25
    offset = (page - 1) * limit
    records, total = get_module_predictions_admin('precaution', search=search, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('admin/precaution_predictions.html', records=records, search=search, page=page, total_pages=total_pages, total=total)

@admin_bp.route('/predictions/risk-factor')
@admin_required
def risk_factor_predictions():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    limit = 25
    offset = (page - 1) * limit
    records, total = get_module_predictions_admin('risk_factor', search=search, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('admin/risk_factor_predictions.html', records=records, search=search, page=page, total_pages=total_pages, total=total)

@admin_bp.route('/export/csv/<module>')
@admin_required
def export_admin_csv(module):
    valid_modules = ['disease', 'medicine', 'precaution', 'risk_factor', 'all', 'history']
    if module not in valid_modules:
        flash("Invalid module for export.", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    csv_buffer, filename = export_predictions_to_csv(
        user=None,
        module=None if module in ['all', 'history'] else module,
        is_admin=True
    )

    return send_file(
        csv_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"admin_{filename}"
    )

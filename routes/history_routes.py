from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from services.history_service import get_user_history, get_module_specific_history

history_bp = Blueprint('history', __name__, url_prefix='/history')

@history_bp.route('/')
@login_required
def history_index():
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    module = request.args.get('module', 'all')
    
    predictions, total = get_user_history(current_user.user_id, module=module, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    
    return render_template(
        'history/history.html',
        predictions=predictions,
        active_module=module,
        page=page,
        total_pages=total_pages,
        total_records=total
    )

@history_bp.route('/disease')
@login_required
def disease_history():
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    records, total = get_module_specific_history(current_user.user_id, 'disease', limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('history/disease_history.html', records=records, page=page, total_pages=total_pages, total=total)

@history_bp.route('/medicine')
@login_required
def medicine_history():
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    records, total = get_module_specific_history(current_user.user_id, 'medicine', limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('history/medicine_history.html', records=records, page=page, total_pages=total_pages, total=total)

@history_bp.route('/precaution')
@login_required
def precaution_history():
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    records, total = get_module_specific_history(current_user.user_id, 'precaution', limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('history/precaution_history.html', records=records, page=page, total_pages=total_pages, total=total)

@history_bp.route('/risk-factor')
@login_required
def risk_factor_history():
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    records, total = get_module_specific_history(current_user.user_id, 'risk_factor', limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return render_template('history/risk_factor_history.html', records=records, page=page, total_pages=total_pages, total=total)

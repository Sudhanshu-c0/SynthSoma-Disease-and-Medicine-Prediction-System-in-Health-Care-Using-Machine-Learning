from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.profile_service import get_user_stats
from services.history_service import get_user_history

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    stats = get_user_stats(current_user.user_id)
    recent_history, _ = get_user_history(current_user.user_id, limit=5)
    return render_template(
        'dashboard/dashboard.html',
        stats=stats,
        recent_history=recent_history,
        user=current_user
    )

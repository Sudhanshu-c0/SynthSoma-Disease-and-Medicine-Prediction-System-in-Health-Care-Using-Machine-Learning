from flask import Blueprint, render_template, send_file, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from services.report_service import get_prediction_report_pdf
from services.history_service import get_user_history, get_prediction_by_id

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/')
@login_required
def report_list():
    predictions, total = get_user_history(current_user.user_id, limit=50)
    return render_template('reports/disease_report.html', predictions=predictions, total=total)

@report_bp.route('/download/<int:prediction_id>')
@login_required
def download_pdf(prediction_id):
    pdf_buffer, filename = get_prediction_report_pdf(prediction_id, current_user)
    if not pdf_buffer:
        flash("Report could not be generated or unauthorized access.", "danger")
        return redirect(url_for('history.history_index'))
        
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@report_bp.route('/view/<int:prediction_id>')
@login_required
def view_inline_pdf(prediction_id):
    pdf_buffer, filename = get_prediction_report_pdf(prediction_id, current_user)
    if not pdf_buffer:
        abort(404)
        
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=False,
        download_name=filename
    )

import io
import csv
from models.database_models import db, Prediction, DiseasePrediction, MedicinePrediction, PrecautionPrediction, RiskFactorPrediction, User

def export_predictions_to_csv(user=None, module=None, is_admin=False):
    """
    Generate CSV file buffer for predictions.
    If is_admin is False, only export records for `user`.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    if module == 'disease':
        writer.writerow(['Prediction ID', 'User ID', 'User Name', 'Selected Symptoms', 'Predicted Disease', 'Confidence', 'Model Used', 'Timestamp'])
        query = db.session.query(DiseasePrediction, User).join(User, DiseasePrediction.user_id == User.user_id)
        if not is_admin and user:
            query = query.filter(DiseasePrediction.user_id == user.user_id)
        rows = query.order_by(DiseasePrediction.created_at.desc()).all()
        for r, u in rows:
            writer.writerow([
                r.id,
                r.user_id,
                u.name if u else r.user_id,
                r.selected_symptoms,
                r.predicted_disease,
                f"{r.confidence * 100:.1f}%" if r.confidence is not None else 'N/A',
                r.model_used,
                r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
            ])

    elif module == 'medicine':
        writer.writerow(['Prediction ID', 'User ID', 'User Name', 'Disease Input', 'Predicted Medicines', 'Timestamp'])
        query = db.session.query(MedicinePrediction, User).join(User, MedicinePrediction.user_id == User.user_id)
        if not is_admin and user:
            query = query.filter(MedicinePrediction.user_id == user.user_id)
        rows = query.order_by(MedicinePrediction.created_at.desc()).all()
        for r, u in rows:
            writer.writerow([
                r.id,
                r.user_id,
                u.name if u else r.user_id,
                r.disease_input,
                r.predicted_medicines,
                r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
            ])

    elif module == 'precaution':
        writer.writerow(['Prediction ID', 'User ID', 'User Name', 'Disease Input', 'Recommended Precautions', 'Timestamp'])
        query = db.session.query(PrecautionPrediction, User).join(User, PrecautionPrediction.user_id == User.user_id)
        if not is_admin and user:
            query = query.filter(PrecautionPrediction.user_id == user.user_id)
        rows = query.order_by(PrecautionPrediction.created_at.desc()).all()
        for r, u in rows:
            writer.writerow([
                r.id,
                r.user_id,
                u.name if u else r.user_id,
                r.disease_input,
                r.precautions,
                r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
            ])

    elif module == 'risk_factor':
        writer.writerow(['Prediction ID', 'User ID', 'User Name', 'Disease Input', 'Matched Disease', 'Risk Factors', 'Occurrence', 'Timestamp'])
        query = db.session.query(RiskFactorPrediction, User).join(User, RiskFactorPrediction.user_id == User.user_id)
        if not is_admin and user:
            query = query.filter(RiskFactorPrediction.user_id == user.user_id)
        rows = query.order_by(RiskFactorPrediction.created_at.desc()).all()
        for r, u in rows:
            writer.writerow([
                r.id,
                r.user_id,
                u.name if u else r.user_id,
                r.disease_input,
                r.matched_disease,
                r.risk_factors,
                r.occurrence,
                r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
            ])

    else:
        # All prediction history
        writer.writerow(['Prediction ID', 'User ID', 'User Name', 'Email', 'Phone', 'Location', 'Module', 'Input Summary', 'Result Summary', 'Timestamp'])
        query = db.session.query(Prediction, User).join(User, Prediction.user_id == User.user_id)
        if not is_admin and user:
            query = query.filter(Prediction.user_id == user.user_id)
        rows = query.order_by(Prediction.created_at.desc()).all()
        for r, u in rows:
            writer.writerow([
                r.id,
                r.user_id,
                u.name if u else '',
                u.email if u else '',
                u.phone if u else '',
                u.location if u else '',
                r.module,
                r.input_summary,
                r.result_summary,
                r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
            ])

    output.seek(0)
    bytes_buffer = io.BytesIO(output.getvalue().encode('utf-8'))
    filename = f"synthsoma_{module or 'all_history'}_export.csv"
    return bytes_buffer, filename

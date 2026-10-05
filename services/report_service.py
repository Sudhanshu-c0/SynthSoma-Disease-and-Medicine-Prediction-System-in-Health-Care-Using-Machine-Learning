from services.pdf_service import generate_pdf_report
from services.history_service import get_prediction_by_id

def get_prediction_report_pdf(prediction_id, user):
    record = get_prediction_by_id(prediction_id, user)
    if not record:
        return None, None
        
    details = record.get_details()
    pdf_buffer = generate_pdf_report(user=record.user, module=record.module, prediction_record=record, details=details)
    filename = f"synthsoma_{record.module}_report_{record.id}.pdf"
    return pdf_buffer, filename

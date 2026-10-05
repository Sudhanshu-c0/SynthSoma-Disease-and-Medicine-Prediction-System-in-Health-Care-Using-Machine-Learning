from datetime import datetime

def format_datetime(dt, fmt='%b %d, %Y %I:%M %p'):
    if not dt:
        return 'N/A'
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except Exception:
            return dt
    return dt.strftime(fmt)

def clean_disease_name(name):
    if not name:
        return ''
    return str(name).strip().lower()

def title_case_disease(name):
    if not name:
        return ''
    return str(name).strip().title()

def get_medical_disclaimer():
    return (
        "Medical Disclaimer: SynthSoma is an academic and reference intelligence prototype designed "
        "for informational purposes only. It is not a substitute for professional medical diagnosis, "
        "treatment, or clinical judgment. Always consult a qualified healthcare professional regarding any "
        "health conditions, prescriptions, or medical decisions."
    )

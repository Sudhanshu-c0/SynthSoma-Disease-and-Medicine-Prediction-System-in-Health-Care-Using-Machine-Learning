import pytest
from app import create_app
from database.db import db
from models.database_models import User
from services.disease_prediction_service import predict_disease
from services.report_service import get_prediction_report_pdf

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_generate_pdf_report(app):
    with app.app_context():
        user = User(
            user_id='pdf_tester',
            name='Dr. PDF Tester',
            email='pdftest@synthsoma.org',
            phone='1234567890',
            location='Philadelphia, PA'
        )
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        # Run disease prediction
        res = predict_disease(user=user, symptom_inputs=['itching', 'skin_rash'], save_history=True)
        pred_id = res['id']

        pdf_buffer, filename = get_prediction_report_pdf(pred_id, user)
        assert pdf_buffer is not None
        assert filename.startswith('synthsoma_disease_report_')
        assert filename.endswith('.pdf')

        # Verify PDF header magic bytes %PDF
        pdf_bytes = pdf_buffer.read()
        assert len(pdf_bytes) > 500
        assert pdf_bytes.startswith(b'%PDF')

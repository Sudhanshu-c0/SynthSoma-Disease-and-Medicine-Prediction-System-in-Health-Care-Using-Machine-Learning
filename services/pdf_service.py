import io
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

def generate_pdf_report(user, module, prediction_record, details=None):
    """
    Generate professional healthcare PDF report for any of the 4 modules:
    'disease', 'medicine', 'precaution', 'risk_factor'
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    brand_teal = colors.HexColor('#0d9488')
    dark_slate = colors.HexColor('#1e293b')
    light_bg = colors.HexColor('#f8fafc')
    border_color = colors.HexColor('#cbd5e1')
    text_muted = colors.HexColor('#64748b')
    disclaimer_bg = colors.HexColor('#fef3c7')
    disclaimer_border = colors.HexColor('#f59e0b')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=brand_teal,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_muted,
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=dark_slate,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_slate
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=dark_slate
    )

    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#78350f')
    )

    elements = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>SYNTHSOMA</b><br/><font size=8 color='#0f766e'>CLINICAL REFERENCE INTELLIGENCE PLATFORM</font>", title_style),
            Paragraph(f"<b>REPORT ID:</b> #{prediction_record.id if hasattr(prediction_record, 'id') else 'N/A'}<br/><b>DATE:</b> {datetime.utcnow().strftime('%B %d, %Y')}<br/><b>TIME:</b> {datetime.utcnow().strftime('%H:%M:%S UTC')}", subtitle_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[3.8 * inch, 3.2 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=1.5, color=brand_teal, spaceBefore=4, spaceAfter=10))

    # 2. User & Module Metadata Card
    user_name = user.name if user else 'Anonymous Patient'
    user_id = user.user_id if user else 'N/A'
    user_email = user.email if user else 'N/A'
    user_loc = user.location if user else 'N/A'
    module_title = module.replace('_', ' ').title() + " Module Report"

    meta_table_data = [
        [
            Paragraph("<b>Patient / User:</b>", bold_label),
            Paragraph(user_name, body_style),
            Paragraph("<b>Module:</b>", bold_label),
            Paragraph(module_title, body_style)
        ],
        [
            Paragraph("<b>User ID:</b>", bold_label),
            Paragraph(user_id, body_style),
            Paragraph("<b>Email:</b>", bold_label),
            Paragraph(user_email, body_style)
        ],
        [
            Paragraph("<b>Location:</b>", bold_label),
            Paragraph(user_loc, body_style),
            Paragraph("<b>Timestamp:</b>", bold_label),
            Paragraph(prediction_record.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(prediction_record, 'created_at') and prediction_record.created_at else 'Current Session', body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[1.1 * inch, 2.4 * inch, 1.1 * inch, 2.4 * inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 10))

    # Parse details dictionary
    data_dict = details or {}
    if not data_dict and hasattr(prediction_record, 'get_details'):
        data_dict = prediction_record.get_details()

    # 3. Input & Primary Result
    elements.append(Paragraph("1. Assessment Input & Output", h2_style))
    
    input_str = prediction_record.input_summary if hasattr(prediction_record, 'input_summary') else str(data_dict.get('selected_symptoms') or data_dict.get('disease_input'))
    result_str = prediction_record.result_summary if hasattr(prediction_record, 'result_summary') else str(data_dict.get('predicted_disease') or data_dict.get('matched_disease'))

    result_rows = [
        [Paragraph("<b>Submitted Clinical Input:</b>", bold_label), Paragraph(input_str, body_style)],
        [Paragraph("<b>Primary ML Result:</b>", bold_label), Paragraph(f"<b><font color='#0d9488'>{result_str}</font></b>", body_style)],
    ]

    if 'confidence_percentage' in data_dict and data_dict['confidence_percentage']:
        result_rows.append([Paragraph("<b>Confidence Level:</b>", bold_label), Paragraph(data_dict['confidence_percentage'], body_style)])
    if 'model_used' in data_dict and data_dict['model_used']:
        result_rows.append([Paragraph("<b>Model Architecture:</b>", bold_label), Paragraph(data_dict['model_used'], body_style)])

    res_table = Table(result_rows, colWidths=[2.2 * inch, 4.8 * inch])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(res_table)
    elements.append(Spacer(1, 10))

    # 4. Module Specific Detailed Tables
    if module == 'disease':
        elements.append(Paragraph("2. Clinical Supporting Intelligence", h2_style))
        precautions = data_dict.get('precautions', [])
        risk_factors = data_dict.get('risk_factors', [])
        occurrence = data_dict.get('occurrence_frequency', 'N/A')
        medicines = data_dict.get('reference_medicines', [])

        supp_data = [
            [Paragraph("<b>Occurrence / Epidemiology:</b>", bold_label), Paragraph(occurrence, body_style)],
            [Paragraph("<b>Recommended Precautions:</b>", bold_label), Paragraph(' • ' + '<br/> • '.join(precautions) if precautions else 'No specific precaution records', body_style)],
            [Paragraph("<b>Known Risk Factors:</b>", bold_label), Paragraph(', '.join(risk_factors) if risk_factors else 'Standard baseline clinical risk', body_style)],
            [Paragraph("<b>Reference Medicines:</b>", bold_label), Paragraph(', '.join(medicines) if medicines else 'Consult medical specialist', body_style)]
        ]
        supp_table = Table(supp_data, colWidths=[2.2 * inch, 4.8 * inch])
        supp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), light_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(supp_table)

    elif module == 'medicine':
        elements.append(Paragraph("2. Reference Pharmaceutical Formulation Catalog", h2_style))
        meds = data_dict.get('medicines', [])
        med_rows = [[Paragraph("<b>Medicine Name</b>", bold_label), Paragraph("<b>Composition</b>", bold_label), Paragraph("<b>Clinical Description</b>", bold_label)]]
        
        if meds:
            for m in meds:
                med_rows.append([
                    Paragraph(m.get('name', 'N/A'), bold_label),
                    Paragraph(m.get('composition', 'N/A'), body_style),
                    Paragraph(m.get('description', 'N/A'), body_style)
                ])
        else:
            med_rows.append([Paragraph("No reference medicines predicted", body_style), Paragraph("-", body_style), Paragraph("-", body_style)])

        med_table = Table(med_rows, colWidths=[2.0 * inch, 2.5 * inch, 2.5 * inch])
        med_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), brand_teal),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(med_table)

    elif module == 'precaution':
        elements.append(Paragraph("2. Recommended Clinical & Lifestyle Precautions", h2_style))
        precs = data_dict.get('precautions', [])
        prec_rows = []
        if precs:
            for idx, p in enumerate(precs, 1):
                prec_rows.append([Paragraph(f"<b>{idx}.</b>", bold_label), Paragraph(p, body_style)])
        else:
            prec_rows.append([Paragraph("-", bold_label), Paragraph("Standard clinical observation recommended.", body_style)])
            
        p_table = Table(prec_rows, colWidths=[0.5 * inch, 6.5 * inch])
        p_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(p_table)

    elif module == 'risk_factor':
        elements.append(Paragraph("2. Risk Profile & Epidemiological Characteristics", h2_style))
        rfs = data_dict.get('risk_factors', [])
        occur = data_dict.get('occurrence_frequency', 'N/A')
        clinical = data_dict.get('clinical_note', '')
        
        rf_rows = [
            [Paragraph("<b>Matched Disease:</b>", bold_label), Paragraph(data_dict.get('matched_disease', 'N/A'), body_style)],
            [Paragraph("<b>Occurrence Frequency:</b>", bold_label), Paragraph(occur, body_style)],
            [Paragraph("<b>Identified Risk Factors:</b>", bold_label), Paragraph(' • ' + '<br/> • '.join(rfs) if rfs else 'General baseline', body_style)],
            [Paragraph("<b>Clinical Notes:</b>", bold_label), Paragraph(clinical if clinical else 'Follow standard preventative measures', body_style)]
        ]
        rf_table = Table(rf_rows, colWidths=[2.0 * inch, 5.0 * inch])
        rf_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(rf_table)

    elements.append(Spacer(1, 15))

    # 5. Mandatory Medical Disclaimer Box
    disclaimer_p = Paragraph(
        "<b>MANDATORY MEDICAL DISCLAIMER:</b><br/>"
        "This system is intended for educational and informational purposes only. It is not a substitute for professional "
        "medical diagnosis, treatment, or clinical advice. Never disregard professional medical advice or delay seeking it "
        "because of information contained in this report. This document does not constitute a valid prescription or clinical treatment regimen.",
        disclaimer_style
    )
    disclaimer_table = Table([[disclaimer_p]], colWidths=[7.0 * inch])
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), disclaimer_bg),
        ('BOX', (0, 0), (-1, -1), 1, disclaimer_border),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(disclaimer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

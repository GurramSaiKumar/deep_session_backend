import io
from datetime import datetime
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_focus_report_pdf(user, sessions, report_date):
    """
    Generate a daily focus report PDF for the given user and sessions.
    Returns a bytes object representing the PDF file.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph(f"Daily ddyaan Report - {user.name}", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Date
    date_str = report_date.strftime("%B %d, %Y")
    elements.append(Paragraph(f"Report for: {date_str}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # If no sessions
    if not sessions:
        elements.append(Paragraph("No focus sessions recorded today.", styles["Normal"]))
    else:
        # Prepare data table
        data = [["Start Time", "End Time", "Duration (mins)", "Goal", "Status"]]
        for session in sessions:
            duration = round((session.end_time - session.start_time).total_seconds() / 60)
            data.append([
                session.start_time.strftime("%H:%M"),
                session.end_time.strftime("%H:%M"),
                duration,
                session.goal or "-",
                session.status or "Completed"
            ])

        table = Table(data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def send_focus_report_email(user, pdf_bytes, report_date):
    """
    Send the generated PDF report to the user via email.
    """
    subject = f"Your Daily ddyaan Report - {report_date.strftime('%B %d, %Y')}"
    body = (
        f"Hi {user.name},\n\n"
        "Here’s your ddyaan summary report. Keep up the great work!\n\n"
        "Stay consistent 💪,\nddyaan App Team"
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email="no-reply@ddyaanapp.com",
        to=[user.email],
    )

    # Attach PDF
    email.attach(
        filename=f"ddyaan_report_{report_date.strftime('%Y%m%d')}.pdf",
        content=pdf_bytes,
        mimetype="application/pdf"
    )

    email.send()

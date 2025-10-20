# focus/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import FocusSession
from deepSessionBackend.login.models import User
from .utils import generate_focus_report_pdf, send_focus_report_email
from datetime import date, timedelta


@shared_task
def generate_daily_focus_reports():
    """
    Generate and email focus reports for all active users.
    """
    report_date = date.today() - timedelta(days=1)  # Get yesterday's date
    users = User.objects.filter(is_deleted=False)

    for user in users:
        sessions = FocusSession.objects.filter(
            user=user,
            start_time__date=report_date
        )
        pdf_bytes = generate_focus_report_pdf(user, sessions, report_date)
        send_focus_report_email(user, pdf_bytes, report_date)

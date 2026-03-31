"""Dealix - Email Worker Tasks"""
import logging
from app.extensions import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="send_email", max_retries=3, default_retry_delay=60)
def send_email_task(to: str, subject: str, body: str, html: str = None):
    """إرسال بريد إلكتروني واحد"""
    logger.info(f"Sending email to {to}: {subject}")
    # TODO: تنفيذ الإرسال الفعلي عبر SMTP
    return {"status": "queued", "to": to, "subject": subject}


@celery_app.task(name="send_bulk_email", max_retries=3, default_retry_delay=120)
def send_bulk_email_task(recipients: list, subject: str, body: str, html: str = None):
    """إرسال بريد إلكتروني جماعي"""
    logger.info(f"Sending bulk email to {len(recipients)} recipients")
    results = []
    for email in recipients:
        send_email_task.delay(email, subject, body, html)
        results.append({"to": email, "status": "queued"})
    return {"total": len(recipients), "results": results}

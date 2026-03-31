from celery import Celery
from ..core.config import settings
celery = Celery("dealix", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery.conf.update(task_serializer="json", timezone="Asia/Riyadh", enable_utc=True)
@celery.task
def send_reminder(lead_id: int, channel: str):
    return {"status": "sent", "lead_id": lead_id}
@celery.task
def check_stale_leads():
    return {"status": "checked"}

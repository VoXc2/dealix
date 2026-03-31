"""
Dealix - التمديدات المشتركة
"""
from celery import Celery
from redis import asyncio as aioredis

from app.core.config import settings

# Celery
celery_app = Celery(
    "dealix",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.DEFAULT_TIMEZONE,
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_soft_time_limit=300,
    task_time_limit=360,
)

# Redis async
redis_client: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis:
    """تهيئة اتصال Redis"""
    global redis_client
    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=50,
    )
    return redis_client


async def close_redis() -> None:
    """إغلاق اتصال Redis"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


def get_redis() -> aioredis.Redis:
    """الحصول على عميل Redis"""
    if redis_client is None:
        raise RuntimeError("Redis غير مهيأ - اتصل بـ init_redis() أولاً")
    return redis_client

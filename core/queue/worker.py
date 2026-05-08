"""
ARQ Worker Configuration — async Redis task queue for background LLM processing.
إعداد عامل ARQ — طابور مهام Redis غير متزامن لمعالجة النماذج اللغوية في الخلفية.

Run the worker with:
    python -m arq core.queue.worker.WorkerSettings

Or from project root:
    arq core.queue.worker.WorkerSettings
"""

from __future__ import annotations

import logging
from typing import Any

from arq.connections import RedisSettings

from core.queue.tasks import run_agent_job
from core.config.settings import get_settings

logger = logging.getLogger(__name__)


async def startup(ctx: dict[str, Any]) -> None:
    """Worker startup hook — initialise shared resources."""
    logger.info("arq_worker_startup")
    # Pre-warm the LLM router singleton so the first job doesn't pay init cost.
    from core.llm import get_router
    ctx["router"] = get_router()


async def shutdown(ctx: dict[str, Any]) -> None:
    """Worker shutdown hook — clean up connections."""
    logger.info("arq_worker_shutdown")


class WorkerSettings:
    """
    ARQ worker settings.
    All timeout / retry / backoff values follow ARQ conventions.

    Retry strategy: exponential backoff — ARQ retries are triggered by
    raising ``arq.Abort`` (permanent failure) or any exception (retryable).
    """

    # ── Task registry ────────────────────────────────────────────
    functions = [run_agent_job]

    # ── Concurrency ──────────────────────────────────────────────
    max_jobs: int = 10  # concurrent jobs per worker process

    # ── Timeouts ─────────────────────────────────────────────────
    job_timeout: int = 300          # 5 min — hard limit per job
    keep_result: int = 3_600        # 1 h  — keep completed job result in Redis
    keep_result_forever: bool = False

    # ── Retry / backoff ──────────────────────────────────────────
    max_tries: int = 3              # total attempts (1 original + 2 retries)
    retry_jobs: bool = True
    # ARQ uses exponential back-off: delay = attempt² seconds
    # attempt 1 → 1 s, attempt 2 → 4 s, attempt 3 → 9 s

    # ── Queue ────────────────────────────────────────────────────
    queue_name: str = "dealix:arq:default"

    # ── Polling interval (seconds) ───────────────────────────────
    poll_delay: float = 0.5         # how often worker checks Redis for new jobs

    # ── Lifecycle hooks ──────────────────────────────────────────
    on_startup = startup
    on_shutdown = shutdown

    # ── Redis connection ─────────────────────────────────────────
    @classmethod
    def redis_settings(cls) -> RedisSettings:
        """Pull Redis URL from app settings."""
        settings = get_settings()
        return RedisSettings.from_dsn(settings.redis_url)

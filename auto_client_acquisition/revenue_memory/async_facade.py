"""
Async facade for appending RevenueEvents from FastAPI async routes.

Dual-write when backend is postgres:
  1. Always append to the in-memory singleton (keeps sync replay helpers working).
  2. Await Postgres append for durability.

Orchestrator paths stay on sync ``InMemoryEventStore`` only (see revenue_os router).
"""

from __future__ import annotations

import logging

from auto_client_acquisition.revenue_memory.event_store import (
    get_default_store,
    get_postgres_store,
)
from auto_client_acquisition.revenue_memory.events import RevenueEvent
from core.config.settings import get_settings

log = logging.getLogger(__name__)


async def append_revenue_event(event: RevenueEvent) -> None:
    """Append one event: memory always; postgres additionally when configured."""
    settings = get_settings()
    mem = get_default_store("memory")
    mem.append(event)

    if settings.revenue_memory_backend != "postgres":
        return

    try:
        pg = get_postgres_store()
        await pg.append(event)
    except Exception:
        log.exception(
            "revenue_memory_postgres_append_failed",
            extra={"event_id": event.event_id, "event_type": event.event_type},
        )
        raise

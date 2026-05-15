"""Shared read helpers for ``org_consciousness_os``.

Keeps the per-system component files thin and consistent.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

from auto_client_acquisition.revenue_memory.event_store import (
    EventStore,
    get_default_store,
)
from auto_client_acquisition.revenue_memory.events import RevenueEvent

AGENT_ACTION_EVENT_TYPES: tuple[str, ...] = (
    "agent.action_requested",
    "agent.action_approved",
    "agent.action_rejected",
    "agent.action_executed",
    "agent.action_failed",
)


def utcnow_naive() -> datetime:
    """Naive UTC ``now`` — matches how ``RevenueEvent.occurred_at`` is stored."""
    return datetime.now(UTC).replace(tzinfo=None)


def read_agent_events(
    *,
    customer_id: str,
    window_days: int,
    store: EventStore | None = None,
    event_types: tuple[str, ...] = AGENT_ACTION_EVENT_TYPES,
) -> list[RevenueEvent]:
    """Read agent-action events for ``customer_id`` within ``window_days``.

    Read-only. Returns an explicit list (never swallows an empty store).
    """
    s = store or get_default_store()
    since = utcnow_naive() - timedelta(days=window_days)
    return list(s.read_for_customer(customer_id, since=since, event_types=event_types))

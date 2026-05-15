"""Support SLA monitor — find tickets whose SLA has been breached.

Used by the Daily Executive Pack (Phase 8) to surface overdue tickets.
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.support_inbox.state_store import _INDEX
from auto_client_acquisition.support_os.ticket import Ticket


def find_breached_tickets(
    *,
    customer_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return all tickets where sla_due_at < now and status not terminal."""
    now = datetime.now(UTC)
    out: list[dict[str, Any]] = []
    for t in _INDEX.values():
        if customer_id and t.customer_id != customer_id:
            continue
        if t.status in ("resolved", "closed"):
            continue
        if t.sla_due_at < now:
            out.append({
                "ticket_id": t.id,
                "customer_id": t.customer_id,
                "category": t.category,
                "priority": t.priority,
                "status": t.status,
                "minutes_overdue": int((now - t.sla_due_at).total_seconds() // 60),
            })
    return sorted(out, key=lambda x: x["minutes_overdue"], reverse=True)

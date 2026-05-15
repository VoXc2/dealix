"""Value ledger events (cross-package stable import path: ``value_os``).

In-memory MVP store. Tier discipline (enforced in :func:`add_event`):

* ``verified`` requires a ``source_ref``.
* ``client_confirmed`` requires both ``source_ref`` and ``confirmation_ref``.

``estimated`` and ``observed`` are never auto-promoted to a higher tier.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

VALID_TIERS = ("estimated", "observed", "verified", "client_confirmed")


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier sourcing discipline."""


@dataclass
class ValueEvent:
    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    occurred_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_LEDGER: dict[str, list[ValueEvent]] = {}
_LOCK = threading.Lock()


def add_event(
    *,
    customer_id: str,
    kind: str,
    tier: str,
    amount: float = 0.0,
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    """Append a value event after enforcing tier sourcing discipline."""
    if tier not in VALID_TIERS:
        raise ValueDisciplineError(f"unknown tier: {tier!r}")
    if tier in ("verified", "client_confirmed") and not source_ref.strip():
        raise ValueDisciplineError(f"tier {tier!r} requires source_ref")
    if tier == "client_confirmed" and not confirmation_ref.strip():
        raise ValueDisciplineError("tier 'client_confirmed' requires confirmation_ref")

    event = ValueEvent(
        customer_id=customer_id,
        kind=kind,
        amount=float(amount),
        tier=tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
        notes=notes,
    )
    with _LOCK:
        _LEDGER.setdefault(customer_id, []).append(event)
    return event


def list_events(*, customer_id: str) -> list[ValueEvent]:
    """Return all value events recorded for ``customer_id``."""
    with _LOCK:
        return list(_LEDGER.get(customer_id, []))


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    """Aggregate a customer's value events per tier within a trailing window."""
    cutoff = datetime.now(UTC) - timedelta(days=period_days)
    summary: dict[str, Any] = {
        tier: {"count": 0, "total_amount": 0.0} for tier in VALID_TIERS
    }
    for event in list_events(customer_id=customer_id):
        try:
            occurred = datetime.fromisoformat(event.occurred_at)
        except ValueError:
            continue
        if occurred.tzinfo is None:
            occurred = occurred.replace(tzinfo=UTC)
        if occurred < cutoff:
            continue
        bucket = summary.setdefault(event.tier, {"count": 0, "total_amount": 0.0})
        bucket["count"] += 1
        bucket["total_amount"] += event.amount
    return summary


def clear_for_test(customer_id: str) -> None:
    """Drop a customer's events. Test-support only."""
    with _LOCK:
        _LEDGER.pop(customer_id, None)


__all__ = [
    "VALID_TIERS",
    "ValueDisciplineError",
    "ValueEvent",
    "ValueLedgerEvent",
    "add_event",
    "clear_for_test",
    "list_events",
    "summarize",
    "value_ledger_event_valid",
]

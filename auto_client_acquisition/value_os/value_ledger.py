"""Value ledger — tier-disciplined value events per customer.

Two surfaces live here:

  * ``ValueLedgerEvent`` — the canonical auditable value event, re-exported
    from ``proof_architecture_os`` for the stable ``value_os`` import path.
  * ``ValueEvent`` + ``add_event`` / ``list_events`` — a lightweight,
    in-memory, tier-disciplined event store consumed by the Value OS router
    and the Monthly Value Report.

Tier discipline (mirrors the Value OS doctrine — Estimated value is not
Verified value):

  * ``estimated``        — projection; no reference required.
  * ``observed``         — seen in-workflow; no reference required.
  * ``verified``         — requires a ``source_ref``.
  * ``client_confirmed`` — requires both a ``source_ref`` and a
    ``confirmation_ref``.

A tier outside this set, or a missing required reference, raises
``ValueDisciplineError`` — callers map it to HTTP 422.
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

VALID_TIERS: frozenset[str] = frozenset(
    {"estimated", "observed", "verified", "client_confirmed"},
)


class ValueDisciplineError(ValueError):
    """Raised when an event violates value-tier discipline."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    """A single value event, scoped to a customer and a discipline tier."""

    value_event_id: str
    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    occurred_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# In-memory ledger — customer_id -> append-only list of events.
_LEDGER: dict[str, list[ValueEvent]] = {}


def _validate_tier_discipline(
    tier: str,
    source_ref: str,
    confirmation_ref: str,
) -> None:
    if tier not in VALID_TIERS:
        msg = f"invalid_tier: {tier!r} (allowed: {sorted(VALID_TIERS)})"
        raise ValueDisciplineError(msg)
    if tier == "verified" and not source_ref.strip():
        raise ValueDisciplineError("verified_tier_requires_source_ref")
    if tier == "client_confirmed" and not (
        source_ref.strip() and confirmation_ref.strip()
    ):
        raise ValueDisciplineError(
            "client_confirmed_tier_requires_source_ref_and_confirmation_ref",
        )


def add_event(
    *,
    customer_id: str,
    kind: str,
    amount: float = 0.0,
    tier: str,
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    """Append a value event after enforcing tier discipline.

    Raises ``ValueDisciplineError`` if the tier is unknown or a required
    reference is missing.
    """
    tier = tier.strip().lower()
    _validate_tier_discipline(tier, source_ref, confirmation_ref)
    event = ValueEvent(
        value_event_id=f"ve_{uuid.uuid4().hex[:16]}",
        customer_id=customer_id,
        kind=kind,
        amount=float(amount),
        tier=tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
        notes=notes,
    )
    _LEDGER.setdefault(customer_id, []).append(event)
    return event


def list_events(*, customer_id: str) -> list[ValueEvent]:
    """Return all value events recorded for a customer (append order)."""
    return list(_LEDGER.get(customer_id, []))


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    """Aggregate a customer's recent value events by tier.

    Tiers are never auto-promoted — estimated value stays estimated. Each
    tier key maps to its event count and total amount inside the window.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=period_days)
    summary: dict[str, Any] = {
        tier: {"count": 0, "total_amount": 0.0} for tier in sorted(VALID_TIERS)
    }
    for event in _LEDGER.get(customer_id, []):
        try:
            occurred = datetime.fromisoformat(event.occurred_at)
        except ValueError:
            continue
        if occurred.tzinfo is None:
            occurred = occurred.replace(tzinfo=timezone.utc)
        if occurred < cutoff:
            continue
        bucket = summary[event.tier]
        bucket["count"] += 1
        bucket["total_amount"] += event.amount
    return summary


def clear_for_test(customer_id: str) -> None:
    """Drop one customer's events from the in-memory ledger (test isolation)."""
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

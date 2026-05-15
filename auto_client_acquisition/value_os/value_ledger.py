"""Value ledger — auditable, tier-disciplined value events per customer.

Tier discipline (doctrine):
- ``estimated`` / ``observed``  → accepted without external refs.
- ``verified``                 → requires ``source_ref``.
- ``client_confirmed``         → requires BOTH ``source_ref`` and
                                 ``confirmation_ref``.

Estimated value is never auto-promoted to a higher tier. Storage is a
tenant-scoped JSONL file (``DEALIX_VALUE_LEDGER_PATH``), mirroring the
friction-log store.

The structural ``ValueLedgerEvent`` contract from ``proof_architecture_os``
is re-exported for callers that need the cross-package stable import path.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_VALID_TIERS = ("estimated", "observed", "verified", "client_confirmed")
_DEFAULT_PATH = "var/value-ledger.jsonl"
_lock = threading.Lock()


class ValueDisciplineError(ValueError):
    """Raised when an event violates value-tier evidence discipline."""


@dataclass(slots=True)
class ValueEvent:
    """A single recorded value event for a customer."""

    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    value_event_id: str = field(default_factory=lambda: f"val_{uuid.uuid4().hex[:12]}")
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _enforce_discipline(tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier not in _VALID_TIERS:
        raise ValueDisciplineError(f"unknown value tier {tier!r}; expected one of {_VALID_TIERS}")
    if tier == "verified" and not source_ref.strip():
        raise ValueDisciplineError("verified tier requires a non-empty source_ref")
    if tier == "client_confirmed" and not (source_ref.strip() and confirmation_ref.strip()):
        raise ValueDisciplineError(
            "client_confirmed tier requires both source_ref and confirmation_ref"
        )


def add_event(
    *,
    customer_id: str,
    kind: str,
    amount: float,
    tier: str,
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    """Record a value event after enforcing tier discipline."""
    if not customer_id:
        raise ValueError("customer_id is required")
    _enforce_discipline(tier, source_ref, confirmation_ref)
    event = ValueEvent(
        customer_id=customer_id,
        kind=kind,
        amount=float(amount),
        tier=tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
        notes=notes,
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def _read_all() -> list[ValueEvent]:
    path = _path()
    if not path.exists():
        return []
    out: list[ValueEvent] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(ValueEvent(**json.loads(line)))
            except Exception:  # noqa: S112 — skip a corrupt ledger line
                continue
    return out


def list_events(*, customer_id: str) -> list[ValueEvent]:
    """All recorded value events for a customer (newest insertion order)."""
    if not customer_id:
        return []
    return [e for e in _read_all() if e.customer_id == customer_id]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    """Aggregate a customer's value events by tier within a time window.

    Estimated value is reported as-is and never promoted to a higher tier.
    """
    cutoff = datetime.now(UTC) - timedelta(days=period_days)
    by_tier: dict[str, dict[str, Any]] = {
        t: {"count": 0, "total_amount": 0.0} for t in _VALID_TIERS
    }
    total = 0
    for ev in list_events(customer_id=customer_id):
        try:
            ts = datetime.fromisoformat(ev.occurred_at)
        except ValueError:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        if ts < cutoff:
            continue
        bucket = by_tier.setdefault(ev.tier, {"count": 0, "total_amount": 0.0})
        bucket["count"] += 1
        bucket["total_amount"] = round(bucket["total_amount"] + ev.amount, 2)
        total += 1
    return {
        "customer_id": customer_id,
        "period_days": period_days,
        "total_events": total,
        **by_tier,
    }


def clear_for_test(customer_id: str) -> None:
    """Remove a single customer's events — test isolation helper."""
    remaining = [e for e in _read_all() if e.customer_id != customer_id]
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("w", encoding="utf-8") as f:
        for e in remaining:
            f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")


__all__ = [
    "ValueDisciplineError",
    "ValueEvent",
    "ValueLedgerEvent",
    "add_event",
    "clear_for_test",
    "list_events",
    "summarize",
    "value_ledger_event_valid",
]

"""Value ledger — auditable, tier-disciplined value events per customer.

سجل القيمة — أحداث قيمة مُدقَّقة ومنضبطة الطبقات لكل عميل.

Tier discipline (doctrine — no fake proof):
  * ``verified`` requires a ``source_ref``.
  * ``client_confirmed`` requires both ``source_ref`` and ``confirmation_ref``.

Also re-exports ``ValueLedgerEvent`` / ``value_ledger_event_valid`` from
``proof_architecture_os`` so ``value_os`` remains the stable canonical path.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

VALUE_TIERS: tuple[str, ...] = ("estimated", "observed", "verified", "client_confirmed")

_DEFAULT_PATH = "var/value-ledger.jsonl"
_lock = threading.Lock()


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier-discipline rules."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    """One auditable value event, scoped to a customer."""

    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    value_event_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    occurred_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _read_raw() -> list[ValueEvent]:
    """Read every persisted value event. Caller holds ``_lock``."""
    path = _path()
    if not path.exists():
        return []
    out: list[ValueEvent] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(ValueEvent(**json.loads(line)))
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
    return out


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
    """Append a tier-disciplined value event for a customer.

    Raises ``ValueDisciplineError`` for an unknown tier, or when a
    ``verified`` / ``client_confirmed`` event lacks its required references.
    """
    if not customer_id:
        raise ValueDisciplineError("customer_id is required")
    if tier not in VALUE_TIERS:
        raise ValueDisciplineError(f"unknown value tier: {tier}")
    if tier == "verified" and not source_ref.strip():
        raise ValueDisciplineError("verified tier requires a source_ref")
    if tier == "client_confirmed" and not (
        source_ref.strip() and confirmation_ref.strip()
    ):
        raise ValueDisciplineError(
            "client_confirmed tier requires both source_ref and confirmation_ref"
        )
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


def list_events(*, customer_id: str) -> list[ValueEvent]:
    """Every value event for a customer (newest-last, no time filter)."""
    if not customer_id:
        return []
    with _lock:
        events = _read_raw()
    return [e for e in events if e.customer_id == customer_id]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    """Per-tier value totals for a customer within the trailing window.

    Estimated value is never auto-promoted to a higher tier — each event
    keeps the tier it was recorded with.
    """
    cutoff = datetime.now(UTC) - timedelta(days=period_days)
    totals: dict[str, float] = dict.fromkeys(VALUE_TIERS, 0.0)
    counts: dict[str, int] = dict.fromkeys(VALUE_TIERS, 0)
    for event in list_events(customer_id=customer_id):
        try:
            occurred = datetime.fromisoformat(event.occurred_at)
        except ValueError:
            continue
        if occurred.tzinfo is None:
            occurred = occurred.replace(tzinfo=UTC)
        if occurred < cutoff:
            continue
        if event.tier in totals:
            totals[event.tier] += event.amount
            counts[event.tier] += 1
    return {
        **{tier: totals[tier] for tier in VALUE_TIERS},
        "counts": counts,
        "customer_id": customer_id,
        "period_days": period_days,
    }


def clear_for_test(customer_id: str | None = None) -> None:
    """Test helper — drop one customer's events, or the whole ledger."""
    path = _path()
    if not path.exists():
        return
    with _lock:
        if customer_id is None:
            path.write_text("", encoding="utf-8")
            return
        kept = [e for e in _read_raw() if e.customer_id != customer_id]
        with path.open("w", encoding="utf-8") as f:
            for event in kept:
                f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")


__all__ = [
    "VALUE_TIERS",
    "ValueDisciplineError",
    "ValueEvent",
    "ValueLedgerEvent",
    "add_event",
    "clear_for_test",
    "list_events",
    "summarize",
    "value_ledger_event_valid",
]

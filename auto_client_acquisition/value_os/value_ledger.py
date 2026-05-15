"""Value ledger — auditable, tier-disciplined value events.

Cross-package stable import path: ``value_os``.

Tier discipline (doctrine):
  * ``estimated``        — no source required (range; not claimable externally)
  * ``observed``         — requires ``source_ref`` (measured in workflow)
  * ``verified``         — requires ``source_ref``
  * ``client_confirmed`` — requires both ``source_ref`` and ``confirmation_ref``

Persistence: append-only JSONL at ``DEALIX_VALUE_LEDGER_PATH`` (dev fallback).
Every operational event carries ``tenant_id`` for enterprise isolation.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Re-exported for backwards-compatible imports (value_os.__init__).
from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_DEFAULT_PATH = "var/value-ledger.jsonl"
_DEFAULT_TENANT = "default"
_VALID_TIERS = ("estimated", "observed", "verified", "client_confirmed")
_lock = threading.Lock()


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier sourcing discipline."""


@dataclass(slots=True)
class ValueEvent:
    customer_id: str
    kind: str
    amount: float
    tier: str
    tenant_id: str = _DEFAULT_TENANT
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
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


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _enforce_discipline(
    *, tier: str, source_ref: str, confirmation_ref: str
) -> None:
    if tier not in _VALID_TIERS:
        raise ValueDisciplineError(
            f"unknown value tier '{tier}'; expected one of {_VALID_TIERS}"
        )
    if tier in ("observed", "verified", "client_confirmed") and not source_ref.strip():
        raise ValueDisciplineError(
            f"tier '{tier}' is a measured tier and requires a non-empty source_ref"
        )
    if tier == "client_confirmed" and not confirmation_ref.strip():
        raise ValueDisciplineError(
            "tier 'client_confirmed' requires a non-empty confirmation_ref"
        )


def add_event(
    *,
    customer_id: str,
    kind: str,
    amount: float,
    tier: str,
    tenant_id: str = _DEFAULT_TENANT,
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    if not customer_id:
        raise ValueDisciplineError("customer_id is required")
    _enforce_discipline(
        tier=tier, source_ref=source_ref, confirmation_ref=confirmation_ref
    )
    event = ValueEvent(
        customer_id=customer_id,
        kind=kind,
        amount=float(amount),
        tier=tier,
        tenant_id=tenant_id or _DEFAULT_TENANT,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
        notes=notes,
    )
    path = _path()
    _ensure_dir(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def _parse_event(line: str) -> ValueEvent | None:
    """Parse a single JSONL ledger line; returns None on any malformed input."""
    try:
        data = json.loads(line)
        data.setdefault("tenant_id", _DEFAULT_TENANT)
        return ValueEvent(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def _event_timestamp(event: ValueEvent) -> float:
    try:
        return datetime.fromisoformat(event.occurred_at).timestamp()
    except (TypeError, ValueError):
        return 0.0


def list_events(
    *,
    customer_id: str,
    tenant_id: str | None = None,
    limit: int = 1000,
    since_days: int | None = None,
) -> list[ValueEvent]:
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    cutoff = (
        None
        if since_days is None
        else datetime.now(UTC).timestamp() - since_days * 86400
    )
    out: list[ValueEvent] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            ev = _parse_event(line)
            if ev is None or ev.customer_id != customer_id:
                continue
            if tenant_id is not None and ev.tenant_id != tenant_id:
                continue
            if cutoff is not None and _event_timestamp(ev) < cutoff:
                continue
            out.append(ev)
            if len(out) >= limit:
                break
    return out


def summarize(
    *, customer_id: str, period_days: int = 30, tenant_id: str | None = None
) -> dict[str, Any]:
    events = list_events(
        customer_id=customer_id, tenant_id=tenant_id, since_days=period_days
    )
    summary: dict[str, Any] = {
        tier: {"count": 0, "total": 0.0} for tier in _VALID_TIERS
    }
    for ev in events:
        bucket = summary.setdefault(ev.tier, {"count": 0, "total": 0.0})
        bucket["count"] += 1
        bucket["total"] += ev.amount
    summary["customer_id"] = customer_id
    summary["period_days"] = period_days
    summary["event_count"] = len(events)
    return summary


def clear_for_test(customer_id: str | None = None) -> None:
    """Dev/test helper — truncates the JSONL ledger file."""
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


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

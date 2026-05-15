"""Value ledger — auditable, tenant-scoped value events for the Monthly Value Report.

Tier discipline (Dealix doctrine — estimated value is never auto-promoted):
  * ``estimated``        — modelled range; no evidence required.
  * ``observed``         — seen in workflow; requires ``source_ref``.
  * ``verified``         — sourced fact; requires ``source_ref``.
  * ``client_confirmed`` — client signed off; requires ``source_ref`` AND
    ``confirmation_ref``.

Backed by a JSONL file (env ``DEALIX_VALUE_LEDGER_PATH``) so it mirrors the
friction_log store and stays append-only / auditable.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/value-ledger.jsonl"
_lock = threading.Lock()

VALID_TIERS: frozenset[str] = frozenset(
    {"estimated", "observed", "verified", "client_confirmed"}
)


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier evidence discipline."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    value_event_id: str = field(default_factory=lambda: f"VAL-{uuid.uuid4().hex[:12]}")
    occurred_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _validate_discipline(
    tier: str, source_ref: str, confirmation_ref: str
) -> None:
    if tier not in VALID_TIERS:
        raise ValueDisciplineError(
            f"unknown tier '{tier}'; expected one of {sorted(VALID_TIERS)}"
        )
    if tier in {"observed", "verified", "client_confirmed"} and not source_ref.strip():
        raise ValueDisciplineError(f"tier '{tier}' requires a non-empty source_ref")
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
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    if not customer_id:
        raise ValueError("customer_id is required")
    _validate_discipline(tier, source_ref, confirmation_ref)
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
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(*, customer_id: str, period_days: int | None = None) -> list[ValueEvent]:
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    cutoff: float | None = None
    if period_days is not None:
        cutoff = datetime.now(timezone.utc).timestamp() - period_days * 86400
    out: list[ValueEvent] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = ValueEvent(**json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
                if ev.customer_id != customer_id:
                    continue
                if cutoff is not None:
                    try:
                        ts = datetime.fromisoformat(ev.occurred_at).timestamp()
                    except Exception:  # noqa: BLE001
                        ts = 0.0
                    if ts < cutoff:
                        continue
                out.append(ev)
    return out


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    """Aggregate per-tier totals. Estimated is never promoted into other tiers."""
    events = list_events(customer_id=customer_id, period_days=period_days)
    summary: dict[str, Any] = {
        tier: {"count": 0, "total_amount": 0.0} for tier in sorted(VALID_TIERS)
    }
    for ev in events:
        bucket = summary.setdefault(
            ev.tier, {"count": 0, "total_amount": 0.0}
        )
        bucket["count"] += 1
        bucket["total_amount"] = round(bucket["total_amount"] + ev.amount, 2)
    summary["event_count"] = len(events)
    summary["period_days"] = period_days
    return summary


def clear_for_test(customer_id: str | None = None) -> None:
    """Test helper — drop one customer's events, or the whole ledger."""
    path = _path()
    if not path.exists():
        return
    with _lock:
        if customer_id is None:
            path.write_text("", encoding="utf-8")
            return
        kept: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                if json.loads(line).get("customer_id") != customer_id:
                    kept.append(line)
            except Exception:  # noqa: BLE001
                continue
        path.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")


# Backwards-compatible re-export of the canonical proof-architecture ledger record.
from auto_client_acquisition.proof_architecture_os.value_ledger import (  # noqa: E402
    ValueLedgerEvent,
    value_ledger_event_valid,
)

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

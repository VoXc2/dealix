"""Value OS ledger (append-only JSONL, tenant-scoped).

This module keeps a compatibility bridge with
``proof_architecture_os.value_ledger`` while also exposing the operational
Value OS API used by routers, reports, and scripts.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_DEFAULT_PATH = "var/value-ledger.jsonl"
_LOCK = threading.Lock()


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier evidence discipline."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    """Operational value event tracked per customer."""

    event_id: str
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

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "customer_id": self.customer_id,
            "kind": self.kind,
            "amount": self.amount,
            "tier": self.tier,
            "source_ref": self.source_ref,
            "confirmation_ref": self.confirmation_ref,
            "notes": self.notes,
            "occurred_at": self.occurred_at,
        }


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _new_event_id() -> str:
    return f"val_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"


def _normalize_tier(tier: str) -> str:
    return str(tier or "").strip().lower()


def _validate_discipline(*, tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier == "verified" and not source_ref:
        raise ValueDisciplineError(
            "tier=verified requires non-empty source_ref",
        )
    if tier == "client_confirmed" and (not source_ref or not confirmation_ref):
        raise ValueDisciplineError(
            "tier=client_confirmed requires both source_ref and confirmation_ref",
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
    """Append one value event after discipline checks."""
    if not str(customer_id).strip():
        raise ValueError("customer_id is required")
    if not str(kind).strip():
        raise ValueError("kind is required")

    normalized_tier = _normalize_tier(tier)
    _validate_discipline(
        tier=normalized_tier,
        source_ref=str(source_ref or "").strip(),
        confirmation_ref=str(confirmation_ref or "").strip(),
    )
    event = ValueEvent(
        event_id=_new_event_id(),
        customer_id=str(customer_id).strip(),
        kind=str(kind).strip(),
        amount=float(amount or 0.0),
        tier=normalized_tier,
        source_ref=str(source_ref or "").strip(),
        confirmation_ref=str(confirmation_ref or "").strip(),
        notes=str(notes or "").strip(),
    )

    path = _path()
    _ensure_dir(path)
    with _LOCK:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str | None = None,
    limit: int = 200,
    since_days: int | None = None,
) -> list[ValueEvent]:
    """List events, optionally scoped by customer and time window."""
    path = _path()
    if not path.exists():
        return []
    cutoff = None
    if since_days is not None and since_days >= 0:
        cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)

    out: list[ValueEvent] = []
    with _LOCK:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    ev = ValueEvent(**data)
                except Exception:  # noqa: BLE001
                    continue
                if customer_id and ev.customer_id != customer_id:
                    continue
                if cutoff is not None:
                    try:
                        ts = datetime.fromisoformat(ev.occurred_at)
                    except Exception:  # noqa: BLE001
                        continue
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    if ts < cutoff:
                        continue
                out.append(ev)
    out.sort(key=lambda e: e.occurred_at, reverse=True)
    return out[: max(0, int(limit))]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, object]:
    """Summarize value amounts by tier in a fixed, stable shape."""
    events = list_events(customer_id=customer_id, limit=5000, since_days=period_days)
    totals = {
        "estimated": 0.0,
        "observed": 0.0,
        "verified": 0.0,
        "client_confirmed": 0.0,
    }
    counts = {
        "estimated": 0,
        "observed": 0,
        "verified": 0,
        "client_confirmed": 0,
    }
    for ev in events:
        if ev.tier in totals:
            totals[ev.tier] += float(ev.amount)
            counts[ev.tier] += 1

    return {
        "customer_id": customer_id,
        "period_days": int(period_days),
        "total_events": len(events),
        "estimated_amount": round(totals["estimated"], 4),
        "observed_amount": round(totals["observed"], 4),
        "verified_amount": round(totals["verified"], 4),
        "client_confirmed_amount": round(totals["client_confirmed"], 4),
        "estimated": round(totals["estimated"], 4),
        "observed": round(totals["observed"], 4),
        "verified": round(totals["verified"], 4),
        "client_confirmed": round(totals["client_confirmed"], 4),
        "by_tier_count": counts,
    }


def clear_for_test(customer_id: str | None = None) -> None:
    """Clear all events or only one customer's events."""
    path = _path()
    if not path.exists():
        return

    if not customer_id:
        with _LOCK:
            path.write_text("", encoding="utf-8")
        return

    kept: list[str] = []
    with _LOCK:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                if data.get("customer_id") != customer_id:
                    kept.append(json.dumps(data, ensure_ascii=False))
        path.write_text(("\n".join(kept) + ("\n" if kept else "")), encoding="utf-8")


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

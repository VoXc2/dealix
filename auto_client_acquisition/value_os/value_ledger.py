"""Value OS ledger — append-only value events + discipline guards.

Backwards-compat exports (`ValueLedgerEvent`, `value_ledger_event_valid`) stay
available for existing layered package smoke tests.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from auto_client_acquisition.friction_log.sanitizer import sanitize_notes
from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_DEFAULT_PATH = "var/value-ledger.jsonl"
_lock = threading.Lock()
_KNOWN_TIERS = {"estimated", "observed", "verified", "client_confirmed"}


class ValueDisciplineError(ValueError):
    """Raised when event tier discipline is violated."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    event_id: str
    customer_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _normalize_tier(tier: str) -> str:
    t = (tier or "").strip().lower()
    if t not in _KNOWN_TIERS:
        raise ValueDisciplineError(
            f"invalid tier '{tier}'. Allowed: {sorted(_KNOWN_TIERS)}"
        )
    return t


def _validate_discipline(*, tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier == "verified" and not source_ref.strip():
        raise ValueDisciplineError("verified tier requires non-empty source_ref")
    if tier == "client_confirmed":
        if not source_ref.strip() or not confirmation_ref.strip():
            raise ValueDisciplineError(
                "client_confirmed tier requires both source_ref and confirmation_ref"
            )


def _event_from_dict(data: dict[str, object]) -> ValueEvent | None:
    try:
        return ValueEvent(
            event_id=str(data.get("event_id", "")),
            customer_id=str(data.get("customer_id", "")),
            kind=str(data.get("kind", "")),
            amount=float(data.get("amount", 0.0) or 0.0),
            tier=_normalize_tier(str(data.get("tier", "estimated"))),
            source_ref=str(data.get("source_ref", "")),
            confirmation_ref=str(data.get("confirmation_ref", "")),
            notes=str(data.get("notes", "")),
            occurred_at=str(data.get("occurred_at", "")) or datetime.now(timezone.utc).isoformat(),
        )
    except Exception:  # noqa: BLE001
        return None


def add_event(
    *,
    customer_id: str,
    kind: str,
    amount: float = 0.0,
    tier: str = "estimated",
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    """Append one value event with doctrine discipline validation."""
    cid = customer_id.strip()
    if not cid:
        raise ValueDisciplineError("customer_id is required")
    k = kind.strip()
    if not k:
        raise ValueDisciplineError("kind is required")
    normalized_tier = _normalize_tier(tier)
    _validate_discipline(
        tier=normalized_tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
    )

    event = ValueEvent(
        event_id=f"val_{uuid4().hex[:16]}",
        customer_id=cid,
        kind=k,
        amount=float(amount or 0.0),
        tier=normalized_tier,
        source_ref=source_ref.strip(),
        confirmation_ref=confirmation_ref.strip(),
        notes=sanitize_notes(notes),
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str = "",
    limit: int = 200,
    since_days: int = 3650,
) -> list[ValueEvent]:
    """List value events for a customer (or all customers when unset)."""
    path = _path()
    if not path.exists():
        return []

    customer_filter = customer_id.strip()
    cutoff_ts = datetime.now(timezone.utc).timestamp() - max(int(since_days), 0) * 86400
    out: list[ValueEvent] = []

    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                event = _event_from_dict(data if isinstance(data, dict) else {})
                if event is None:
                    continue
                if customer_filter and event.customer_id != customer_filter:
                    continue
                try:
                    ts = datetime.fromisoformat(event.occurred_at).timestamp()
                except Exception:  # noqa: BLE001
                    ts = 0.0
                if ts < cutoff_ts:
                    continue
                out.append(event)

    # Return newest-first for downstream reporting/read-model UX.
    out.sort(key=lambda e: e.occurred_at, reverse=True)
    return out[: max(int(limit), 0)]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, object]:
    """Summarize event counts and monetary totals by tier."""
    events = list_events(customer_id=customer_id, limit=10_000, since_days=period_days)

    amounts = {tier: 0.0 for tier in _KNOWN_TIERS}
    counts = {tier: 0 for tier in _KNOWN_TIERS}
    for ev in events:
        if ev.tier not in amounts:
            continue
        amounts[ev.tier] += float(ev.amount or 0.0)
        counts[ev.tier] += 1

    return {
        "customer_id": customer_id,
        "period_days": int(period_days),
        "total_events": len(events),
        "estimated_amount": round(amounts["estimated"], 2),
        "observed_amount": round(amounts["observed"], 2),
        "verified_amount": round(amounts["verified"], 2),
        "client_confirmed_amount": round(amounts["client_confirmed"], 2),
        "estimated": {"count": counts["estimated"], "amount": round(amounts["estimated"], 2)},
        "observed": {"count": counts["observed"], "amount": round(amounts["observed"], 2)},
        "verified": {"count": counts["verified"], "amount": round(amounts["verified"], 2)},
        "client_confirmed": {
            "count": counts["client_confirmed"],
            "amount": round(amounts["client_confirmed"], 2),
        },
        "governance_decision": "allow_with_review",
        "is_estimate": True,
    }


def clear_for_test(customer_id: str = "") -> None:
    """Clear ledger file entirely, or remove one customer's events."""
    path = _path()
    if not path.exists():
        return

    cid = customer_id.strip()
    with _lock:
        if not cid:
            path.write_text("", encoding="utf-8")
            return
        kept: list[str] = []
        with path.open("r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                except Exception:  # noqa: BLE001
                    continue
                if str(data.get("customer_id", "")) == cid:
                    continue
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

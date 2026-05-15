"""Value OS ledger with tier discipline and JSONL persistence."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
import json
import os
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_LOCK = Lock()
_VALID_TIERS = {"estimated", "observed", "verified", "client_confirmed", "measured"}


class ValueDisciplineError(ValueError):
    """Raised when value evidence discipline is violated."""


@dataclass(slots=True)
class ValueEvent:
    event_id: str
    customer_id: str
    tenant_id: str
    kind: str
    amount: float
    tier: str
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ValueEvent":
        return cls(
            event_id=str(payload.get("event_id", "")),
            customer_id=str(payload.get("customer_id", "")),
            tenant_id=str(payload.get("tenant_id", payload.get("customer_id", ""))),
            kind=str(payload.get("kind", "")),
            amount=float(payload.get("amount", 0.0)),
            tier=str(payload.get("tier", "estimated")),
            source_ref=str(payload.get("source_ref", "")),
            confirmation_ref=str(payload.get("confirmation_ref", "")),
            notes=str(payload.get("notes", "")),
            occurred_at=str(payload.get("occurred_at", datetime.now(UTC).isoformat())),
        )


def _path() -> Path:
    configured = os.getenv("DEALIX_VALUE_LEDGER_PATH", "").strip()
    if configured:
        return Path(configured)
    return Path("data/value_ledger.jsonl")


def _ensure_parent_exists(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _validate_tier_discipline(*, tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier not in _VALID_TIERS:
        raise ValueDisciplineError(f"unsupported tier: {tier}")
    if tier in {"verified", "measured"} and not source_ref.strip():
        raise ValueDisciplineError(f"{tier} tier requires source_ref")
    if tier == "client_confirmed":
        if not source_ref.strip():
            raise ValueDisciplineError("client_confirmed tier requires source_ref")
        if not confirmation_ref.strip():
            raise ValueDisciplineError("client_confirmed tier requires confirmation_ref")


def add_event(
    *,
    customer_id: str,
    kind: str,
    amount: float = 0.0,
    tier: str = "estimated",
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
    tenant_id: str | None = None,
    occurred_at: str | None = None,
) -> ValueEvent:
    customer = customer_id.strip()
    if not customer:
        raise ValueDisciplineError("customer_id is required")
    if not kind.strip():
        raise ValueDisciplineError("kind is required")
    _validate_tier_discipline(
        tier=tier,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
    )
    event = ValueEvent(
        event_id=f"val_{uuid4().hex[:12]}",
        customer_id=customer,
        tenant_id=(tenant_id or customer).strip(),
        kind=kind.strip(),
        amount=float(amount),
        tier=tier,
        source_ref=source_ref.strip(),
        confirmation_ref=confirmation_ref.strip(),
        notes=notes.strip(),
        occurred_at=occurred_at or datetime.now(UTC).isoformat(),
    )
    path = _path()
    _ensure_parent_exists(path)
    with _LOCK:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(*, customer_id: str = "", limit: int = 2000) -> list[ValueEvent]:
    path = _path()
    if not path.exists():
        return []
    customer_filter = customer_id.strip()
    rows: list[ValueEvent] = []
    with _LOCK:
        for line in path.read_text(encoding="utf-8").splitlines():
            payload = line.strip()
            if not payload:
                continue
            try:
                event = ValueEvent.from_dict(json.loads(payload))
            except Exception:  # noqa: BLE001
                continue
            if customer_filter and event.customer_id != customer_filter:
                continue
            rows.append(event)
    rows.sort(key=lambda r: r.occurred_at, reverse=True)
    if limit <= 0:
        return rows
    return rows[:limit]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    cutoff = datetime.now(UTC) - timedelta(days=max(period_days, 0))
    events = []
    for event in list_events(customer_id=customer_id, limit=10_000):
        try:
            ts = datetime.fromisoformat(event.occurred_at)
        except ValueError:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        if ts >= cutoff:
            events.append(event)
    out: dict[str, Any] = {
        "customer_id": customer_id,
        "period_days": period_days,
        "total_events": len(events),
        "estimated": 0.0,
        "observed": 0.0,
        "verified": 0.0,
        "client_confirmed": 0.0,
        "measured": 0.0,
    }
    for event in events:
        out[event.tier] = round(float(out.get(event.tier, 0.0)) + float(event.amount), 2)
    # Compatibility keys consumed by weekly brief and dashboards.
    out["estimated_amount"] = out["estimated"]
    out["observed_amount"] = out["observed"]
    out["verified_amount"] = out["verified"]
    out["client_confirmed_amount"] = out["client_confirmed"]
    out["measured_amount"] = out["measured"]
    return out


def clear_for_test(customer_id: str | None = None) -> None:
    path = _path()
    if not path.exists():
        return
    target_customer = (customer_id or "").strip()
    with _LOCK:
        if not target_customer:
            path.unlink(missing_ok=True)
            return
        kept: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            payload = line.strip()
            if not payload:
                continue
            try:
                event = ValueEvent.from_dict(json.loads(payload))
            except Exception:  # noqa: BLE001
                continue
            if event.customer_id != target_customer:
                kept.append(json.dumps(event.to_dict(), ensure_ascii=False))
        _ensure_parent_exists(path)
        if kept:
            path.write_text("\n".join(kept) + "\n", encoding="utf-8")
        else:
            path.unlink(missing_ok=True)


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

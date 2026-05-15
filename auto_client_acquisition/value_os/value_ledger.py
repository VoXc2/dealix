"""Value ledger with tier-discipline and JSONL persistence."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)


class ValueDisciplineError(ValueError):
    """Raised when tier/source discipline is violated."""


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
    occurred_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _ledger_path() -> Path:
    raw = os.getenv("DEALIX_VALUE_LEDGER_PATH", "data/value_ledger.jsonl")
    path = Path(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _serialize(ev: ValueEvent) -> str:
    return json.dumps(ev.to_dict(), ensure_ascii=False)


def _deserialize(line: str) -> ValueEvent:
    data = json.loads(line)
    return ValueEvent(
        event_id=str(data.get("event_id", "")),
        customer_id=str(data.get("customer_id", "")),
        kind=str(data.get("kind", "")),
        amount=float(data.get("amount", 0.0)),
        tier=str(data.get("tier", "estimated")),
        source_ref=str(data.get("source_ref", "")),
        confirmation_ref=str(data.get("confirmation_ref", "")),
        notes=str(data.get("notes", "")),
        occurred_at=str(data.get("occurred_at", "")),
    )


def _discipline_check(*, tier: str, source_ref: str, confirmation_ref: str) -> None:
    normalized_tier = tier.strip().lower()
    if normalized_tier == "verified" and not source_ref.strip():
        raise ValueDisciplineError("verified tier requires source_ref")
    if normalized_tier == "client_confirmed":
        if not source_ref.strip() or not confirmation_ref.strip():
            raise ValueDisciplineError("client_confirmed tier requires source_ref and confirmation_ref")


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
    _discipline_check(tier=tier, source_ref=source_ref, confirmation_ref=confirmation_ref)
    event = ValueEvent(
        event_id=f"val_{uuid4().hex[:20]}",
        customer_id=customer_id,
        kind=kind,
        amount=float(amount),
        tier=tier.strip().lower(),
        source_ref=source_ref.strip(),
        confirmation_ref=confirmation_ref.strip(),
        notes=notes,
        occurred_at=_now_iso(),
    )
    path = _ledger_path()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(_serialize(event))
        handle.write("\n")
    return event


def list_events(
    *,
    customer_id: str | None = None,
    since_days: int | None = None,
    limit: int = 200,
) -> list[ValueEvent]:
    path = _ledger_path()
    if not path.exists():
        return []
    rows: list[ValueEvent] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                ev = _deserialize(line)
            except Exception:  # noqa: BLE001
                continue
            if customer_id and ev.customer_id != customer_id:
                continue
            rows.append(ev)
    if since_days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
        filtered: list[ValueEvent] = []
        for ev in rows:
            try:
                ts = datetime.fromisoformat(ev.occurred_at)
            except Exception:  # noqa: BLE001
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= cutoff:
                filtered.append(ev)
        rows = filtered
    rows.sort(key=lambda ev: ev.occurred_at, reverse=True)
    return rows[: max(0, limit)]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, float]:
    events = list_events(customer_id=customer_id, since_days=period_days, limit=10000)
    summary = {"estimated": 0.0, "observed": 0.0, "verified": 0.0, "client_confirmed": 0.0}
    for ev in events:
        summary.setdefault(ev.tier, 0.0)
        summary[ev.tier] += float(ev.amount)
    return summary


def clear_for_test(customer_id: str | None = None) -> None:
    path = _ledger_path()
    if not path.exists():
        return
    if not customer_id:
        path.unlink()
        return
    kept = [ev for ev in list_events(limit=100000) if ev.customer_id != customer_id]
    with path.open("w", encoding="utf-8") as handle:
        for ev in kept:
            handle.write(_serialize(ev))
            handle.write("\n")


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

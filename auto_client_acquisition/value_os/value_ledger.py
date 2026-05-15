"""Value OS ledger with backward-compatible event APIs.

This module keeps the original ``ValueLedgerEvent`` re-export for layered
package smoke tests while also exposing the operational Value OS functions used
by routers and reports.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_DEFAULT_PATH = "var/value-ledger.jsonl"
_LOCK = threading.Lock()
_ALLOWED_TIERS = {"estimated", "observed", "verified", "client_confirmed"}


class ValueDisciplineError(ValueError):
    """Raised when Value OS tier-proof discipline rules are violated."""


@dataclass(slots=True)
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    path = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[2] / path
    return path


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _normalize_tier(tier: str) -> str:
    normalized = (tier or "").strip().lower()
    if normalized not in _ALLOWED_TIERS:
        raise ValueDisciplineError(
            "tier must be one of: estimated, observed, verified, client_confirmed",
        )
    return normalized


def _enforce_discipline(*, tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier == "verified" and not source_ref.strip():
        raise ValueDisciplineError("verified tier requires non-empty source_ref")
    if tier == "client_confirmed":
        if not source_ref.strip() or not confirmation_ref.strip():
            raise ValueDisciplineError(
                "client_confirmed tier requires both source_ref and confirmation_ref",
            )


def _event_id(*, customer_id: str, kind: str, occurred_at: str) -> str:
    digest = hashlib.sha256(f"{customer_id}|{kind}|{occurred_at}".encode()).hexdigest()
    return f"val_{digest[:16]}"


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
    if not customer_id.strip():
        raise ValueError("customer_id is required")
    if not kind.strip():
        raise ValueError("kind is required")

    tier_value = _normalize_tier(tier)
    _enforce_discipline(
        tier=tier_value,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
    )
    occurred_at = datetime.now(timezone.utc).isoformat()
    event = ValueEvent(
        event_id=_event_id(customer_id=customer_id, kind=kind, occurred_at=occurred_at),
        customer_id=customer_id.strip(),
        kind=kind.strip(),
        amount=float(amount),
        tier=tier_value,
        source_ref=source_ref.strip(),
        confirmation_ref=confirmation_ref.strip(),
        notes=notes.strip(),
        occurred_at=occurred_at,
    )
    path = _path()
    _ensure_dir(path)
    with _LOCK:
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str | None = None,
    limit: int = 200,
    since_days: int | None = None,
) -> list[ValueEvent]:
    path = _path()
    if not path.exists():
        return []

    cutoff_ts: float | None = None
    if since_days is not None:
        cutoff_ts = datetime.now(timezone.utc).timestamp() - int(since_days) * 86400

    events: list[ValueEvent] = []
    with _LOCK:
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    event = ValueEvent(**row)
                except Exception:  # noqa: BLE001
                    continue
                if customer_id and event.customer_id != customer_id:
                    continue
                if cutoff_ts is not None:
                    try:
                        ts = datetime.fromisoformat(event.occurred_at).timestamp()
                    except Exception:  # noqa: BLE001
                        continue
                    if ts < cutoff_ts:
                        continue
                events.append(event)

    events.sort(key=lambda event: event.occurred_at, reverse=True)
    return events[: max(0, int(limit))]


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    events = list_events(customer_id=customer_id, since_days=period_days, limit=1000)
    summary: dict[str, Any] = {
        "customer_id": customer_id,
        "period_days": int(period_days),
        "total_events": len(events),
        "estimated": 0.0,
        "observed": 0.0,
        "verified": 0.0,
        "client_confirmed": 0.0,
    }
    for event in events:
        summary[event.tier] = round(float(summary.get(event.tier, 0.0)) + float(event.amount), 2)
    # Keep stable keys expected by weekly brief and dashboards.
    summary["estimated_amount"] = summary["estimated"]
    summary["observed_amount"] = summary["observed"]
    summary["verified_amount"] = summary["verified"]
    summary["client_confirmed_amount"] = summary["client_confirmed"]
    return summary


def clear_for_test(customer_id: str | None = None) -> None:
    path = _path()
    if not path.exists():
        return

    with _LOCK:
        if not customer_id:
            path.write_text("", encoding="utf-8")
            return

        kept_lines: list[str] = []
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                if row.get("customer_id") != customer_id:
                    kept_lines.append(json.dumps(row, ensure_ascii=False))

        output = "\n".join(kept_lines)
        if output:
            output += "\n"
        path.write_text(output, encoding="utf-8")


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

"""Value ledger — append-only JSONL store for value events with tier
discipline.

Tiers (strict):
- estimated         → no source_ref required; NEVER promoted to verified
- observed          → no source_ref required; measured in workflow
- verified          → REQUIRES non-empty source_ref
- client_confirmed  → REQUIRES non-empty source_ref AND confirmation_ref

Storage: $DEALIX_VALUE_LEDGER_PATH (default var/value-ledger.jsonl).
Mirrors the pattern used by consent_table.py and proof_ledger/file_backend.py.

`ValueLedgerEvent` / `value_ledger_event_valid` are also re-exported here so
this module stays the single stable ``value_os`` import path for both the
JSONL ledger API and the proof-architecture event contract.
"""
from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

ALLOWED_TIERS = frozenset({"estimated", "observed", "verified", "client_confirmed"})

_DEFAULT_PATH = "var/value-ledger.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_VALUE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        # value_os/value_ledger.py → parent.parent = auto_client_acquisition → parent = repo root
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


class ValueDisciplineError(ValueError):
    """Raised when a value event violates tier discipline."""


@dataclass
class ValueEvent:
    event_id: str = field(default_factory=lambda: f"val_{uuid4().hex[:12]}")
    customer_id: str = ""
    kind: str = ""
    amount: float = 0.0
    tier: str = "estimated"
    source_ref: str = ""
    confirmation_ref: str = ""
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_tier(tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier not in ALLOWED_TIERS:
        raise ValueDisciplineError(
            f"tier {tier!r} not in {sorted(ALLOWED_TIERS)}"
        )
    if tier == "verified" and not source_ref:
        raise ValueDisciplineError("verified tier requires non-empty source_ref")
    if tier == "client_confirmed":
        if not source_ref:
            raise ValueDisciplineError(
                "client_confirmed tier requires non-empty source_ref"
            )
        if not confirmation_ref:
            raise ValueDisciplineError(
                "client_confirmed tier requires non-empty confirmation_ref"
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
        raise ValueDisciplineError("customer_id is required")
    _validate_tier(tier, source_ref, confirmation_ref)
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
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str | None = None,
    tier: str | None = None,
    limit: int = 1000,
) -> list[ValueEvent]:
    path = _path()
    if not path.exists():
        return []
    out: list[ValueEvent] = []
    with _lock:
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
                if tier and ev.tier != tier:
                    continue
                out.append(ev)
                if len(out) >= limit:
                    break
    return out


def summarize(*, customer_id: str, period_days: int = 30) -> dict[str, Any]:
    cutoff = datetime.now(timezone.utc).timestamp() - period_days * 86400
    events = list_events(customer_id=customer_id)
    in_window: list[ValueEvent] = []
    for ev in events:
        try:
            ts = datetime.fromisoformat(ev.occurred_at).timestamp()
        except Exception:  # noqa: BLE001
            ts = 0.0
        if ts >= cutoff:
            in_window.append(ev)
    by_tier: dict[str, dict[str, float]] = {t: {"count": 0, "total_amount": 0.0} for t in ALLOWED_TIERS}
    for ev in in_window:
        bucket = by_tier.setdefault(ev.tier, {"count": 0, "total_amount": 0.0})
        bucket["count"] += 1
        bucket["total_amount"] += float(ev.amount)
    return {
        "customer_id": customer_id,
        "period_days": period_days,
        "total_events": len(in_window),
        "by_tier": by_tier,
        "estimated": by_tier["estimated"],
        "observed": by_tier["observed"],
        "verified": by_tier["verified"],
        "client_confirmed": by_tier["client_confirmed"],
        "estimated_amount": by_tier["estimated"]["total_amount"],
        "observed_amount": by_tier["observed"]["total_amount"],
        "verified_amount": by_tier["verified"]["total_amount"],
        "client_confirmed_amount": by_tier["client_confirmed"]["total_amount"],
    }


def clear_for_test(customer_id: str | None = None) -> None:
    """Test-only: truncate the ledger file. If customer_id is provided,
    only that customer's events are removed; otherwise the whole file is
    truncated."""
    path = _path()
    if not path.exists():
        return
    with _lock:
        if customer_id is None:
            path.write_text("", encoding="utf-8")
            return
        keep: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                if json.loads(line).get("customer_id") != customer_id:
                    keep.append(line)
            except Exception:  # noqa: BLE001
                keep.append(line)
        path.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")


__all__ = [
    "ALLOWED_TIERS",
    "ValueDisciplineError",
    "ValueEvent",
    "ValueLedgerEvent",
    "add_event",
    "clear_for_test",
    "list_events",
    "summarize",
    "value_ledger_event_valid",
]

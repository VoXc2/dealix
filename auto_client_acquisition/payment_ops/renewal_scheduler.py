"""Recurring billing scheduler — Wave 2 Retainer Engine.

Schedules a renewal attempt N days after a paid retainer cycle.
For month-1 retainers, the founder reviews + manually confirms each cycle.
After 3 successful manual confirms, the customer can be flipped to
auto-charge (Moyasar subscription).

Storage: $DEALIX_RENEWAL_SCHEDULE_PATH (default var/renewal-schedule.jsonl).
Same JSONL pattern as friction_log + value_ledger + capital_ledger.
"""
from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4


class RenewalStatus(StrEnum):
    SCHEDULED = "scheduled"
    AWAITING_FOUNDER = "awaiting_founder"
    CONFIRMED = "confirmed"
    SKIPPED = "skipped"
    FAILED = "failed"
    AUTO_CHARGED = "auto_charged"


_DEFAULT_PATH = "var/renewal-schedule.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_RENEWAL_SCHEDULE_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class RenewalSchedule:
    schedule_id: str = field(default_factory=lambda: f"rnw_{uuid4().hex[:12]}")
    customer_id: str = ""
    plan: str = ""  # managed_revenue_ops_starter | managed_revenue_ops_growth | ...
    amount_sar: int = 0
    cadence_days: int = 30
    next_attempt_at: str = ""
    last_paid_at: str = ""
    cycle_count: int = 0
    status: str = RenewalStatus.SCHEDULED.value
    auto_charge_eligible: bool = False  # flips to True after 3 confirmed manual cycles
    notes: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def schedule_renewal(
    *,
    customer_id: str,
    plan: str,
    amount_sar: int,
    cadence_days: int = 30,
    last_paid_at: str | None = None,
) -> RenewalSchedule:
    """Schedule the next renewal for a retainer customer.

    Default month-1 behavior: status=AWAITING_FOUNDER. Founder reviews + confirms.
    """
    if not customer_id:
        raise ValueError("customer_id is required")
    if amount_sar <= 0:
        raise ValueError("amount_sar must be positive")
    last_paid = last_paid_at or datetime.now(timezone.utc).isoformat()
    last_dt = datetime.fromisoformat(last_paid)
    next_dt = last_dt + timedelta(days=cadence_days)
    schedule = RenewalSchedule(
        customer_id=customer_id,
        plan=plan,
        amount_sar=amount_sar,
        cadence_days=cadence_days,
        last_paid_at=last_paid,
        next_attempt_at=next_dt.isoformat(),
        status=RenewalStatus.AWAITING_FOUNDER.value,
        cycle_count=0,
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(schedule.to_dict(), ensure_ascii=False) + "\n")
    return schedule


def list_due(*, on_date: datetime | None = None) -> list[RenewalSchedule]:
    """Return scheduled renewals whose next_attempt_at is in the past."""
    target = (on_date or datetime.now(timezone.utc)).isoformat()
    path = _path()
    if not path.exists():
        return []
    out: list[RenewalSchedule] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    s = RenewalSchedule(**data)
                except Exception:  # noqa: BLE001
                    continue
                if s.status in (
                    RenewalStatus.SCHEDULED.value,
                    RenewalStatus.AWAITING_FOUNDER.value,
                ) and s.next_attempt_at <= target:
                    out.append(s)
    return out


def list_by_customer(customer_id: str) -> list[RenewalSchedule]:
    path = _path()
    if not path.exists():
        return []
    out: list[RenewalSchedule] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    s = RenewalSchedule(**data)
                except Exception:  # noqa: BLE001
                    continue
                if s.customer_id == customer_id:
                    out.append(s)
    return out


def mark_confirmed(schedule_id: str) -> bool:
    """Founder confirmed receipt of payment. Increments cycle count. Eligible
    for auto-charge after 3 confirmed cycles.
    """
    return _patch(schedule_id, {"status": RenewalStatus.CONFIRMED.value, "_inc_cycle": True})


def mark_skipped(schedule_id: str, reason: str = "") -> bool:
    return _patch(
        schedule_id, {"status": RenewalStatus.SKIPPED.value, "notes": reason}
    )


def mark_failed(schedule_id: str, reason: str = "") -> bool:
    return _patch(
        schedule_id, {"status": RenewalStatus.FAILED.value, "notes": reason}
    )


def _patch(schedule_id: str, patch: dict[str, Any]) -> bool:
    path = _path()
    if not path.exists():
        return False
    with _lock:
        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines: list[str] = []
        found = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except Exception:  # noqa: BLE001
                new_lines.append(line)
                continue
            if data.get("schedule_id") == schedule_id:
                found = True
                inc = patch.pop("_inc_cycle", False)
                data.update(patch)
                if inc:
                    data["cycle_count"] = int(data.get("cycle_count", 0)) + 1
                if data.get("cycle_count", 0) >= 3:
                    data["auto_charge_eligible"] = True
                new_lines.append(json.dumps(data, ensure_ascii=False))
            else:
                new_lines.append(json.dumps(data, ensure_ascii=False))
        if not found:
            return False
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return True


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "RenewalSchedule",
    "RenewalStatus",
    "clear_for_test",
    "list_by_customer",
    "list_due",
    "mark_confirmed",
    "mark_failed",
    "mark_skipped",
    "schedule_renewal",
]

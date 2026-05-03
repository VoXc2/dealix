"""
SLA Tracker — pure helpers that compute breach + remaining time per session.

No I/O. The router calls these on rows already loaded from the DB.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class SLAStatus:
    deadline_at: datetime | None
    is_breached: bool
    hours_remaining: float | None  # negative when breached
    risk_level: str                # ok | warning | breach


def status_for(
    deadline_at: datetime | None,
    *,
    now: datetime | None = None,
    warning_window_hours: float = 6.0,
) -> SLAStatus:
    if deadline_at is None:
        return SLAStatus(None, False, None, "ok")
    cur = now or datetime.now(timezone.utc)
    # Tolerate naive deadline values returned by SQLite.
    if deadline_at.tzinfo is None:
        deadline_at = deadline_at.replace(tzinfo=timezone.utc)
    delta = (deadline_at - cur).total_seconds() / 3600.0
    if delta < 0:
        return SLAStatus(deadline_at, True, delta, "breach")
    if delta < warning_window_hours:
        return SLAStatus(deadline_at, False, delta, "warning")
    return SLAStatus(deadline_at, False, delta, "ok")


def summarize(rows) -> dict[str, int]:
    """Bucket a list of ServiceSessionRecord-like by SLA risk_level."""
    buckets = {"ok": 0, "warning": 0, "breach": 0, "no_deadline": 0}
    for r in rows:
        if not r.deadline_at:
            buckets["no_deadline"] += 1
            continue
        s = status_for(r.deadline_at)
        buckets[s.risk_level] += 1
    return buckets

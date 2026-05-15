"""Friction log aggregator. Pure function over events."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.friction_log.schemas import FrictionEvent
from auto_client_acquisition.friction_log.store import list_events


@dataclass
class FrictionAggregate:
    customer_id: str
    window_days: int
    total: int
    by_kind: dict[str, int] = field(default_factory=dict)
    by_severity: dict[str, int] = field(default_factory=dict)
    top_3_kinds: list[tuple[str, int]] = field(default_factory=list)
    total_cost_minutes: int = 0
    week_over_week_delta: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "window_days": self.window_days,
            "total": self.total,
            "by_kind": dict(self.by_kind),
            "by_severity": dict(self.by_severity),
            "top_3_kinds": [list(t) for t in self.top_3_kinds],
            "total_cost_minutes": self.total_cost_minutes,
            "week_over_week_delta": self.week_over_week_delta,
        }


def _events_in_window(events: list[FrictionEvent], window_days: int) -> list[FrictionEvent]:
    cutoff = datetime.now(UTC).timestamp() - window_days * 86400
    out: list[FrictionEvent] = []
    for ev in events:
        try:
            ts = datetime.fromisoformat(ev.occurred_at).timestamp()
        except Exception:
            ts = 0.0
        if ts >= cutoff:
            out.append(ev)
    return out


def aggregate(*, customer_id: str, window_days: int = 30) -> FrictionAggregate:
    # Pull a wide window so we can compute WoW delta within the same call.
    events_2x = list_events(customer_id=customer_id, since_days=window_days * 2, limit=10000)
    current = _events_in_window(events_2x, window_days)
    older_start = datetime.now(UTC).timestamp() - window_days * 2 * 86400
    older_end = datetime.now(UTC).timestamp() - window_days * 86400
    previous: list[FrictionEvent] = []
    for ev in events_2x:
        try:
            ts = datetime.fromisoformat(ev.occurred_at).timestamp()
        except Exception:
            continue
        if older_start <= ts < older_end:
            previous.append(ev)

    by_kind: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    cost = 0
    for ev in current:
        by_kind[ev.kind] = by_kind.get(ev.kind, 0) + 1
        by_severity[ev.severity] = by_severity.get(ev.severity, 0) + 1
        cost += int(ev.cost_minutes or 0)
    top3 = sorted(by_kind.items(), key=lambda x: x[1], reverse=True)[:3]

    return FrictionAggregate(
        customer_id=customer_id,
        window_days=window_days,
        total=len(current),
        by_kind=by_kind,
        by_severity=by_severity,
        top_3_kinds=top3,
        total_cost_minutes=cost,
        week_over_week_delta=len(current) - len(previous),
    )


__all__ = ["FrictionAggregate", "aggregate"]

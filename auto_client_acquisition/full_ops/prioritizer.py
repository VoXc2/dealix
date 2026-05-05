"""V12 — pure-function WorkItem prioritizer.

Sort order (lowest = first):
  1. priority bucket (p0 < p1 < p2 < p3)
  2. has any ``risk_flags`` (flagged items first)
  3. age (older ``created_at`` first)
  4. id (stable tiebreak)

No mutation; returns a new sorted list.
"""
from __future__ import annotations

from auto_client_acquisition.full_ops.work_item import Priority, WorkItem

_PRIORITY_RANK: dict[Priority, int] = {"p0": 0, "p1": 1, "p2": 2, "p3": 3}


def prioritize(items: list[WorkItem]) -> list[WorkItem]:
    """Return items sorted by (priority, has_risk, age, id)."""
    return sorted(
        items,
        key=lambda it: (
            _PRIORITY_RANK.get(it.priority, 99),
            0 if it.risk_flags else 1,
            it.created_at,
            it.id,
        ),
    )


def top_n(items: list[WorkItem], n: int) -> list[WorkItem]:
    return prioritize(items)[: max(0, n)]

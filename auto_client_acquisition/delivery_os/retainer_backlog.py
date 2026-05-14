"""Retainer backlog — queue improvements that belong to monthly cadence, not the sprint."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

_BACKLOG: list["RetainerBacklogItem"] = []


@dataclass
class RetainerBacklogItem:
    item_id: str
    engagement_id: str
    title: str
    notes: str
    created_at: str = field(default_factory=lambda: datetime.now(tz=UTC).isoformat())


def enqueue_retainer_backlog_item(
    *,
    item_id: str,
    engagement_id: str,
    title: str,
    notes: str,
) -> RetainerBacklogItem:
    item = RetainerBacklogItem(item_id=item_id, engagement_id=engagement_id, title=title, notes=notes)
    _BACKLOG.append(item)
    return item


def list_retainer_backlog(engagement_id: str | None = None) -> tuple[RetainerBacklogItem, ...]:
    if engagement_id is None:
        return tuple(_BACKLOG)
    return tuple(x for x in _BACKLOG if x.engagement_id == engagement_id)


def clear_retainer_backlog_for_tests() -> None:
    _BACKLOG.clear()


__all__ = [
    "RetainerBacklogItem",
    "clear_retainer_backlog_for_tests",
    "enqueue_retainer_backlog_item",
    "list_retainer_backlog",
]

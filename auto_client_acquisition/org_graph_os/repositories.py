"""Org graph tenant-scoped nodes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class GraphNode:
    node_id: str
    tenant_id: str
    node_type: str
    label: str
    created_at: datetime = field(default_factory=_now)


__all__ = ["GraphNode"]

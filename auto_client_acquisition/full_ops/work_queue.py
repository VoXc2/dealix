"""V12 — in-memory WorkItem queue.

Pure local. No DB. Reset between tests via ``_reset()`` (or call
``get_default_queue().clear()`` directly). Multi-tenant safe: items
are partitioned by ``tenant_id``.
"""
from __future__ import annotations

from collections.abc import Iterable
from threading import RLock

from auto_client_acquisition.full_ops.work_item import (
    OSType,
    Priority,
    WorkItem,
    WorkItemStatus,
)


class WorkQueue:
    """Append-only-by-default queue with idempotent insert by item id."""

    def __init__(self) -> None:
        self._items: dict[str, WorkItem] = {}
        self._lock = RLock()

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def add(self, item: WorkItem) -> WorkItem:
        """Insert (or replace by id). Idempotent on repeated id."""
        with self._lock:
            self._items[item.id] = item
        return item

    def add_many(self, items: Iterable[WorkItem]) -> int:
        n = 0
        for it in items:
            self.add(it)
            n += 1
        return n

    def get(self, item_id: str) -> WorkItem | None:
        return self._items.get(item_id)

    def list_all(self, *, tenant_id: str = "dealix") -> list[WorkItem]:
        with self._lock:
            return [
                it for it in self._items.values() if it.tenant_id == tenant_id
            ]

    def list_by_os(
        self, os_type: OSType, *, tenant_id: str = "dealix"
    ) -> list[WorkItem]:
        return [
            it
            for it in self.list_all(tenant_id=tenant_id)
            if it.os_type == os_type
        ]

    def list_by_priority(
        self, priority: Priority, *, tenant_id: str = "dealix"
    ) -> list[WorkItem]:
        return [
            it
            for it in self.list_all(tenant_id=tenant_id)
            if it.priority == priority
        ]

    def list_by_status(
        self, status: WorkItemStatus, *, tenant_id: str = "dealix"
    ) -> list[WorkItem]:
        return [
            it
            for it in self.list_all(tenant_id=tenant_id)
            if it.status == status
        ]

    def mark_status(self, item_id: str, status: WorkItemStatus) -> WorkItem | None:
        with self._lock:
            item = self._items.get(item_id)
            if item is None:
                return None
            updated = item.model_copy(update={"status": status})
            self._items[item_id] = updated
            return updated


_DEFAULT = WorkQueue()


def get_default_queue() -> WorkQueue:
    """Module-level shared queue used by the Daily Command Center."""
    return _DEFAULT


def _reset() -> None:
    """Test-only — wipe the default queue."""
    _DEFAULT.clear()

"""Append-only in-memory control event ledger."""

from __future__ import annotations

from threading import Lock

from auto_client_acquisition.control_plane_os.schemas import ControlEvent


class ControlEventLedger:
    """Thread-safe append-only event ledger (MVP fallback)."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._rows: list[ControlEvent] = []

    def append(self, event: ControlEvent) -> ControlEvent:
        with self._lock:
            self._rows.append(event)
        return event

    def list_by_run(self, *, tenant_id: str, run_id: str) -> list[ControlEvent]:
        with self._lock:
            return [
                row
                for row in self._rows
                if row.tenant_id == tenant_id and row.run_id == run_id
            ]

    def list_by_tenant(self, *, tenant_id: str, limit: int = 200) -> list[ControlEvent]:
        with self._lock:
            rows = [row for row in self._rows if row.tenant_id == tenant_id]
        rows.sort(key=lambda row: row.occurred_at, reverse=True)
        return rows[: max(limit, 0)]

    def clear_for_test(self) -> None:
        with self._lock:
            self._rows.clear()


__all__ = ["ControlEventLedger"]

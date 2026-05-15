"""Postgres ledger interface for production persistence.

Current branch keeps an MVP in-memory implementation as fallback. This class
defines the runtime contract used by repositories and tests.
"""

from __future__ import annotations

from auto_client_acquisition.control_plane_os.ledger import ControlEventLedger
from auto_client_acquisition.control_plane_os.schemas import ControlEvent


class PostgresControlLedger:
    """Repository-compatible adapter with MVP fallback behavior."""

    def __init__(self, dsn: str | None = None) -> None:
        self._dsn = (dsn or "").strip()
        self._fallback = ControlEventLedger()

    @property
    def is_configured(self) -> bool:
        return bool(self._dsn)

    def append(self, event: ControlEvent) -> ControlEvent:
        # TODO: wire SQL persistence when migrations are applied.
        return self._fallback.append(event)

    def list_by_run(self, *, tenant_id: str, run_id: str) -> list[ControlEvent]:
        return self._fallback.list_by_run(tenant_id=tenant_id, run_id=run_id)

    def list_by_tenant(self, *, tenant_id: str, limit: int = 200) -> list[ControlEvent]:
        return self._fallback.list_by_tenant(tenant_id=tenant_id, limit=limit)

    def clear_for_test(self) -> None:
        self._fallback.clear_for_test()


__all__ = ["PostgresControlLedger"]

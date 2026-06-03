"""Postgres JSONB snapshot store for revenue ops autopilot records."""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import JSON, DateTime, String, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
from dealix.revenue_ops_autopilot.store import AutopilotJSONStore, _utcnow_iso


class _AutopilotStoreBase(DeclarativeBase):
    pass


class AutopilotStoreSnapshotORM(_AutopilotStoreBase):
    __tablename__ = "autopilot_store_snapshots"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default="default")
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


def _empty_blob() -> dict[str, Any]:
    return {
        "version": 1,
        "generated_at": _utcnow_iso(),
        "leads": [],
        "opportunities": [],
        "support_tickets": [],
        "evidence_events": [],
        "diagnostics": [],
        "invoice_drafts": [],
    }


class AutopilotPostgresStore(AutopilotJSONStore):
    """Single-row JSONB blob store — same public API as :class:`AutopilotJSONStore`."""

    SNAPSHOT_ID = "default"

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        self._lock = threading.Lock()
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True, pool_pre_ping=True)
        self._engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        if create_tables:
            _AutopilotStoreBase.metadata.create_all(self._engine)
        self._path = Path("/dev/null")

    def _read_raw(self) -> dict[str, Any]:
        with self._lock, self._sessionmaker() as session:
            row = session.get(AutopilotStoreSnapshotORM, self.SNAPSHOT_ID)
            if row is None:
                return _empty_blob()
            data = row.data
            if not isinstance(data, dict):
                return _empty_blob()
            return data

    def _write_atomic(self, data: dict[str, Any]) -> None:
        data["generated_at"] = _utcnow_iso()
        now = datetime.now(UTC)
        with self._lock, self._sessionmaker() as session:
            row = session.get(AutopilotStoreSnapshotORM, self.SNAPSHOT_ID)
            if row is None:
                row = AutopilotStoreSnapshotORM(
                    id=self.SNAPSHOT_ID,
                    data=data,
                    updated_at=now,
                )
                session.add(row)
            else:
                row.data = data
                row.updated_at = now
            session.commit()


def sync_database_url_from_env() -> str | None:
    import os

    raw = os.environ.get("DATABASE_URL", "").strip()
    if not raw:
        try:
            from core.config.settings import get_settings

            raw = getattr(get_settings(), "database_url", "") or ""
        except Exception:
            return None
    if not raw:
        return None
    return sync_sqlalchemy_url(raw)


def reset_autopilot_postgres_tables_for_test(engine: Engine) -> None:
    """Drop autopilot snapshot table (pytest helper)."""
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS autopilot_store_snapshots"))


__all__ = [
    "AutopilotPostgresStore",
    "AutopilotStoreSnapshotORM",
    "reset_autopilot_postgres_tables_for_test",
    "sync_database_url_from_env",
]

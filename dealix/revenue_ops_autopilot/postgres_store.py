"""Postgres JSONB snapshot store for revenue ops autopilot records."""

from __future__ import annotations

import threading
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import JSON, DateTime, String, create_engine, inspect, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.orm.attributes import flag_modified

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
    """Single-row JSON store with transaction-bound mutation semantics."""

    SNAPSHOT_ID = "default"
    _ADVISORY_LOCK_KEY = "dealix:autopilot-store-snapshot:v1"

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = False,
    ) -> None:
        # Reentrant because read helpers can be called from inherited methods.
        self._lock = threading.RLock()
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            connect_args = {"connect_timeout": 3} if url.startswith("postgresql") else {}
            engine = create_engine(
                url, future=True, pool_pre_ping=True, connect_args=connect_args
            )
        self._engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        if create_tables:
            _AutopilotStoreBase.metadata.create_all(self._engine)
        self._path = Path("/dev/null")

    def required_schema_ready(self) -> bool:
        """Read-only check that the Alembic-owned snapshot table already exists."""
        try:
            return inspect(self._engine).has_table(AutopilotStoreSnapshotORM.__tablename__)
        except Exception:
            return False

    def _read_raw(self) -> dict[str, Any]:
        with self._lock, self._sessionmaker() as session:
            row = session.get(AutopilotStoreSnapshotORM, self.SNAPSHOT_ID)
            if row is None:
                return _empty_blob()
            data = row.data
            if not isinstance(data, dict):
                return _empty_blob()
            return deepcopy(data)

    def _write_atomic(self, data: dict[str, Any]) -> None:
        payload = deepcopy(data)
        payload["generated_at"] = _utcnow_iso()
        now = datetime.now(UTC)
        with self._lock, self._sessionmaker() as session, session.begin():
            row = session.get(AutopilotStoreSnapshotORM, self.SNAPSHOT_ID)
            if row is None:
                row = AutopilotStoreSnapshotORM(
                    id=self.SNAPSHOT_ID,
                    data=payload,
                    updated_at=now,
                )
                session.add(row)
            else:
                row.data = payload
                row.updated_at = now
                flag_modified(row, "data")

    def _mutate(self, fn: Any) -> Any:
        """Run read-modify-write in one transaction and one writer lock.

        PostgreSQL uses an advisory transaction lock plus ``FOR UPDATE`` so
        different API workers cannot both accept the same idempotency key or
        overwrite each other's snapshot mutation. SQLite tests rely on the
        process-local RLock because SQLite ignores row-level ``FOR UPDATE``.
        """

        with self._lock, self._sessionmaker() as session, session.begin():
            if self._engine.dialect.name == "postgresql":
                session.execute(
                    text("SELECT pg_advisory_xact_lock(hashtext(:lock_key))"),
                    {"lock_key": self._ADVISORY_LOCK_KEY},
                )
            stmt = (
                select(AutopilotStoreSnapshotORM)
                .where(AutopilotStoreSnapshotORM.id == self.SNAPSHOT_ID)
                .with_for_update()
            )
            row = session.execute(stmt).scalar_one_or_none()
            if row is None:
                data = _empty_blob()
                row = AutopilotStoreSnapshotORM(
                    id=self.SNAPSHOT_ID,
                    data=data,
                    updated_at=datetime.now(UTC),
                )
                session.add(row)
                session.flush()
            else:
                data = deepcopy(row.data) if isinstance(row.data, dict) else _empty_blob()

            out = fn(data)
            data["generated_at"] = _utcnow_iso()
            row.data = data
            row.updated_at = datetime.now(UTC)
            flag_modified(row, "data")
            return out


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

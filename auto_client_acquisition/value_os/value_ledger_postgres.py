"""Postgres persistence for :mod:`auto_client_acquisition.value_os.value_ledger`.

Uses the ``value_ledger_events`` table (Alembic revision ``012``). Tests pass an
in-memory SQLite engine; production passes ``database_url`` derived from
``DATABASE_URL`` (asyncpg → psycopg sync prefix).
"""

from __future__ import annotations

import threading
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, String, Text, create_engine, delete, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url


class _ValueLedgerBase(DeclarativeBase):
    pass


class ValueLedgerEventORM(_ValueLedgerBase):
    __tablename__ = "value_ledger_events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(255), index=True)
    kind: Mapped[str] = mapped_column(String(128))
    amount: Mapped[float] = mapped_column(Float)
    tier: Mapped[str] = mapped_column(String(64))
    source_ref: Mapped[str] = mapped_column(Text, default="")
    confirmation_ref: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


def _row_to_dict(row: ValueLedgerEventORM) -> dict[str, Any]:
    return {
        "event_id": row.event_id,
        "customer_id": row.tenant_id,
        "kind": row.kind,
        "amount": float(row.amount),
        "tier": row.tier,
        "source_ref": row.source_ref or "",
        "confirmation_ref": row.confirmation_ref or "",
        "notes": row.notes or "",
        "occurred_at": row.occurred_at.isoformat() if row.occurred_at else "",
    }


class PostgresValueLedgerStore:
    """SQLAlchemy-backed value ledger (same semantics as JSONL file)."""

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True)
        self._engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        self._lock = threading.Lock()
        if create_tables:
            _ValueLedgerBase.metadata.create_all(self._engine)

    def insert_event(self, row: dict[str, Any]) -> None:
        occurred_raw = str(row.get("occurred_at") or "")
        occurred_at = datetime.fromisoformat(occurred_raw.replace("Z", "+00:00"))
        orm_row = ValueLedgerEventORM(
            event_id=str(row["event_id"]),
            tenant_id=str(row["customer_id"]),
            kind=str(row["kind"]),
            amount=float(row["amount"]),
            tier=str(row["tier"]),
            source_ref=str(row.get("source_ref") or ""),
            confirmation_ref=str(row.get("confirmation_ref") or ""),
            notes=str(row.get("notes") or ""),
            occurred_at=occurred_at,
        )
        with self._lock, self._sessionmaker() as session:
            session.merge(orm_row)
            session.commit()

    def list_events(
        self,
        *,
        customer_id: str | None = None,
        since_days: int | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        stmt = select(ValueLedgerEventORM).order_by(ValueLedgerEventORM.occurred_at.desc())
        if customer_id:
            stmt = stmt.where(ValueLedgerEventORM.tenant_id == customer_id)
        stmt = stmt.limit(max(0, min(limit, 50_000)))
        with self._lock, self._sessionmaker() as session:
            rows = list(session.execute(stmt).scalars().all())
        out = [_row_to_dict(r) for r in rows]
        if since_days is not None:
            from datetime import timedelta, timezone

            cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
            filtered: list[dict[str, Any]] = []
            for ev in out:
                try:
                    ts = datetime.fromisoformat(str(ev["occurred_at"]).replace("Z", "+00:00"))
                except Exception:  # noqa: BLE001
                    continue
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                if ts >= cutoff:
                    filtered.append(ev)
            out = filtered
        out.sort(key=lambda ev: str(ev["occurred_at"]), reverse=True)
        return out[: max(0, limit)]

    def clear_for_test(self, customer_id: str | None = None) -> None:
        with self._lock, self._sessionmaker() as session:
            if customer_id:
                session.execute(delete(ValueLedgerEventORM).where(ValueLedgerEventORM.tenant_id == customer_id))
            else:
                session.execute(delete(ValueLedgerEventORM))
            session.commit()


_engine_singleton: Engine | None = None
_store_singleton: PostgresValueLedgerStore | None = None
_store_lock = threading.Lock()


def _settings_sync_url() -> str | None:
    import os

    raw = os.environ.get("DEALIX_VALUE_LEDGER_SYNC_DATABASE_URL", "").strip()
    if raw:
        return sync_sqlalchemy_url(raw)
    try:
        from core.config.settings import get_settings

        u = getattr(get_settings(), "database_url", "") or ""
        return sync_sqlalchemy_url(u) if u else None
    except Exception:  # noqa: BLE001
        return None


def get_postgres_value_ledger_store() -> PostgresValueLedgerStore | None:
    """Lazy singleton for postgres/dual backends. Returns None if URL unusable."""
    global _engine_singleton, _store_singleton
    url = _settings_sync_url()
    if not url:
        return None
    with _store_lock:
        if _store_singleton is not None:
            return _store_singleton
        try:
            eng = create_engine(url, future=True, pool_pre_ping=True)
            eng.connect().close()
        except Exception:
            return None
        _engine_singleton = eng
        _store_singleton = PostgresValueLedgerStore(engine=_engine_singleton, create_tables=True)
        return _store_singleton


def reset_postgres_value_ledger_singleton_for_test() -> None:
    global _engine_singleton, _store_singleton
    with _store_lock:
        if _store_singleton is not None:
            try:
                _ValueLedgerBase.metadata.drop_all(_store_singleton._engine)
            except Exception:  # noqa: BLE001
                pass
        _engine_singleton = None
        _store_singleton = None


__all__ = [
    "PostgresValueLedgerStore",
    "ValueLedgerEventORM",
    "get_postgres_value_ledger_store",
    "reset_postgres_value_ledger_singleton_for_test",
]

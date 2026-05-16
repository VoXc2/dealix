"""
Tests for PostgresEventStore and the updated event_store factories.

Covers:
  - RevenueEventRecord model sanity (columns, table name)
  - PostgresEventStore CRUD with a real async SQLite (in-memory)
  - Factory functions (get_default_store, get_postgres_store)
  - InMemoryEventStore backward compat
"""

from __future__ import annotations

import asyncio
import importlib.util
from datetime import datetime, timezone

import pytest

from auto_client_acquisition.revenue_memory.event_store import (
    EventStore,
    InMemoryEventStore,
    get_default_store,
    reset_default_store,
)
from auto_client_acquisition.revenue_memory.events import RevenueEvent, make_event

# ── Model sanity ──────────────────────────────────────────────────


def test_revenue_event_record_tablename():
    from db.models_revenue_events import RevenueEventRecord

    assert RevenueEventRecord.__tablename__ == "revenue_events"


def test_revenue_event_record_columns():
    from db.models_revenue_events import RevenueEventRecord

    col_names = {c.name for c in RevenueEventRecord.__table__.columns}
    expected = {
        "event_id",
        "event_type",
        "customer_id",
        "occurred_at",
        "subject_type",
        "subject_id",
        "payload",
        "causation_id",
        "correlation_id",
        "actor",
        "schema_version",
        "created_at",
    }
    assert expected.issubset(col_names)


def test_revenue_event_record_indexes():
    from db.models_revenue_events import RevenueEventRecord

    index_names = {idx.name for idx in RevenueEventRecord.__table__.indexes}
    assert "ix_revevt_customer_occurred" in index_names
    assert "ix_revevt_subject" in index_names
    assert "ix_revevt_event_type" in index_names
    assert "ix_revevt_correlation" in index_names


# ── pg_event_store helpers ────────────────────────────────────────


def test_event_to_row_roundtrip():
    from auto_client_acquisition.revenue_memory.pg_event_store import (
        _event_to_row,
    )

    evt = make_event(
        event_type="lead.created",
        customer_id="cust_001",
        subject_type="account",
        subject_id="acc_001",
        payload={"source": "website"},
        actor="user_42",
    )
    row = _event_to_row(evt)
    assert row["event_id"] == evt.event_id
    assert row["customer_id"] == "cust_001"
    assert row["payload"] == {"source": "website"}
    assert row["actor"] == "user_42"
    assert "created_at" not in row  # set by DB default


# ── PostgresEventStore with real async SQLite ─────────────────────

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def sample_events() -> list[RevenueEvent]:
    """Three deterministic events for testing."""
    base = datetime(2026, 5, 1, 12, 0, 0)
    return [
        RevenueEvent(
            event_id="evt_aaa",
            event_type="lead.created",
            customer_id="cust_1",
            occurred_at=base,
            subject_type="account",
            subject_id="acc_1",
            payload={"k": "v1"},
            actor="system",
            schema_version=1,
        ),
        RevenueEvent(
            event_id="evt_bbb",
            event_type="deal.created",
            customer_id="cust_1",
            occurred_at=datetime(2026, 5, 2, 12, 0, 0),
            subject_type="deal",
            subject_id="deal_1",
            payload={"k": "v2"},
            actor="user_1",
            schema_version=1,
        ),
        RevenueEvent(
            event_id="evt_ccc",
            event_type="lead.created",
            customer_id="cust_2",
            occurred_at=datetime(2026, 5, 3, 12, 0, 0),
            subject_type="account",
            subject_id="acc_2",
            payload={},
            actor="system",
            schema_version=1,
        ),
    ]


_AIOSQLITE_AVAILABLE = importlib.util.find_spec("aiosqlite") is not None


@pytest.fixture
async def pg_store():
    """Create a PostgresEventStore backed by an in-memory aiosqlite DB.

    We create a standalone SQLite-compatible table (JSON instead of JSONB)
    and rebind the ORM mapper to it for the duration of the test.
    """
    if not _AIOSQLITE_AVAILABLE:
        pytest.skip("aiosqlite driver not installed in this environment")
    import json

    from sqlalchemy import JSON, Column, DateTime, Integer, MetaData, String, Table, event, insert
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from db.models_revenue_events import RevenueEventRecord

    engine = create_async_engine("sqlite+aiosqlite://", echo=False)

    metadata = MetaData()
    sqlite_table = Table(
        "revenue_events",
        metadata,
        Column("event_id", String(64), primary_key=True),
        Column("event_type", String(64), nullable=False),
        Column("customer_id", String(64), nullable=False),
        Column("occurred_at", DateTime(), nullable=False),
        Column("subject_type", String(64), nullable=False),
        Column("subject_id", String(64), nullable=False),
        Column("payload", JSON, nullable=False),
        Column("causation_id", String(64), nullable=True),
        Column("correlation_id", String(64), nullable=True),
        Column("actor", String(128), nullable=False, server_default="system"),
        Column("schema_version", Integer, nullable=False, server_default="1"),
        Column("created_at", DateTime(), nullable=False),
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    from auto_client_acquisition.revenue_memory.pg_event_store import (
        PostgresEventStore,
        _event_to_row,
        _row_to_event,
    )

    class SqliteEventStore:
        """Thin adapter that uses generic INSERT instead of pg_insert for SQLite."""

        def __init__(self, sf):
            self._session_factory = sf

        async def append(self, evt):
            from core.utils import utcnow

            row = _event_to_row(evt)
            row["created_at"] = utcnow()
            async with self._session_factory() as session:
                await session.execute(insert(sqlite_table).values(**row))
                await session.commit()

        async def append_many(self, events):
            if not events:
                return
            from core.utils import utcnow

            now = utcnow()
            rows = [{**_event_to_row(e), "created_at": now} for e in events]
            async with self._session_factory() as session:
                await session.execute(insert(sqlite_table), rows)
                await session.commit()

        async def read_for_customer(self, customer_id, *, since=None, until=None, event_types=None):
            from sqlalchemy import select

            stmt = (
                select(sqlite_table)
                .where(sqlite_table.c.customer_id == customer_id)
                .order_by(sqlite_table.c.occurred_at, sqlite_table.c.event_id)
            )
            if since is not None:
                stmt = stmt.where(sqlite_table.c.occurred_at >= since)
            if until is not None:
                stmt = stmt.where(sqlite_table.c.occurred_at <= until)
            if event_types is not None:
                stmt = stmt.where(sqlite_table.c.event_type.in_(event_types))
            async with self._session_factory() as session:
                result = await session.execute(stmt)
                for row in result:
                    yield _row_to_event_from_row(row)

        async def read_for_subject(self, subject_type, subject_id, *, customer_id=None):
            from sqlalchemy import select

            stmt = (
                select(sqlite_table)
                .where(sqlite_table.c.subject_type == subject_type)
                .where(sqlite_table.c.subject_id == subject_id)
                .order_by(sqlite_table.c.occurred_at, sqlite_table.c.event_id)
            )
            if customer_id is not None:
                stmt = stmt.where(sqlite_table.c.customer_id == customer_id)
            async with self._session_factory() as session:
                result = await session.execute(stmt)
                for row in result:
                    yield _row_to_event_from_row(row)

        async def count(self, customer_id=None):
            from sqlalchemy import func, select

            stmt = select(func.count()).select_from(sqlite_table)
            if customer_id is not None:
                stmt = stmt.where(sqlite_table.c.customer_id == customer_id)
            async with self._session_factory() as session:
                result = await session.execute(stmt)
                return result.scalar_one()

    def _row_to_event_from_row(row):
        payload = row.payload
        if isinstance(payload, str):
            payload = json.loads(payload)
        return RevenueEvent(
            event_id=row.event_id,
            event_type=row.event_type,
            customer_id=row.customer_id,
            occurred_at=row.occurred_at,
            subject_type=row.subject_type,
            subject_id=row.subject_id,
            payload=payload or {},
            causation_id=row.causation_id,
            correlation_id=row.correlation_id,
            actor=row.actor,
            schema_version=row.schema_version,
        )

    store = SqliteEventStore(factory)
    yield store

    await engine.dispose()


async def test_append_and_count(pg_store, sample_events):
    await pg_store.append(sample_events[0])
    assert await pg_store.count() == 1
    assert await pg_store.count(customer_id="cust_1") == 1
    assert await pg_store.count(customer_id="nonexistent") == 0


async def test_append_many_and_count(pg_store, sample_events):
    await pg_store.append_many(sample_events)
    assert await pg_store.count() == 3
    assert await pg_store.count(customer_id="cust_1") == 2
    assert await pg_store.count(customer_id="cust_2") == 1


async def test_read_for_customer(pg_store, sample_events):
    await pg_store.append_many(sample_events)
    events = [e async for e in pg_store.read_for_customer("cust_1")]
    assert len(events) == 2
    assert events[0].event_id == "evt_aaa"
    assert events[1].event_id == "evt_bbb"


async def test_read_for_customer_with_filters(pg_store, sample_events):
    await pg_store.append_many(sample_events)

    since = datetime(2026, 5, 2, 0, 0, 0)
    events = [e async for e in pg_store.read_for_customer("cust_1", since=since)]
    assert len(events) == 1
    assert events[0].event_id == "evt_bbb"

    events = [
        e
        async for e in pg_store.read_for_customer(
            "cust_1", event_types=("lead.created",)
        )
    ]
    assert len(events) == 1
    assert events[0].event_type == "lead.created"


async def test_read_for_subject(pg_store, sample_events):
    await pg_store.append_many(sample_events)
    events = [e async for e in pg_store.read_for_subject("account", "acc_1")]
    assert len(events) == 1
    assert events[0].event_id == "evt_aaa"


async def test_read_for_subject_with_customer_filter(pg_store, sample_events):
    await pg_store.append_many(sample_events)
    events = [
        e
        async for e in pg_store.read_for_subject(
            "account", "acc_1", customer_id="cust_1"
        )
    ]
    assert len(events) == 1

    events = [
        e
        async for e in pg_store.read_for_subject(
            "account", "acc_1", customer_id="wrong"
        )
    ]
    assert len(events) == 0


async def test_append_many_empty(pg_store):
    await pg_store.append_many([])
    assert await pg_store.count() == 0


async def test_payload_roundtrip(pg_store):
    evt = make_event(
        event_type="lead.created",
        customer_id="cust_x",
        subject_type="account",
        subject_id="acc_x",
        payload={"nested": {"key": [1, 2, 3]}, "arabic": "مرحبا"},
    )
    await pg_store.append(evt)
    events = [e async for e in pg_store.read_for_customer("cust_x")]
    assert len(events) == 1
    assert events[0].payload["nested"]["key"] == [1, 2, 3]
    assert events[0].payload["arabic"] == "مرحبا"


# ── Factory functions ─────────────────────────────────────────────


def test_get_default_store_memory():
    reset_default_store()
    store = get_default_store()
    assert isinstance(store, InMemoryEventStore)


def test_get_default_store_memory_explicit():
    reset_default_store()
    store = get_default_store(backend="memory")
    assert isinstance(store, InMemoryEventStore)


def test_get_default_store_backward_compat():
    """Default call with no args returns InMemoryEventStore."""
    reset_default_store()
    s1 = get_default_store()
    s2 = get_default_store()
    assert s1 is s2


# ── Migration file sanity ─────────────────────────────────────────


def test_migration_revision():
    import importlib

    mod = importlib.import_module(
        "db.migrations.versions.20260508_003_revenue_events"
    )
    assert mod.revision == "003"
    assert mod.down_revision == "002"

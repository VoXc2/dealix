"""
PostgreSQL-backed EventStore using SQLAlchemy 2.0 async.
مخزن أحداث مدعوم بـ PostgreSQL — التنفيذ الإنتاجي لذاكرة الإيرادات.

Implements the EventStore protocol with real database persistence.
Append-only: no update or delete methods exposed.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from auto_client_acquisition.revenue_memory.events import RevenueEvent
from db.models_revenue_events import RevenueEventRecord


def _event_to_row(event: RevenueEvent) -> dict[str, Any]:
    """Convert a RevenueEvent dataclass to a dict suitable for INSERT."""
    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "customer_id": event.customer_id,
        "occurred_at": event.occurred_at,
        "subject_type": event.subject_type,
        "subject_id": event.subject_id,
        "tenant_id": event.tenant_id,
        "payload": event.payload,
        "causation_id": event.causation_id,
        "correlation_id": event.correlation_id,
        "actor": event.actor,
        "schema_version": event.schema_version,
    }


def _row_to_event(row: RevenueEventRecord) -> RevenueEvent:
    """Reconstitute a RevenueEvent from a DB row."""
    return RevenueEvent(
        event_id=row.event_id,
        event_type=row.event_type,
        customer_id=row.customer_id,
        occurred_at=row.occurred_at,
        subject_type=row.subject_type,
        subject_id=row.subject_id,
        payload=row.payload or {},
        causation_id=row.causation_id,
        correlation_id=row.correlation_id,
        actor=row.actor,
        tenant_id=getattr(row, "tenant_id", None),
        schema_version=row.schema_version,
    )


class PostgresEventStore:
    """
    Production EventStore backed by PostgreSQL (revenue_events table).

    All methods are async. Satisfies the EventStore protocol with async variants.
    Uses the shared async session factory from db.session.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def append(self, event: RevenueEvent) -> None:
        """Persist a single event."""
        async with self._session_factory() as session:
            stmt = pg_insert(RevenueEventRecord).values(**_event_to_row(event))
            await session.execute(stmt)
            await session.commit()

    async def append_many(self, events: list[RevenueEvent]) -> None:
        """Persist a batch of events in a single transaction."""
        if not events:
            return
        async with self._session_factory() as session:
            rows = [_event_to_row(e) for e in events]
            await session.execute(pg_insert(RevenueEventRecord), rows)
            await session.commit()

    async def read_for_customer(
        self,
        customer_id: str,
        *,
        since: datetime | None = None,
        until: datetime | None = None,
        event_types: tuple[str, ...] | None = None,
        tenant_id: str | None = None,
    ) -> AsyncIterator[RevenueEvent]:
        """Yield events for a customer, ordered by (occurred_at, event_id)."""
        stmt = (
            select(RevenueEventRecord)
            .where(RevenueEventRecord.customer_id == customer_id)
            .order_by(RevenueEventRecord.occurred_at, RevenueEventRecord.event_id)
        )
        if tenant_id is not None:
            stmt = stmt.where(RevenueEventRecord.tenant_id == tenant_id)
        if since is not None:
            stmt = stmt.where(RevenueEventRecord.occurred_at >= since)
        if until is not None:
            stmt = stmt.where(RevenueEventRecord.occurred_at <= until)
        if event_types is not None:
            stmt = stmt.where(RevenueEventRecord.event_type.in_(event_types))

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            for row in result.scalars():
                yield _row_to_event(row)

    async def read_for_subject(
        self,
        subject_type: str,
        subject_id: str,
        *,
        customer_id: str | None = None,
        tenant_id: str | None = None,
    ) -> AsyncIterator[RevenueEvent]:
        """Yield events for a subject entity, ordered by (occurred_at, event_id)."""
        stmt = (
            select(RevenueEventRecord)
            .where(
                RevenueEventRecord.subject_type == subject_type,
                RevenueEventRecord.subject_id == subject_id,
            )
            .order_by(RevenueEventRecord.occurred_at, RevenueEventRecord.event_id)
        )
        if customer_id is not None:
            stmt = stmt.where(RevenueEventRecord.customer_id == customer_id)
        if tenant_id is not None:
            stmt = stmt.where(RevenueEventRecord.tenant_id == tenant_id)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            for row in result.scalars():
                yield _row_to_event(row)

    async def count(
        self,
        customer_id: str | None = None,
        *,
        tenant_id: str | None = None,
    ) -> int:
        """Return total event count, optionally filtered by customer_id."""
        stmt = select(func.count()).select_from(RevenueEventRecord)
        if customer_id is not None:
            stmt = stmt.where(RevenueEventRecord.customer_id == customer_id)
        if tenant_id is not None:
            stmt = stmt.where(RevenueEventRecord.tenant_id == tenant_id)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar_one()

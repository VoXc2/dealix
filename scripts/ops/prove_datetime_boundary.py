"""Ephemeral PostgreSQL proof for Dealix's datetime persistence boundary.

The proof uses only the disposable DATABASE_URL supplied by CI.  It validates
both the isolated type contract and representative real Dealix ORM models.
Nothing here is safe to point at production, so an explicit ephemeral guard is
required.
"""

from __future__ import annotations

import asyncio
import os
import sys
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alembic.migration import MigrationContext
from sqlalchemy import Column, DateTime, inspect, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Import the db package first so its legacy datetime listener is installed
# before real mapped models are registered.
import db
from db.datetime_types import UTCNaiveDateTime
from db.models import (
    CustomerRecord,
    DealRecord,
    EmailSendLog,
    LeadRecord,
    OutreachQueueRecord,
    TaskRecord,
    TenantRecord,
)
from db.models_commercial_intelligence import CommercialSourceRecord


class ProofBase(DeclarativeBase):
    type_annotation_map = {datetime: UTCNaiveDateTime()}


class TimestampBoundaryProof(ProofBase):
    __tablename__ = "_dealix_datetime_boundary_proof"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    assigned_at: Mapped[datetime]
    explicit_aware_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


REAL_TABLES = [
    TenantRecord.__table__,
    LeadRecord.__table__,
    DealRecord.__table__,
    CustomerRecord.__table__,
    OutreachQueueRecord.__table__,
    TaskRecord.__table__,
    EmailSendLog.__table__,
]


def _drop_real_tables(sync_conn) -> None:
    """Drop only the representative ephemeral tables used by this proof."""
    db.models.Base.metadata.drop_all(sync_conn, tables=REAL_TABLES)


def _create_real_tables(sync_conn) -> None:
    """Create only the representative ephemeral tables used by this proof."""
    db.models.Base.metadata.create_all(sync_conn, tables=REAL_TABLES)


def _assert_model_mapping_contract() -> None:
    legacy = [
        TenantRecord.__table__.c.created_at,
        LeadRecord.__table__.c.created_at,
        DealRecord.__table__.c.created_at,
        CustomerRecord.__table__.c.created_at,
        OutreachQueueRecord.__table__.c.created_at,
        TaskRecord.__table__.c.due_at,
        EmailSendLog.__table__.c.created_at,
    ]
    for column in legacy:
        if not isinstance(column.type, UTCNaiveDateTime):
            raise AssertionError(
                f"legacy column not normalized: {column.table.name}.{column.name}={column.type!r}"
            )
        if getattr(column.type.impl, "timezone", None) is not False:
            raise AssertionError(
                f"legacy physical type changed: {column.table.name}.{column.name}"
            )

    explicit = CommercialSourceRecord.__table__.c.created_at.type
    if isinstance(explicit, UTCNaiveDateTime):
        raise AssertionError("explicit timezone-aware commercial timestamp was rewritten")
    if not isinstance(explicit, DateTime) or explicit.timezone is not True:
        raise AssertionError(f"unexpected explicit aware type: {explicit!r}")


async def _prove_isolated_type(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(ProofBase.metadata.drop_all)
        await conn.run_sync(ProofBase.metadata.create_all)
        rows = (
            await conn.execute(
                text(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = '_dealix_datetime_boundary_proof'
                    ORDER BY column_name
                    """
                )
            )
        ).all()
        types = dict(rows)
        if types.get("created_at") != "timestamp without time zone":
            raise AssertionError(f"unexpected legacy DB type: {types.get('created_at')}")
        if types.get("explicit_aware_at") != "timestamp with time zone":
            raise AssertionError(
                f"explicit timezone-aware type changed: {types.get('explicit_aware_at')}"
            )

    source = datetime(2026, 8, 13, 4, 30, tzinfo=timezone(timedelta(hours=3)))
    expected_naive_utc = source.astimezone(UTC).replace(tzinfo=None)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        row = TimestampBoundaryProof(
            id=1,
            assigned_at=source,
            explicit_aware_at=source,
        )
        session.add(row)
        await session.commit()
        session.expunge_all()
        loaded = await session.get(TimestampBoundaryProof, 1)
        assert loaded is not None
        if loaded.assigned_at.tzinfo is not None:
            raise AssertionError("legacy ORM read semantics unexpectedly became timezone-aware")
        if loaded.assigned_at != expected_naive_utc:
            raise AssertionError(f"bind normalization mismatch: {loaded.assigned_at!r}")
        if loaded.created_at.tzinfo is not None:
            raise AssertionError("legacy default read semantics unexpectedly became timezone-aware")
        if loaded.explicit_aware_at is None or loaded.explicit_aware_at.tzinfo is None:
            raise AssertionError("explicit timezone-aware column lost timezone information")


async def _prove_real_models(engine) -> None:
    # Create only the representative tables needed for this proof.  This avoids
    # treating create_all() as a production migration mechanism.
    async with engine.begin() as conn:
        await conn.run_sync(_drop_real_tables)
        await conn.run_sync(_create_real_tables)

    Session = async_sessionmaker(engine, expire_on_commit=False)
    aware = datetime(2026, 8, 13, 8, 0, tzinfo=timezone(timedelta(hours=3)))

    # Persist the ownership parents in separate committed transactions.  This
    # proof targets datetime binding; it must not depend on unit-of-work insert
    # ordering for objects that do not have explicit relationship assignments.
    async with Session() as session:
        session.add(TenantRecord(id="tenant_dt", name="Datetime Proof", slug="datetime-proof"))
        await session.commit()

    async with Session() as session:
        persisted_tenant = await session.get(TenantRecord, "tenant_dt")
        if persisted_tenant is None:
            raise AssertionError("datetime proof tenant parent was not persisted")
        if persisted_tenant.created_at.tzinfo is not None:
            raise AssertionError(
                f"legacy tenant.created_at read became aware: {persisted_tenant.created_at!r}"
            )

    async with Session() as session:
        session.add(
            LeadRecord(
                id="lead_dt",
                tenant_id="tenant_dt",
                source="proof",
                company_name="Proof Co",
            )
        )
        await session.commit()

    async with Session() as session:
        persisted_lead = await session.get(LeadRecord, "lead_dt")
        if persisted_lead is None:
            raise AssertionError("datetime proof lead parent was not persisted")
        session.add(DealRecord(id="deal_dt", tenant_id="tenant_dt", lead_id="lead_dt"))
        await session.commit()

    async with Session() as session:
        session.add(CustomerRecord(id="customer_dt", updated_at=aware))
        await session.commit()

    async with Session() as session:
        session.add(
            OutreachQueueRecord(
                id="outreach_dt",
                lead_id="lead_dt",
                channel="email",
                message="proof only",
                due_at=aware,
            )
        )
        await session.commit()

    async with Session() as session:
        session.add(
            TaskRecord(
                id="task_dt",
                lead_id="lead_dt",
                task_type="proof",
                due_at=aware,
            )
        )
        await session.commit()

    async with Session() as session:
        session.add(
            EmailSendLog(
                id="email_dt",
                account_id=None,
                queue_id="outreach_dt",
                to_email="proof@example.invalid",
                subject="proof",
                created_at=aware,
                updated_at=aware,
            )
        )
        await session.commit()

    async with Session() as session:
        loaded_tenant = await session.get(TenantRecord, "tenant_dt")
        loaded_customer = await session.get(CustomerRecord, "customer_dt")
        loaded_task = await session.get(TaskRecord, "task_dt")
        loaded_email = await session.get(EmailSendLog, "email_dt")
        for label, value in [
            ("tenant.created_at", loaded_tenant.created_at if loaded_tenant else None),
            ("customer.updated_at", loaded_customer.updated_at if loaded_customer else None),
            ("task.due_at", loaded_task.due_at if loaded_task else None),
            ("email.created_at", loaded_email.created_at if loaded_email else None),
        ]:
            if value is None:
                raise AssertionError(f"missing real-model timestamp: {label}")
            if value.tzinfo is not None:
                raise AssertionError(f"legacy real-model read became aware: {label}={value!r}")

    async with engine.begin() as conn:
        table_names = [table.name for table in REAL_TABLES]
        rows = (
            await conn.execute(
                text(
                    """
                    SELECT table_name, column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = ANY(:table_names)
                      AND column_name IN ('created_at', 'updated_at', 'due_at')
                    """
                ),
                {"table_names": table_names},
            )
        ).all()
        for table_name, column_name, data_type in rows:
            if data_type != "timestamp without time zone":
                raise AssertionError(
                    f"unexpected physical type {table_name}.{column_name}={data_type}"
                )


def _compare_reflected_types(sync_conn) -> None:
    """Assert Alembic sees no model-vs-database type drift from the decorator."""
    inspector = inspect(sync_conn)
    migration_context = MigrationContext.configure(sync_conn)

    tenants = {item["name"]: item["type"] for item in inspector.get_columns("tenants")}
    proof = {
        item["name"]: item["type"]
        for item in inspector.get_columns("_dealix_datetime_boundary_proof")
    }

    comparisons = [
        (
            "tenants.created_at",
            Column("created_at", tenants["created_at"]),
            TenantRecord.__table__.c.created_at,
        ),
        (
            "proof.created_at",
            Column("created_at", proof["created_at"]),
            TimestampBoundaryProof.__table__.c.created_at,
        ),
        (
            "proof.explicit_aware_at",
            Column("explicit_aware_at", proof["explicit_aware_at"]),
            TimestampBoundaryProof.__table__.c.explicit_aware_at,
        ),
    ]
    for label, reflected_column, model_column in comparisons:
        if migration_context.impl.compare_type(reflected_column, model_column):
            raise AssertionError(
                f"Alembic would emit unexpected type drift for {label}: "
                f"db={reflected_column.type!r} model={model_column.type!r}"
            )


async def _prove_alembic_type_compatibility(engine) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(_compare_reflected_types)


async def main() -> int:
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if not database_url:
        raise SystemExit("DATABASE_URL is required")
    if os.environ.get("DEALIX_DATETIME_PROOF_EPHEMERAL") != "1":
        raise SystemExit("Refusing: DEALIX_DATETIME_PROOF_EPHEMERAL=1 is required")

    _assert_model_mapping_contract()
    engine = create_async_engine(database_url)
    try:
        await _prove_isolated_type(engine)
        await _prove_real_models(engine)
        await _prove_alembic_type_compatibility(engine)
        print("DATETIME_BOUNDARY_POSTGRES=PASS")
        print("LEGACY_DB_TYPE=timestamp without time zone")
        print("LEGACY_PYTHON_READ=naive_utc")
        print("AWARE_INPUT_NORMALIZED=true")
        print("EXPLICIT_TIMEZONE_COLUMNS_PRESERVED=true")
        print("ALEMBIC_TYPE_DRIFT=false")
        print("REAL_MODEL_PATHS=7")
        print("DDL_REQUIRED=false")
    finally:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(ProofBase.metadata.drop_all)
                await conn.run_sync(_drop_real_tables)
        finally:
            await engine.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

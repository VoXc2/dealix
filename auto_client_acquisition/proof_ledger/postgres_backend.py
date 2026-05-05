"""Postgres-backed implementation of the proof ledger.

Mirrors :class:`auto_client_acquisition.proof_ledger.file_backend.FileProofLedger`
byte-for-byte at the public-API level so callers can swap backends without
behavioural change. Storage uses SQLAlchemy 2.0 (works with sqlite for tests
and Postgres in production — no driver-specific code in this module).

Hard contract (must match the file backend):
  * PII redaction happens **before** insert. Raw summary fields are stored
    only as the caller supplied them (we do not store an unredacted form
    that did not exist on the input event); the redacted variants are
    always written.
  * Customer handle anonymization on read is the export layer's job
    (``evidence_export.py``), NOT this storage layer.
  * Public methods: ``record``, ``list_events``, ``record_unit``, ``list_units``.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Engine,
    Float,
    Integer,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.proof_ledger.schemas import (
    ProofEvent,
    RevenueWorkUnit,
)


class ProofLedgerBase(DeclarativeBase):
    """Dedicated declarative base for proof-ledger ORM tables.

    Kept separate from ``db.models.Base`` so the proof ledger can be
    bootstrapped against an in-memory SQLite engine in tests without
    pulling the entire app schema along for the ride.
    """


class ProofEventORM(ProofLedgerBase):
    """SQLAlchemy mapping for :class:`ProofEvent`."""

    __tablename__ = "proof_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    customer_handle: Mapped[str] = mapped_column(String(255), index=True, default="Saudi B2B customer")
    service_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    summary_ar: Mapped[str] = mapped_column(Text, default="")
    summary_en: Mapped[str] = mapped_column(Text, default="")
    evidence_source: Mapped[str] = mapped_column(String(255), default="")
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    consent_for_publication: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    redacted_summary_ar: Mapped[str] = mapped_column(Text, default="")
    redacted_summary_en: Mapped[str] = mapped_column(Text, default="")
    approval_status: Mapped[str] = mapped_column(String(32), default="approval_required", index=True)
    risk_level: Mapped[str] = mapped_column(String(16), default="low", index=True)
    payload: Mapped[dict] = mapped_column("payload_json", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )


class RevenueWorkUnitORM(ProofLedgerBase):
    """SQLAlchemy mapping for :class:`RevenueWorkUnit`."""

    __tablename__ = "proof_revenue_work_units"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    unit_type: Mapped[str] = mapped_column(String(64), index=True)
    customer_handle: Mapped[str] = mapped_column(String(255), index=True, default="Saudi B2B customer")
    service_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    description: Mapped[str] = mapped_column(Text, default="")
    proof_event_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )


def _orm_to_event(row: ProofEventORM) -> ProofEvent:
    return ProofEvent.model_validate({
        "id": row.id,
        "event_type": row.event_type,
        "customer_handle": row.customer_handle,
        "service_id": row.service_id,
        "summary_ar": row.summary_ar or "",
        "summary_en": row.summary_en or "",
        "evidence_source": row.evidence_source or "",
        "confidence": row.confidence,
        "consent_for_publication": row.consent_for_publication,
        "redacted_summary_ar": row.redacted_summary_ar or "",
        "redacted_summary_en": row.redacted_summary_en or "",
        "approval_status": row.approval_status,
        "risk_level": row.risk_level,
        "payload": row.payload or {},
        "created_at": row.created_at,
    })


def _orm_to_unit(row: RevenueWorkUnitORM) -> RevenueWorkUnit:
    return RevenueWorkUnit.model_validate({
        "id": row.id,
        "unit_type": row.unit_type,
        "customer_handle": row.customer_handle,
        "service_id": row.service_id,
        "quantity": row.quantity,
        "description": row.description or "",
        "proof_event_id": row.proof_event_id,
        "created_at": row.created_at,
    })


class PostgresProofLedger:
    """SQLAlchemy-backed proof ledger.

    Same public surface as :class:`FileProofLedger`. Engine is supplied by
    the caller — the factory wires Postgres in production; tests pass a
    sqlite in-memory engine.
    """

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
        self._engine: Engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        self._lock = threading.Lock()
        if create_tables:
            ProofLedgerBase.metadata.create_all(self._engine)

    # ─── ProofEvents ────────────────────────────────────────────

    def record(self, event: ProofEvent) -> ProofEvent:
        """Persist one event with redaction. Returns the stored event.

        Mirrors :meth:`FileProofLedger.record`: redacted summaries are
        computed at write time and persisted alongside the raw fields.
        """
        ar_redacted = redact_text(event.summary_ar) if event.summary_ar else ""
        en_redacted = redact_text(event.summary_en) if event.summary_en else ""

        stored = event.model_copy(update={
            "redacted_summary_ar": ar_redacted,
            "redacted_summary_en": en_redacted,
        })

        row = ProofEventORM(
            id=stored.id,
            event_type=str(stored.event_type),
            customer_handle=stored.customer_handle,
            service_id=stored.service_id,
            summary_ar=stored.summary_ar or "",
            summary_en=stored.summary_en or "",
            evidence_source=stored.evidence_source or "",
            confidence=stored.confidence,
            consent_for_publication=stored.consent_for_publication,
            redacted_summary_ar=stored.redacted_summary_ar or "",
            redacted_summary_en=stored.redacted_summary_en or "",
            approval_status=stored.approval_status,
            risk_level=stored.risk_level,
            payload=dict(stored.payload or {}),
            created_at=stored.created_at,
        )

        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
        return stored

    def list_events(
        self,
        *,
        customer_handle: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[ProofEvent]:
        """Return recent events, newest first, with optional filters."""
        stmt = select(ProofEventORM).order_by(ProofEventORM.created_at.desc())
        if customer_handle is not None:
            stmt = stmt.where(ProofEventORM.customer_handle == customer_handle)
        if event_type is not None:
            stmt = stmt.where(ProofEventORM.event_type == event_type)
        stmt = stmt.limit(limit)
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_orm_to_event(r) for r in rows]

    # ─── RevenueWorkUnits ───────────────────────────────────────

    def record_unit(self, unit: RevenueWorkUnit) -> RevenueWorkUnit:
        row = RevenueWorkUnitORM(
            id=unit.id,
            unit_type=str(unit.unit_type),
            customer_handle=unit.customer_handle,
            service_id=unit.service_id,
            quantity=unit.quantity,
            description=unit.description or "",
            proof_event_id=unit.proof_event_id,
            created_at=unit.created_at,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
        return unit

    def list_units(
        self,
        *,
        customer_handle: str | None = None,
        unit_type: str | None = None,
        limit: int = 100,
    ) -> list[RevenueWorkUnit]:
        stmt = select(RevenueWorkUnitORM).order_by(RevenueWorkUnitORM.created_at.desc())
        if customer_handle is not None:
            stmt = stmt.where(RevenueWorkUnitORM.customer_handle == customer_handle)
        if unit_type is not None:
            stmt = stmt.where(RevenueWorkUnitORM.unit_type == unit_type)
        stmt = stmt.limit(limit)
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_orm_to_unit(r) for r in rows]

    # ─── Test helpers ───────────────────────────────────────────

    def clear(self) -> None:
        """Test-only: drop and recreate the ledger tables."""
        with self._lock:
            ProofLedgerBase.metadata.drop_all(self._engine)
            ProofLedgerBase.metadata.create_all(self._engine)


__all__: list[str] = [
    "PostgresProofLedger",
    "ProofEventORM",
    "RevenueWorkUnitORM",
    "ProofLedgerBase",
]

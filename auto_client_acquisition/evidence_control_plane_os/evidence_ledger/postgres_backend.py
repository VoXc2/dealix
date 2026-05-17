"""Postgres-backed implementation of the append-only Evidence Events ledger.

Mirrors :class:`FileEvidenceLedger` at the public-API level. Storage uses
SQLAlchemy 2.0 (sqlite for tests, Postgres in production).

Hard contract:
  * Append-only — only ``append`` writes; there is no update or delete
    method, and the ORM table carries no ``updated_at`` / ``deleted_at``.
  * PII redaction happens **before** insert (``summary`` field).
  * Each row carries an HMAC ``signature`` over its canonical metadata,
    computed via ``proof_ledger/hmac_signing.py``.
"""
from __future__ import annotations

import os
import threading
from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Engine,
    Float,
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
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.schemas import (
    EvidenceEvent,
)
from auto_client_acquisition.proof_ledger.hmac_signing import sign_pack_metadata


class EvidenceLedgerBase(DeclarativeBase):
    """Dedicated declarative base for the evidence ledger ORM table.

    Kept separate from ``db.models.Base`` so the ledger can be bootstrapped
    against an in-memory SQLite engine in tests.
    """


class EvidenceEventORM(EvidenceLedgerBase):
    """SQLAlchemy mapping for :class:`EvidenceEvent` — append-only."""

    __tablename__ = "evidence_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    source: Mapped[str] = mapped_column(String(255), index=True)
    summary: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    linked_asset: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    actor: Mapped[str] = mapped_column(String(128), index=True)
    signature: Mapped[str] = mapped_column(String(128), default="UNSIGNED")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )


def _signing_secret() -> str | None:
    return os.getenv("DEALIX_EVIDENCE_LEDGER_SECRET") or None


def _signature_payload(event: EvidenceEvent) -> dict[str, object]:
    return {
        "id": event.id,
        "event_type": event.event_type,
        "source": event.source,
        "summary": event.summary,
        "confidence": event.confidence,
        "approval_required": event.approval_required,
        "linked_asset": event.linked_asset,
        "actor": event.actor,
        "created_at": event.created_at.isoformat(),
    }


def _orm_to_event(row: EvidenceEventORM) -> EvidenceEvent:
    return EvidenceEvent.model_validate(
        {
            "id": row.id,
            "event_type": row.event_type,
            "source": row.source,
            "summary": row.summary or "",
            "confidence": row.confidence,
            "approval_required": row.approval_required,
            "linked_asset": row.linked_asset,
            "actor": row.actor,
            "created_at": row.created_at,
        }
    )


class PostgresEvidenceLedger:
    """SQLAlchemy-backed append-only evidence ledger."""

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
            EvidenceLedgerBase.metadata.create_all(self._engine)

    def append(self, event: EvidenceEvent) -> EvidenceEvent:
        """Persist one evidence event with redacted summary + HMAC signature."""
        stored = event.model_copy(update={"summary": redact_text(event.summary or "")})
        signature = sign_pack_metadata(_signature_payload(stored), _signing_secret())
        row = EvidenceEventORM(
            id=stored.id,
            event_type=stored.event_type,
            source=stored.source,
            summary=stored.summary or "",
            confidence=stored.confidence,
            approval_required=stored.approval_required,
            linked_asset=stored.linked_asset,
            actor=stored.actor,
            signature=signature,
            created_at=stored.created_at,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
        return stored

    def list_events(
        self,
        *,
        event_type: str | None = None,
        source: str | None = None,
        limit: int = 200,
    ) -> list[EvidenceEvent]:
        """Return recent events, newest first, with optional filters."""
        stmt = select(EvidenceEventORM).order_by(EvidenceEventORM.created_at.desc())
        if event_type is not None:
            stmt = stmt.where(EvidenceEventORM.event_type == event_type)
        if source is not None:
            stmt = stmt.where(EvidenceEventORM.source == source)
        stmt = stmt.limit(limit)
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_orm_to_event(r) for r in rows]

    def get(self, event_id: str) -> EvidenceEvent | None:
        """Fetch one event by id, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(EvidenceEventORM, event_id)
        return _orm_to_event(row) if row is not None else None

    def verify(self, event: EvidenceEvent) -> bool:
        """Recompute the signature and compare against the stored row."""
        expected = sign_pack_metadata(_signature_payload(event), _signing_secret())
        with self._lock, self._sessionmaker() as session:
            row = session.get(EvidenceEventORM, event.id)
        return row is not None and row.signature == expected

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the ledger table."""
        with self._lock:
            EvidenceLedgerBase.metadata.drop_all(self._engine)
            EvidenceLedgerBase.metadata.create_all(self._engine)


__all__ = [
    "EvidenceLedgerBase",
    "EvidenceEventORM",
    "PostgresEvidenceLedger",
]

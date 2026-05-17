"""Postgres-backed append-only Decision Passport store.

Append-only by construction: only ``add`` writes; there is no update or
delete method. Every stored passport carries explicit ``source`` +
approval (``approved_by`` / ``approved_at``) — all NOT NULL — and an
HMAC ``signature`` over its canonical metadata.

``validate_passport()`` is run before any write — a passport with an
empty ``proof_target`` or ``owner`` never reaches the store.
"""
from __future__ import annotations

import os
import threading
from datetime import UTC, datetime

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from auto_client_acquisition.decision_passport.schema import (
    DecisionPassport,
    validate_passport,
)
from auto_client_acquisition.proof_ledger.hmac_signing import sign_pack_metadata
from db.models import Base, DecisionPassportRecord


class PassportPersistenceError(Exception):
    """Raised when a passport cannot be persisted (validation or governance)."""


def _signing_secret() -> str | None:
    return os.getenv("DEALIX_DECISION_PASSPORT_SECRET") or None


def _signature_payload(passport: DecisionPassport) -> dict[str, object]:
    return {
        "lead_id": passport.lead_id,
        "company": passport.company,
        "source": passport.source,
        "proof_target": passport.proof_target,
        "owner": str(passport.owner),
        "priority_bucket": str(passport.priority_bucket),
        "measurable_impact": passport.measurable_impact,
        "evidence_event_ids": list(passport.evidence_event_ids),
    }


def _row_to_passport(row: DecisionPassportRecord) -> DecisionPassport:
    return DecisionPassport.model_validate(row.passport_json)


class PostgresPassportStore:
    """SQLAlchemy-backed append-only Decision Passport store."""

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
            DecisionPassportRecord.__table__.create(self._engine, checkfirst=True)

    def add(
        self,
        passport: DecisionPassport,
        *,
        tenant_id: str | None = None,
        passport_id: str | None = None,
    ) -> str:
        """Validate + persist one passport. Returns the stored row id.

        Raises :class:`PassportPersistenceError` when ``validate_passport``
        fails or the passport carries no explicit source / approval.
        """
        try:
            validate_passport(passport)
        except Exception as exc:  # noqa: BLE001
            raise PassportPersistenceError(f"passport validation failed: {exc}") from exc
        if not passport.source or not passport.source.strip():
            raise PassportPersistenceError("passport source is mandatory")
        if passport.approval is None:
            raise PassportPersistenceError("passport approval is mandatory before persistence")

        row_id = passport_id or f"dp_{passport.lead_id}_{int(datetime.now(UTC).timestamp() * 1000)}"
        signature = sign_pack_metadata(_signature_payload(passport), _signing_secret())
        row = DecisionPassportRecord(
            id=row_id,
            tenant_id=tenant_id,
            lead_id=passport.lead_id,
            company=passport.company,
            schema_version=passport.schema_version,
            source=passport.source,
            approved_by=passport.approval.approver,
            approved_at=passport.approval.approved_at,
            proof_target=passport.proof_target,
            owner=str(passport.owner),
            priority_bucket=str(passport.priority_bucket),
            measurable_impact=passport.measurable_impact,
            evidence_event_ids=list(passport.evidence_event_ids),
            signature=signature,
            passport_json=passport.model_dump(mode="json"),
            created_at=datetime.now(UTC),
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
        return row_id

    def get(self, passport_id: str) -> DecisionPassport | None:
        """Fetch one passport by stored row id, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(DecisionPassportRecord, passport_id)
        return _row_to_passport(row) if row is not None else None

    def list(
        self,
        *,
        tenant_id: str | None = None,
        lead_id: str | None = None,
        limit: int = 200,
    ) -> list[DecisionPassport]:
        """Return recent passports, newest first."""
        stmt = select(DecisionPassportRecord).order_by(
            DecisionPassportRecord.created_at.desc()
        )
        if tenant_id is not None:
            stmt = stmt.where(DecisionPassportRecord.tenant_id == tenant_id)
        if lead_id is not None:
            stmt = stmt.where(DecisionPassportRecord.lead_id == lead_id)
        stmt = stmt.limit(max(1, limit))
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_row_to_passport(r) for r in rows]

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the passport table."""
        with self._lock:
            DecisionPassportRecord.__table__.drop(self._engine, checkfirst=True)
            DecisionPassportRecord.__table__.create(self._engine, checkfirst=True)


# Keep Base referenced so static checkers see the dependency intentionally.
_ = Base

__all__ = ["PassportPersistenceError", "PostgresPassportStore"]

"""Postgres-backed Diagnostics store.

Persists diagnostic runs to :class:`db.models.DiagnosticRecord` (table
``diagnostics``). ``findings`` text is PII-redacted before any write so
no contact PII lands in storage.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from db.models import DiagnosticRecord


def _redact_value(value: object) -> object:
    """Recursively redact PII from strings inside findings / recommendations."""
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, dict):
        return {k: _redact_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact_value(v) for v in value]
    return value


def _row_to_dict(row: DiagnosticRecord) -> dict[str, object]:
    return {
        "id": row.id,
        "tenant_id": row.tenant_id,
        "subject_type": row.subject_type,
        "subject_id": row.subject_id,
        "diagnostic_type": row.diagnostic_type,
        "findings": dict(row.findings or {}),
        "score": row.score,
        "severity": row.severity,
        "recommendations": list(row.recommendations or []),
        "run_by": row.run_by,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


class PostgresDiagnosticStore:
    """SQLAlchemy-backed Diagnostics store."""

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
            DiagnosticRecord.__table__.create(self._engine, checkfirst=True)

    def add(
        self,
        *,
        subject_type: str,
        subject_id: str,
        diagnostic_type: str,
        findings: dict[str, object] | None = None,
        score: float = 0.0,
        severity: str = "low",
        recommendations: list[object] | None = None,
        run_by: str = "",
        tenant_id: str | None = None,
    ) -> dict[str, object]:
        """Persist one diagnostic run. ``findings`` is PII-redacted before insert."""
        if not subject_type or not diagnostic_type:
            raise ValueError("subject_type + diagnostic_type are mandatory")
        now = datetime.now(UTC)
        row = DiagnosticRecord(
            id=f"diag_{uuid4().hex[:20]}",
            tenant_id=tenant_id,
            subject_type=subject_type,
            subject_id=subject_id,
            diagnostic_type=diagnostic_type,
            findings=_redact_value(dict(findings or {})),  # type: ignore[arg-type]
            score=float(score),
            severity=severity,
            recommendations=_redact_value(list(recommendations or [])),  # type: ignore[arg-type]
            run_by=run_by,
            created_at=now,
            updated_at=now,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
            return _row_to_dict(row)

    def get(self, diagnostic_id: str) -> dict[str, object] | None:
        """Fetch one active diagnostic by id, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(DiagnosticRecord, diagnostic_id)
            if row is None or row.deleted_at is not None:
                return None
            return _row_to_dict(row)

    def list(
        self,
        *,
        tenant_id: str | None = None,
        subject_type: str | None = None,
        subject_id: str | None = None,
        diagnostic_type: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, object]]:
        """Return active diagnostics, newest first."""
        stmt = (
            select(DiagnosticRecord)
            .where(DiagnosticRecord.deleted_at.is_(None))
            .order_by(DiagnosticRecord.created_at.desc())
        )
        if tenant_id is not None:
            stmt = stmt.where(DiagnosticRecord.tenant_id == tenant_id)
        if subject_type is not None:
            stmt = stmt.where(DiagnosticRecord.subject_type == subject_type)
        if subject_id is not None:
            stmt = stmt.where(DiagnosticRecord.subject_id == subject_id)
        if diagnostic_type is not None:
            stmt = stmt.where(DiagnosticRecord.diagnostic_type == diagnostic_type)
        stmt = stmt.limit(max(1, limit))
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
            return [_row_to_dict(r) for r in rows]

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the diagnostics table."""
        with self._lock:
            DiagnosticRecord.__table__.drop(self._engine, checkfirst=True)
            DiagnosticRecord.__table__.create(self._engine, checkfirst=True)


__all__ = ["PostgresDiagnosticStore"]

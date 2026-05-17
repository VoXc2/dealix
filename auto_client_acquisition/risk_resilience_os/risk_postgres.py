"""Postgres-backed Risk Register store.

Persists risk entries to :class:`db.models.RiskRecord` (table ``risks``).
``category`` is validated against ``RISK_TAXONOMY_CATEGORIES`` before any
write. Soft-delete is supported via the ``deleted_at`` column.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from auto_client_acquisition.risk_resilience_os.risk_register import (
    RISK_TAXONOMY_CATEGORIES,
)
from db.models import RiskRecord


class RiskValidationError(Exception):
    """Raised when a risk entry fails validation (e.g. unknown category)."""


def _row_to_dict(row: RiskRecord) -> dict[str, object]:
    return {
        "id": row.id,
        "tenant_id": row.tenant_id,
        "category": row.category,
        "title": row.title,
        "description": row.description,
        "owner": row.owner,
        "severity": row.severity,
        "likelihood": row.likelihood,
        "control": row.control,
        "early_warning_signal": row.early_warning_signal,
        "response_plan": row.response_plan,
        "test_or_checklist": row.test_or_checklist,
        "status": row.status,
        "linked_deal_id": row.linked_deal_id,
        "linked_customer_id": row.linked_customer_id,
        "meta_json": dict(row.meta_json or {}),
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


class PostgresRiskRegister:
    """SQLAlchemy-backed Risk Register store."""

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
            RiskRecord.__table__.create(self._engine, checkfirst=True)

    def add(
        self,
        *,
        category: str,
        title: str,
        tenant_id: str | None = None,
        description: str = "",
        owner: str = "",
        severity: str = "medium",
        likelihood: str = "medium",
        control: str = "",
        early_warning_signal: str = "",
        response_plan: str = "",
        test_or_checklist: str = "",
        status: str = "open",
        linked_deal_id: str | None = None,
        linked_customer_id: str | None = None,
        meta_json: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Validate + persist one risk entry. Returns the stored row as a dict."""
        if category not in RISK_TAXONOMY_CATEGORIES:
            raise RiskValidationError(
                f"unknown risk category {category!r}; "
                f"must be one of {RISK_TAXONOMY_CATEGORIES}"
            )
        if not title or not title.strip():
            raise RiskValidationError("risk title is mandatory")
        now = datetime.now(UTC)
        row = RiskRecord(
            id=f"risk_{uuid4().hex[:20]}",
            tenant_id=tenant_id,
            category=category,
            title=title,
            description=description,
            owner=owner,
            severity=severity,
            likelihood=likelihood,
            control=control,
            early_warning_signal=early_warning_signal,
            response_plan=response_plan,
            test_or_checklist=test_or_checklist,
            status=status,
            linked_deal_id=linked_deal_id,
            linked_customer_id=linked_customer_id,
            meta_json=dict(meta_json or {}),
            created_at=now,
            updated_at=now,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
            return _row_to_dict(row)

    def get(self, risk_id: str) -> dict[str, object] | None:
        """Fetch one active risk by id, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(RiskRecord, risk_id)
            if row is None or row.deleted_at is not None:
                return None
            return _row_to_dict(row)

    def list(
        self,
        *,
        tenant_id: str | None = None,
        category: str | None = None,
        status: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, object]]:
        """Return active risks, newest first."""
        stmt = (
            select(RiskRecord)
            .where(RiskRecord.deleted_at.is_(None))
            .order_by(RiskRecord.created_at.desc())
        )
        if tenant_id is not None:
            stmt = stmt.where(RiskRecord.tenant_id == tenant_id)
        if category is not None:
            stmt = stmt.where(RiskRecord.category == category)
        if status is not None:
            stmt = stmt.where(RiskRecord.status == status)
        stmt = stmt.limit(max(1, limit))
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
            return [_row_to_dict(r) for r in rows]

    def update_status(self, risk_id: str, status: str) -> dict[str, object] | None:
        """Update a risk's status. Returns the updated row or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(RiskRecord, risk_id)
            if row is None or row.deleted_at is not None:
                return None
            row.status = status
            row.updated_at = datetime.now(UTC)
            session.commit()
            return _row_to_dict(row)

    def soft_delete(self, risk_id: str) -> bool:
        """Soft-delete a risk. Returns True if found."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(RiskRecord, risk_id)
            if row is None or row.deleted_at is not None:
                return False
            row.deleted_at = datetime.now(UTC)
            session.commit()
            return True

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the risks table."""
        with self._lock:
            RiskRecord.__table__.drop(self._engine, checkfirst=True)
            RiskRecord.__table__.create(self._engine, checkfirst=True)


__all__ = ["PostgresRiskRegister", "RiskValidationError"]

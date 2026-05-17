"""Postgres-backed Content Assets store.

Persists DesignOps content artifacts to :class:`db.models.ContentAssetRecord`
(table ``content_assets``). Approval-gated: an asset created without an
approver stays ``draft``; ``approve`` is the only path to ``approved``.
A ``checksum`` over the canonical asset metadata gives integrity.
"""
from __future__ import annotations

import hashlib
import threading
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from db.models import ContentAssetRecord


def _checksum(*, asset_type: str, title: str, uri: str, template_id: str | None) -> str:
    """Deterministic SHA-256 over the asset's identifying metadata."""
    payload = f"{asset_type}|{title}|{uri}|{template_id or ''}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _row_to_dict(row: ContentAssetRecord) -> dict[str, object]:
    return {
        "id": row.id,
        "tenant_id": row.tenant_id,
        "asset_type": row.asset_type,
        "title": row.title,
        "uri": row.uri,
        "template_id": row.template_id,
        "status": row.status,
        "approved_by": row.approved_by,
        "approved_at": row.approved_at.isoformat() if row.approved_at else None,
        "linked_deal_id": row.linked_deal_id,
        "checksum": row.checksum,
        "meta_json": dict(row.meta_json or {}),
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


class PostgresContentAssetStore:
    """SQLAlchemy-backed Content Assets store."""

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
            ContentAssetRecord.__table__.create(self._engine, checkfirst=True)

    def add(
        self,
        *,
        asset_type: str,
        title: str,
        tenant_id: str | None = None,
        uri: str = "",
        template_id: str | None = None,
        linked_deal_id: str | None = None,
        meta_json: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Persist one content asset. Always created in ``draft`` — no approver."""
        if not asset_type or not title:
            raise ValueError("asset_type + title are mandatory")
        now = datetime.now(UTC)
        row = ContentAssetRecord(
            id=f"asset_{uuid4().hex[:20]}",
            tenant_id=tenant_id,
            asset_type=asset_type,
            title=title,
            uri=uri,
            template_id=template_id,
            status="draft",
            approved_by=None,
            approved_at=None,
            linked_deal_id=linked_deal_id,
            checksum=_checksum(
                asset_type=asset_type, title=title, uri=uri, template_id=template_id
            ),
            meta_json=dict(meta_json or {}),
            created_at=now,
            updated_at=now,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
            return _row_to_dict(row)

    def get(self, asset_id: str) -> dict[str, object] | None:
        """Fetch one active content asset by id, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(ContentAssetRecord, asset_id)
            if row is None or row.deleted_at is not None:
                return None
            return _row_to_dict(row)

    def list(
        self,
        *,
        tenant_id: str | None = None,
        asset_type: str | None = None,
        status: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, object]]:
        """Return active content assets, newest first."""
        stmt = (
            select(ContentAssetRecord)
            .where(ContentAssetRecord.deleted_at.is_(None))
            .order_by(ContentAssetRecord.created_at.desc())
        )
        if tenant_id is not None:
            stmt = stmt.where(ContentAssetRecord.tenant_id == tenant_id)
        if asset_type is not None:
            stmt = stmt.where(ContentAssetRecord.asset_type == asset_type)
        if status is not None:
            stmt = stmt.where(ContentAssetRecord.status == status)
        stmt = stmt.limit(max(1, limit))
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
            return [_row_to_dict(r) for r in rows]

    def approve(
        self, asset_id: str, *, approver: str
    ) -> dict[str, object] | None:
        """Approve a content asset. Requires a non-empty approver.

        Without an approver the asset stays ``draft`` — the approval gate.
        Returns the updated row, or None when the asset is not found.
        """
        if not approver or not approver.strip():
            raise ValueError("approver is mandatory — asset stays draft without one")
        with self._lock, self._sessionmaker() as session:
            row = session.get(ContentAssetRecord, asset_id)
            if row is None or row.deleted_at is not None:
                return None
            row.status = "approved"
            row.approved_by = approver
            row.approved_at = datetime.now(UTC)
            row.updated_at = datetime.now(UTC)
            session.commit()
            return _row_to_dict(row)

    def verify_checksum(self, asset_id: str) -> bool:
        """Recompute the checksum and compare against the stored value."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(ContentAssetRecord, asset_id)
            if row is None:
                return False
            expected = _checksum(
                asset_type=row.asset_type,
                title=row.title,
                uri=row.uri,
                template_id=row.template_id,
            )
            return row.checksum == expected

    def soft_delete(self, asset_id: str) -> bool:
        """Soft-delete a content asset. Returns True if found."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(ContentAssetRecord, asset_id)
            if row is None or row.deleted_at is not None:
                return False
            row.deleted_at = datetime.now(UTC)
            session.commit()
            return True

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the content_assets table."""
        with self._lock:
            ContentAssetRecord.__table__.drop(self._engine, checkfirst=True)
            ContentAssetRecord.__table__.create(self._engine, checkfirst=True)


__all__ = ["PostgresContentAssetStore"]

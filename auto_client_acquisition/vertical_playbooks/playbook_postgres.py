"""Postgres-backed Playbooks store.

Persists vertical playbooks to :class:`db.models.PlaybookRecord` (table
``playbooks``). Soft-delete is supported via the ``deleted_at`` column.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from auto_client_acquisition.vertical_playbooks.catalog import PLAYBOOKS
from db.models import PlaybookRecord


def _row_to_dict(row: PlaybookRecord) -> dict[str, object]:
    return {
        "id": row.id,
        "tenant_id": row.tenant_id,
        "name": row.name,
        "vertical": row.vertical,
        "version": row.version,
        "stage": row.stage,
        "steps": list(row.steps or []),
        "entry_criteria": list(row.entry_criteria or []),
        "exit_criteria": list(row.exit_criteria or []),
        "owner": row.owner,
        "status": row.status,
        "meta_json": dict(row.meta_json or {}),
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


class PostgresPlaybookStore:
    """SQLAlchemy-backed Playbooks store."""

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
            PlaybookRecord.__table__.create(self._engine, checkfirst=True)

    def add(
        self,
        *,
        name: str,
        vertical: str,
        tenant_id: str | None = None,
        version: int = 1,
        stage: str = "",
        steps: list[object] | None = None,
        entry_criteria: list[object] | None = None,
        exit_criteria: list[object] | None = None,
        owner: str = "",
        status: str = "draft",
        meta_json: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Persist one playbook. Returns the stored row as a dict."""
        if not name or not vertical:
            raise ValueError("playbook name + vertical are mandatory")
        now = datetime.now(UTC)
        row = PlaybookRecord(
            id=f"pbk_{uuid4().hex[:20]}",
            tenant_id=tenant_id,
            name=name,
            vertical=vertical,
            version=int(version),
            stage=stage,
            steps=list(steps or []),
            entry_criteria=list(entry_criteria or []),
            exit_criteria=list(exit_criteria or []),
            owner=owner,
            status=status,
            meta_json=dict(meta_json or {}),
            created_at=now,
            updated_at=now,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
            return _row_to_dict(row)

    def get(self, playbook_id: str) -> dict[str, object] | None:
        """Fetch one active playbook by id, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(PlaybookRecord, playbook_id)
            if row is None or row.deleted_at is not None:
                return None
            return _row_to_dict(row)

    def list(
        self,
        *,
        tenant_id: str | None = None,
        vertical: str | None = None,
        status: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, object]]:
        """Return active playbooks, newest first."""
        stmt = (
            select(PlaybookRecord)
            .where(PlaybookRecord.deleted_at.is_(None))
            .order_by(PlaybookRecord.created_at.desc())
        )
        if tenant_id is not None:
            stmt = stmt.where(PlaybookRecord.tenant_id == tenant_id)
        if vertical is not None:
            stmt = stmt.where(PlaybookRecord.vertical == vertical)
        if status is not None:
            stmt = stmt.where(PlaybookRecord.status == status)
        stmt = stmt.limit(max(1, limit))
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
            return [_row_to_dict(r) for r in rows]

    def update_status(
        self, playbook_id: str, status: str
    ) -> dict[str, object] | None:
        """Update a playbook's status. Returns the updated row or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(PlaybookRecord, playbook_id)
            if row is None or row.deleted_at is not None:
                return None
            row.status = status
            row.updated_at = datetime.now(UTC)
            session.commit()
            return _row_to_dict(row)

    def soft_delete(self, playbook_id: str) -> bool:
        """Soft-delete a playbook. Returns True if found."""
        with self._lock, self._sessionmaker() as session:
            row = session.get(PlaybookRecord, playbook_id)
            if row is None or row.deleted_at is not None:
                return False
            row.deleted_at = datetime.now(UTC)
            session.commit()
            return True

    def seed_from_catalog(
        self, *, tenant_id: str | None = None
    ) -> list[dict[str, object]]:
        """Seed the store from the hand-curated 5-vertical catalog."""
        out: list[dict[str, object]] = []
        for vertical, playbook in PLAYBOOKS.items():
            data = playbook.to_dict()
            out.append(
                self.add(
                    name=data["name_en"],
                    vertical=vertical.value,
                    tenant_id=tenant_id,
                    stage="catalog",
                    steps=[data["message_pattern_en"]],
                    entry_criteria=list(data["common_pains_en"]),
                    exit_criteria=[data["proof_metric"]],
                    owner="founder",
                    status="published",
                    meta_json={
                        "name_ar": data["name_ar"],
                        "best_first_offer_en": data["best_first_offer_en"],
                        "safe_channels": data["safe_channels"],
                        "forbidden_channels": data["forbidden_channels"],
                        "blocked_actions": data["blocked_actions"],
                    },
                )
            )
        return out

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the playbooks table."""
        with self._lock:
            PlaybookRecord.__table__.drop(self._engine, checkfirst=True)
            PlaybookRecord.__table__.create(self._engine, checkfirst=True)


__all__ = ["PostgresPlaybookStore"]

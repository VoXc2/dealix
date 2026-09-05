"""Transaction-safe Postgres snapshot store for the Approval Center."""

from __future__ import annotations

import threading
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, Callable, TypeVar

from sqlalchemy import JSON, DateTime, String, create_engine, inspect, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.orm.attributes import flag_modified

from auto_client_acquisition.approval_center.approval_policy import (
    assert_can_approve,
    assert_can_edit,
    assert_can_reject,
    evaluate_safety,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)

_T = TypeVar("_T")


class _ApprovalStoreBase(DeclarativeBase):
    pass


class ApprovalCenterSnapshotORM(_ApprovalStoreBase):
    __tablename__ = "approval_center_snapshots"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default="default")
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PostgresApprovalStore:
    """ApprovalStore-compatible JSON snapshot backed by one DB transaction.

    Every mutation acquires the canonical snapshot writer lock, reads the row,
    applies policy and state transition, then writes within the same transaction.
    PostgreSQL uses an advisory transaction lock as well as ``FOR UPDATE`` so the
    first-row case and multiple application workers are serialized.
    """

    SNAPSHOT_ID = "default"
    _ADVISORY_LOCK_KEY = "dealix:approval-center-snapshot:v1"

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        self._lock = threading.RLock()
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True, pool_pre_ping=True)
        self._engine = engine
        self._sessionmaker = sessionmaker(
            self._engine,
            expire_on_commit=False,
            future=True,
        )
        if create_tables:
            _ApprovalStoreBase.metadata.create_all(self._engine)

    def assert_ready(self) -> None:
        """Verify connectivity and Alembic-managed table presence without mutation."""
        try:
            with self._engine.connect() as connection:
                if not inspect(connection).has_table(ApprovalCenterSnapshotORM.__tablename__):
                    raise RuntimeError("approval_center_schema_not_migrated")
                connection.execute(
                    select(ApprovalCenterSnapshotORM.id).limit(1)
                ).all()
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError("approval_center_postgres_unavailable") from exc

    @staticmethod
    def _decode_items(blob: dict[str, Any] | None) -> dict[str, ApprovalRequest]:
        if not isinstance(blob, dict):
            return {}
        raw = blob.get("items") or {}
        if not isinstance(raw, dict):
            return {}
        items: dict[str, ApprovalRequest] = {}
        for approval_id, payload in raw.items():
            if isinstance(payload, dict):
                items[str(approval_id)] = ApprovalRequest.model_validate(payload)
        return items

    @staticmethod
    def _encode_items(items: dict[str, ApprovalRequest]) -> dict[str, Any]:
        return {
            "items": {
                approval_id: request.model_dump(mode="json")
                for approval_id, request in items.items()
            }
        }

    def _read_items(self) -> dict[str, ApprovalRequest]:
        with self._lock, self._sessionmaker() as session:
            row = session.get(ApprovalCenterSnapshotORM, self.SNAPSHOT_ID)
            if row is None:
                return {}
            return self._decode_items(deepcopy(row.data))

    def _mutate(
        self,
        mutation: Callable[[dict[str, ApprovalRequest]], _T],
    ) -> _T:
        with self._lock, self._sessionmaker() as session, session.begin():
            if self._engine.dialect.name == "postgresql":
                session.execute(
                    text("SELECT pg_advisory_xact_lock(hashtext(:lock_key))"),
                    {"lock_key": self._ADVISORY_LOCK_KEY},
                )
            statement = (
                select(ApprovalCenterSnapshotORM)
                .where(ApprovalCenterSnapshotORM.id == self.SNAPSHOT_ID)
                .with_for_update()
            )
            row = session.execute(statement).scalar_one_or_none()
            items = self._decode_items(deepcopy(row.data) if row is not None else None)
            result = mutation(items)
            blob = self._encode_items(items)
            now = datetime.now(UTC)
            if row is None:
                row = ApprovalCenterSnapshotORM(
                    id=self.SNAPSHOT_ID,
                    data=blob,
                    updated_at=now,
                )
                session.add(row)
            else:
                row.data = blob
                row.updated_at = now
                flag_modified(row, "data")
            return result

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        evaluate_safety(req)

        def _apply(items: dict[str, ApprovalRequest]) -> ApprovalRequest:
            items[req.approval_id] = req
            return req

        return self._mutate(_apply)

    def create_with_founder_rules(
        self,
        req: ApprovalRequest,
        *,
        confidence: float = 1.0,
        content: str = "",
        engine: Any = None,
    ) -> ApprovalRequest:
        from auto_client_acquisition.approval_center.founder_rules_integration import (
            try_auto_approve_via_founder_rule,
        )

        evaluate_safety(req)

        def _apply(items: dict[str, ApprovalRequest]) -> ApprovalRequest:
            try_auto_approve_via_founder_rule(
                req,
                confidence=confidence,
                content=content,
                engine=engine,
            )
            items[req.approval_id] = req
            return req

        return self._mutate(_apply)

    def get(self, approval_id: str) -> ApprovalRequest | None:
        return self._read_items().get(approval_id)

    def list_pending(self) -> list[ApprovalRequest]:
        rows = [
            request
            for request in self._read_items().values()
            if ApprovalStatus(request.status) == ApprovalStatus.PENDING
        ]
        rows.sort(key=lambda request: request.created_at)
        return rows

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        limit = max(1, min(int(limit), 500))
        rows = list(self._read_items().values())
        rows.sort(key=lambda request: request.updated_at, reverse=True)
        return rows[:limit]

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        def _apply(items: dict[str, ApprovalRequest]) -> ApprovalRequest:
            req = self._require(items, approval_id)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(self._audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
            items[approval_id] = req
            return req

        return self._mutate(_apply)

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        def _apply(items: dict[str, ApprovalRequest]) -> ApprovalRequest:
            req = self._require(items, approval_id)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(
                self._audit_entry(who, "reject", {"reason": reason})
            )
            req.updated_at = datetime.now(UTC)
            items[approval_id] = req
            return req

        return self._mutate(_apply)

    def edit(
        self,
        approval_id: str,
        who: str,
        patch: dict[str, Any],
    ) -> ApprovalRequest:
        allowed = {
            "summary_ar",
            "summary_en",
            "channel",
            "proof_impact",
            "risk_level",
            "action_mode",
            "expires_at",
        }

        def _apply(items: dict[str, ApprovalRequest]) -> ApprovalRequest:
            req = self._require(items, approval_id)
            assert_can_edit(req)
            applied: dict[str, Any] = {}
            for key, value in patch.items():
                if key in allowed:
                    setattr(req, key, value)
                    applied[key] = value
            evaluate_safety(req)
            req.edit_history.append(
                self._audit_entry(who, "edit", {"patch": applied})
            )
            req.updated_at = datetime.now(UTC)
            items[approval_id] = req
            return req

        return self._mutate(_apply)

    def expire_overdue(self) -> int:
        now = datetime.now(UTC)

        def _apply(items: dict[str, ApprovalRequest]) -> int:
            expired_count = 0
            for approval_id, req in items.items():
                if (
                    ApprovalStatus(req.status) == ApprovalStatus.PENDING
                    and req.expires_at is not None
                    and req.expires_at < now
                ):
                    req.status = ApprovalStatus.EXPIRED
                    req.updated_at = now
                    req.edit_history.append(self._audit_entry("system", "expire", {}))
                    items[approval_id] = req
                    expired_count += 1
            return expired_count

        return self._mutate(_apply)

    def bulk_approve(
        self,
        *,
        who: str,
        proof_impact_prefix: str | None = None,
        approval_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        if not approval_ids and not proof_impact_prefix:
            return {
                "approved": [],
                "failed": [],
                "total": 0,
                "reason": "either approval_ids or proof_impact_prefix required",
            }

        def _apply(items: dict[str, ApprovalRequest]) -> dict[str, Any]:
            approved: list[str] = []
            failed: list[dict[str, Any]] = []
            if approval_ids:
                candidates = [
                    req for req in items.values() if req.approval_id in approval_ids
                ]
            else:
                candidates = [
                    req
                    for req in items.values()
                    if (req.proof_impact or "").startswith(proof_impact_prefix or "")
                    and ApprovalStatus(req.status) == ApprovalStatus.PENDING
                ]
            for req in candidates:
                try:
                    assert_can_approve(req)
                    req.status = ApprovalStatus.APPROVED
                    req.edit_history.append(
                        self._audit_entry(who, "bulk_approve", {})
                    )
                    req.updated_at = datetime.now(UTC)
                    items[req.approval_id] = req
                    approved.append(req.approval_id)
                except Exception as exc:
                    failed.append({"id": req.approval_id, "reason": str(exc)})
            return {
                "approved": approved,
                "failed": failed,
                "total": len(approved) + len(failed),
            }

        return self._mutate(_apply)

    def clear(self) -> None:
        def _apply(items: dict[str, ApprovalRequest]) -> None:
            items.clear()

        self._mutate(_apply)

    @staticmethod
    def _require(
        items: dict[str, ApprovalRequest],
        approval_id: str,
    ) -> ApprovalRequest:
        req = items.get(approval_id)
        if req is None:
            raise ValueError(f"approval {approval_id} not found")
        return req

    @staticmethod
    def _audit_entry(
        who: str,
        action: str,
        extra: dict[str, Any],
    ) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "at": datetime.now(UTC).isoformat(),
            "who": who,
            "action": action,
        }
        entry.update(extra)
        return entry


def reset_approval_postgres_tables_for_test(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS approval_center_snapshots"))


__all__ = [
    "ApprovalCenterSnapshotORM",
    "PostgresApprovalStore",
    "reset_approval_postgres_tables_for_test",
]

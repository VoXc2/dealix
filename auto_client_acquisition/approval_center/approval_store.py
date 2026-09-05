"""Approval Center store contract and explicit backend factory.

The in-memory implementation remains the safe local/test default. Production can
opt into Postgres with ``DEALIX_APPROVAL_STORE_BACKEND=postgres`` only when a real
PostgreSQL DSN is supplied and the Alembic-managed snapshot table already exists.
Explicit Postgres selection never falls back to process memory or a non-Postgres
SQLAlchemy backend.
"""
from __future__ import annotations

import os
import threading
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.engine import make_url

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

_BACKEND_ENV = "DEALIX_APPROVAL_STORE_BACKEND"
_DATABASE_URL_ENV = "DEALIX_APPROVAL_DATABASE_URL"
_SQLITE_TEST_OVERRIDE_ENV = "DEALIX_APPROVAL_ALLOW_SQLITE_TEST_BACKEND"
_MEMORY_BACKENDS = {"", "memory", "in-memory", "in_memory"}
_POSTGRES_BACKENDS = {"postgres", "postgresql"}


def _request_contract(req: ApprovalRequest) -> dict[str, Any]:
    """Immutable creation facts used to reject approval-ID substitution."""
    return req.model_dump(
        mode="json",
        exclude={
            "status",
            "edit_history",
            "reject_reason",
            "created_at",
            "updated_at",
        },
    )


class ApprovalStore:
    """Thread-safe in-memory store of ApprovalRequests."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, ApprovalRequest] = {}

    def _insert_or_replay(self, req: ApprovalRequest) -> ApprovalRequest:
        existing = self._items.get(req.approval_id)
        if existing is None:
            self._items[req.approval_id] = req
            return req
        if _request_contract(existing) != _request_contract(req):
            raise ValueError(f"approval_idempotency_conflict:{req.approval_id}")
        return existing

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        evaluate_safety(req)
        with self._lock:
            return self._insert_or_replay(req)

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
        with self._lock:
            existing = self._items.get(req.approval_id)
            if existing is not None:
                return self._insert_or_replay(req)
            try_auto_approve_via_founder_rule(
                req,
                confidence=confidence,
                content=content,
                engine=engine,
            )
            self._items[req.approval_id] = req
            return req

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        with self._lock:
            req = self._require(approval_id)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(self._audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
        return req

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        with self._lock:
            req = self._require(approval_id)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(self._audit_entry(who, "reject", {"reason": reason}))
            req.updated_at = datetime.now(UTC)
        return req

    def edit(
        self,
        approval_id: str,
        who: str,
        patch: dict[str, Any],
    ) -> ApprovalRequest:
        with self._lock:
            req = self._require(approval_id)
            assert_can_edit(req)
            allowed = {
                "summary_ar",
                "summary_en",
                "channel",
                "proof_impact",
                "risk_level",
                "action_mode",
                "expires_at",
            }
            applied: dict[str, Any] = {}
            for key, value in patch.items():
                if key in allowed:
                    setattr(req, key, value)
                    applied[key] = value
            evaluate_safety(req)
            req.edit_history.append(self._audit_entry(who, "edit", {"patch": applied}))
            req.updated_at = datetime.now(UTC)
        return req

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._items.get(approval_id)

    def list_pending(self) -> list[ApprovalRequest]:
        with self._lock:
            rows = [
                r
                for r in self._items.values()
                if ApprovalStatus(r.status) == ApprovalStatus.PENDING
            ]
        rows.sort(key=lambda r: r.created_at)
        return rows

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        limit = max(1, min(int(limit), 500))
        with self._lock:
            rows = list(self._items.values())
        rows.sort(key=lambda r: r.updated_at, reverse=True)
        return rows[:limit]

    def expire_overdue(self) -> int:
        now = datetime.now(UTC)
        expired_count = 0
        with self._lock:
            for req in self._items.values():
                if (
                    ApprovalStatus(req.status) == ApprovalStatus.PENDING
                    and req.expires_at is not None
                    and req.expires_at < now
                ):
                    req.status = ApprovalStatus.EXPIRED
                    req.updated_at = now
                    req.edit_history.append(self._audit_entry("system", "expire", {}))
                    expired_count += 1
        return expired_count

    def bulk_approve(
        self,
        *,
        who: str,
        proof_impact_prefix: str | None = None,
        approval_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        approved: list[str] = []
        failed: list[dict[str, Any]] = []
        with self._lock:
            candidates: list[ApprovalRequest]
            if approval_ids:
                candidates = [
                    r for r in self._items.values() if r.approval_id in approval_ids
                ]
            elif proof_impact_prefix:
                candidates = [
                    r
                    for r in self._items.values()
                    if (r.proof_impact or "").startswith(proof_impact_prefix)
                    and ApprovalStatus(r.status) == ApprovalStatus.PENDING
                ]
            else:
                return {
                    "approved": [],
                    "failed": [],
                    "total": 0,
                    "reason": "either approval_ids or proof_impact_prefix required",
                }

            for req in candidates:
                try:
                    assert_can_approve(req)
                    req.status = ApprovalStatus.APPROVED
                    req.edit_history.append(
                        self._audit_entry(who, "bulk_approve", {})
                    )
                    req.updated_at = datetime.now(UTC)
                    approved.append(req.approval_id)
                except Exception as exc:
                    failed.append({"id": req.approval_id, "reason": str(exc)})
        return {
            "approved": approved,
            "failed": failed,
            "total": len(approved) + len(failed),
        }

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def _require(self, approval_id: str) -> ApprovalRequest:
        req = self._items.get(approval_id)
        if req is None:
            raise ValueError(f"approval {approval_id} not found")
        return req

    @staticmethod
    def _audit_entry(who: str, action: str, extra: dict[str, Any]) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "at": datetime.now(UTC).isoformat(),
            "who": who,
            "action": action,
        }
        entry.update(extra)
        return entry


_DEFAULT: Any | None = None
_DEFAULT_LOCK = threading.Lock()


def _requested_backend() -> str:
    return os.environ.get(_BACKEND_ENV, "memory").strip().lower()


def _sqlite_test_override_enabled() -> bool:
    app_env = os.environ.get("APP_ENV", "").strip().lower()
    enabled = os.environ.get(_SQLITE_TEST_OVERRIDE_ENV, "").strip() == "1"
    return app_env in {"test", "testing"} and enabled


def _normalize_approval_database_url(raw: str) -> str:
    """Return a sync PostgreSQL URL and reject wrong production dialects.

    SQLite is accepted only behind an explicit two-part test override so unit tests
    can exercise the store contract without weakening the production backend gate.
    """
    from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url

    normalized = sync_sqlalchemy_url(raw)
    if normalized.startswith("postgres://"):
        normalized = "postgresql+psycopg://" + normalized.removeprefix("postgres://")
    elif normalized.startswith("postgresql://"):
        normalized = "postgresql+psycopg://" + normalized.removeprefix("postgresql://")

    try:
        backend = make_url(normalized).get_backend_name()
    except Exception:
        raise RuntimeError("approval_store_database_url_invalid") from None

    if backend == "postgresql":
        return normalized
    if backend == "sqlite" and _sqlite_test_override_enabled():
        return normalized
    raise RuntimeError("approval_store_postgres_requires_postgresql_url")


def _approval_database_url_from_env() -> str:
    raw = (
        os.environ.get(_DATABASE_URL_ENV, "").strip()
        or os.environ.get("DATABASE_URL", "").strip()
    )
    if not raw:
        raise RuntimeError(
            "approval_store_postgres_requested_but_database_url_missing"
        )
    return _normalize_approval_database_url(raw)


def approval_store_backend_status() -> dict[str, Any]:
    """Return a redacted, read-only backend readiness receipt."""
    backend = _requested_backend()
    if backend in _MEMORY_BACKENDS:
        return {
            "verdict": "HOLD",
            "backend": "memory",
            "process_scoped": True,
            "database_url_configured": False,
            "schema_ready": False,
            "reason": "approval_center_process_scoped",
        }
    if backend not in _POSTGRES_BACKENDS:
        return {
            "verdict": "FAIL",
            "backend": backend or "unknown",
            "process_scoped": False,
            "database_url_configured": False,
            "schema_ready": False,
            "reason": "unsupported_approval_store_backend",
        }

    try:
        database_url = _approval_database_url_from_env()
    except RuntimeError as exc:
        return {
            "verdict": "HOLD",
            "backend": "postgres",
            "process_scoped": False,
            "database_url_configured": bool(
                os.environ.get(_DATABASE_URL_ENV, "").strip()
                or os.environ.get("DATABASE_URL", "").strip()
            ),
            "schema_ready": False,
            "reason": str(exc),
        }

    try:
        from auto_client_acquisition.approval_center.postgres_store import (
            PostgresApprovalStore,
        )

        store = PostgresApprovalStore(database_url=database_url, create_tables=False)
        store.assert_ready()
    except RuntimeError as exc:
        reason = str(exc)
        if reason not in {
            "approval_center_schema_not_migrated",
            "approval_center_postgres_unavailable",
        }:
            reason = "approval_center_postgres_unavailable"
        return {
            "verdict": "HOLD",
            "backend": "postgres",
            "process_scoped": False,
            "database_url_configured": True,
            "schema_ready": False,
            "reason": reason,
        }
    except Exception:
        return {
            "verdict": "HOLD",
            "backend": "postgres",
            "process_scoped": False,
            "database_url_configured": True,
            "schema_ready": False,
            "reason": "approval_center_postgres_unavailable",
        }
    return {
        "verdict": "PASS",
        "backend": "postgres",
        "process_scoped": False,
        "database_url_configured": True,
        "schema_ready": True,
        "reason": "approval_center_postgres_ready",
    }


def _build_default_approval_store() -> Any:
    backend = _requested_backend()
    if backend in _MEMORY_BACKENDS:
        return ApprovalStore()
    if backend in _POSTGRES_BACKENDS:
        from auto_client_acquisition.approval_center.postgres_store import (
            PostgresApprovalStore,
        )

        try:
            store = PostgresApprovalStore(
                database_url=_approval_database_url_from_env(),
                create_tables=False,
            )
            store.assert_ready()
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError("approval_center_postgres_unavailable") from exc
        return store
    raise RuntimeError(f"unsupported_approval_store_backend:{backend}")


def get_default_approval_store() -> Any:
    global _DEFAULT
    if _DEFAULT is None:
        with _DEFAULT_LOCK:
            if _DEFAULT is None:
                _DEFAULT = _build_default_approval_store()
    return _DEFAULT


def reset_default_approval_store_for_tests(store: Any | None = None) -> Any | None:
    """Reset/inject the singleton for isolated tests only."""
    global _DEFAULT
    with _DEFAULT_LOCK:
        _DEFAULT = store
    return store


__all__ = [
    "ApprovalStore",
    "approval_store_backend_status",
    "get_default_approval_store",
    "reset_default_approval_store_for_tests",
]

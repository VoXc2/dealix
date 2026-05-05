"""In-memory, thread-safe ApprovalStore.

This is the v6 stopgap before a Redis-backed store ships. The public
methods (``create``, ``approve``, ``reject``, ``edit``, ``list_pending``,
``list_history``, ``get``) form the contract that the Redis variant will
implement verbatim.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

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


class ApprovalStore:
    """Thread-safe in-memory store of ApprovalRequests."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, ApprovalRequest] = {}

    # ─── Mutations ───────────────────────────────────────────────

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        """Persist a new request. Runs safety policy at create time."""
        evaluate_safety(req)
        with self._lock:
            self._items[req.approval_id] = req
        return req

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        """Mark a request approved. Raises ValueError on illegal transitions."""
        with self._lock:
            req = self._require(approval_id)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(self._audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
        return req

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        """Mark a request rejected with reason. Raises on illegal transitions."""
        with self._lock:
            req = self._require(approval_id)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(
                self._audit_entry(who, "reject", {"reason": reason})
            )
            req.updated_at = datetime.now(UTC)
        return req

    def edit(
        self,
        approval_id: str,
        who: str,
        patch: dict[str, Any],
    ) -> ApprovalRequest:
        """Apply an edit. Records the patch in ``edit_history`` without
        mutating prior entries. Only safe-list fields are patched."""
        with self._lock:
            req = self._require(approval_id)
            assert_can_edit(req)

            # Whitelist: never let an edit flip status / approval_id /
            # created_at / edit_history itself.
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

            # Re-run safety in case action_mode / risk_level changed.
            evaluate_safety(req)

            req.edit_history.append(
                self._audit_entry(who, "edit", {"patch": applied})
            )
            req.updated_at = datetime.now(UTC)
        return req

    # ─── Reads ───────────────────────────────────────────────────

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._items.get(approval_id)

    def list_pending(self) -> list[ApprovalRequest]:
        with self._lock:
            rows = [
                r for r in self._items.values()
                if ApprovalStatus(r.status) == ApprovalStatus.PENDING
            ]
        rows.sort(key=lambda r: r.created_at)
        return rows

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        """Return most-recent requests in any status, newest first."""
        limit = max(1, min(int(limit), 500))
        with self._lock:
            rows = list(self._items.values())
        rows.sort(key=lambda r: r.updated_at, reverse=True)
        return rows[:limit]

    # ─── Test helpers ────────────────────────────────────────────

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    # ─── Internal ────────────────────────────────────────────────

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


# Module-level singleton (process-scoped).
_DEFAULT: ApprovalStore | None = None


def get_default_approval_store() -> ApprovalStore:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = ApprovalStore()
    return _DEFAULT

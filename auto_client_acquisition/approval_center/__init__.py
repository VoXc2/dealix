"""Approval Command Center public compatibility surface.

Keep the historical package-level helpers stable while routing every operation
through the configured default store. This preserves existing callers while
allowing the explicit durable Postgres backend to replace process memory only
when its fail-closed factory is intentionally enabled.
"""
from typing import Any

from auto_client_acquisition.approval_center.approval_renderer import (
    render_approval_card,
)
from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    approval_store_backend_status,
    get_default_approval_store,
    reset_default_approval_store_for_tests,
)
from auto_client_acquisition.approval_center.schemas import (
    ActionType,
    ApprovalRequest,
    ApprovalStatus,
    is_canonical_action_type,
)


def create_approval(req: ApprovalRequest) -> ApprovalRequest:
    """Create an approval in the configured default store."""
    return get_default_approval_store().create(req)


def approve(approval_id: str, who: str) -> ApprovalRequest:
    """Approve a pending request in the configured default store."""
    return get_default_approval_store().approve(approval_id, who)


def reject(approval_id: str, who: str, reason: str) -> ApprovalRequest:
    """Reject a pending request in the configured default store."""
    return get_default_approval_store().reject(approval_id, who, reason)


def edit(approval_id: str, who: str, patch: dict[str, Any]) -> ApprovalRequest:
    """Edit a pending request in the configured default store."""
    return get_default_approval_store().edit(approval_id, who, patch)


def list_pending() -> list[ApprovalRequest]:
    """List pending approvals from the configured default store."""
    return get_default_approval_store().list_pending()


def list_history(limit: int = 50) -> list[ApprovalRequest]:
    """List recent approvals from the configured default store."""
    return get_default_approval_store().list_history(limit=limit)


__all__ = [
    "ActionType",
    "ApprovalRequest",
    "ApprovalStatus",
    "ApprovalStore",
    "approval_store_backend_status",
    "approve",
    "create_approval",
    "edit",
    "get_default_approval_store",
    "is_canonical_action_type",
    "list_history",
    "list_pending",
    "reject",
    "render_approval_card",
    "reset_default_approval_store_for_tests",
]

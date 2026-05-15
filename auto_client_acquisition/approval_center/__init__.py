"""Approval Command Center — unified queue for every approval-required action.

Bridge between ``dealix.governance.approvals`` (Redis-backed gate) and
the v5 layers. v6 ships an in-memory / file-backed implementation; the
public surface stays stable so the Redis backend can drop in later.
"""
from typing import Any

from auto_client_acquisition.approval_center.approval_renderer import (
    render_approval_card,
)
from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import (
    ActionType,
    ApprovalRequest,
    ApprovalStatus,
    is_canonical_action_type,
)


def create_approval(req: ApprovalRequest) -> ApprovalRequest:
    """Create an approval in the default store."""
    return get_default_approval_store().create(req)


def approve(approval_id: str, who: str) -> ApprovalRequest:
    """Approve a pending request in the default store."""
    return get_default_approval_store().approve(approval_id, who)


def reject(approval_id: str, who: str, reason: str) -> ApprovalRequest:
    """Reject a pending request in the default store."""
    return get_default_approval_store().reject(approval_id, who, reason)


def edit(approval_id: str, who: str, patch: dict[str, Any]) -> ApprovalRequest:
    """Edit a pending request in the default store."""
    return get_default_approval_store().edit(approval_id, who, patch)


def list_pending() -> list[ApprovalRequest]:
    """List pending approvals in the default store."""
    return get_default_approval_store().list_pending()


def list_history(limit: int = 50) -> list[ApprovalRequest]:
    """List recent approvals (any status) in the default store."""
    return get_default_approval_store().list_history(limit=limit)


__all__ = [
    "ActionType",
    "ApprovalRequest",
    "ApprovalStatus",
    "ApprovalStore",
    "approve",
    "create_approval",
    "edit",
    "get_default_approval_store",
    "is_canonical_action_type",
    "list_history",
    "list_pending",
    "reject",
    "render_approval_card",
]

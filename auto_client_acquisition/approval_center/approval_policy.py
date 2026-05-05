"""Policy decisions for approvals.

Centralizes the rules that govern when an approval may transition
state. Kept independent of storage so it can be unit-tested in
isolation and reused by the Redis backend later.
"""
from __future__ import annotations

from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


def evaluate_safety(req: ApprovalRequest) -> ApprovalRequest:
    """Inspect a freshly-created request and force ``blocked`` status
    if policy demands it. Idempotent."""
    if req.action_mode == "blocked" or req.risk_level == "blocked":
        req.status = ApprovalStatus.BLOCKED
    return req


def assert_can_approve(req: ApprovalRequest) -> None:
    """Raise ValueError if the request cannot transition to approved."""
    status = ApprovalStatus(req.status)
    if status == ApprovalStatus.BLOCKED:
        raise ValueError(
            f"approval {req.approval_id} is blocked and cannot be approved"
        )
    if status != ApprovalStatus.PENDING:
        raise ValueError(
            f"approval {req.approval_id} is {status.value}; only pending "
            "requests can be approved"
        )


def assert_can_reject(req: ApprovalRequest) -> None:
    """Raise ValueError if the request cannot transition to rejected."""
    status = ApprovalStatus(req.status)
    if status == ApprovalStatus.BLOCKED:
        raise ValueError(
            f"approval {req.approval_id} is blocked; rejection is implicit"
        )
    if status != ApprovalStatus.PENDING:
        raise ValueError(
            f"approval {req.approval_id} is {status.value}; only pending "
            "requests can be rejected"
        )


def assert_can_edit(req: ApprovalRequest) -> None:
    """Raise ValueError if the request cannot be edited."""
    status = ApprovalStatus(req.status)
    if status in (ApprovalStatus.APPROVED, ApprovalStatus.REJECTED, ApprovalStatus.BLOCKED):
        raise ValueError(
            f"approval {req.approval_id} is {status.value}; edits no longer allowed"
        )

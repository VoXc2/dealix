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


# ── Critical action types ─────────────────────────────────────
# Actions that always carry the ``critical`` risk tier: they require
# approval + evidence + an optional second review before they execute.
# Money movement, data egress, public claims and autonomous external
# actions all qualify.
CRITICAL_ACTION_TYPES: frozenset[str] = frozenset({
    "invoice_send",
    "refund",
    "affiliate_payout",
    "client_data_export",
    "security_compliance_claim",
    "case_study_publish",
    "external_autonomous_action",
})


def is_critical_action(action_type: str) -> bool:
    """True if the action type always demands the ``critical`` tier."""
    return (action_type or "").strip().lower() in CRITICAL_ACTION_TYPES


def evaluate_safety(req: ApprovalRequest) -> ApprovalRequest:
    """Inspect a freshly-created request and force ``blocked`` status
    if policy demands it. Idempotent.

    Critical actions (see ``CRITICAL_ACTION_TYPES``) are upgraded to the
    ``critical`` risk tier and can never be auto-executed — they require
    explicit founder approval (plus evidence and optional second
    review, enforced downstream)."""
    if req.action_mode == "blocked" or req.risk_level == "blocked":
        req.status = ApprovalStatus.BLOCKED
    # Critical actions: pin the risk tier and refuse pre-approved execute.
    if is_critical_action(req.action_type):
        if _RISK_ORDER.get(req.risk_level or "low", 1) < _RISK_ORDER["critical"]:
            req.risk_level = "critical"
        if req.action_mode == "approved_execute":
            req.action_mode = "approval_required"
    # Per-channel hard rules
    if (req.channel or "").lower() == "linkedin":
        # NO_LINKEDIN_AUTO — every LinkedIn action must be founder-approved
        # at minimum; never auto-approved.
        if req.action_mode == "approved_execute":
            req.action_mode = "approval_required"
    return req


# ── Per-channel policy table ──────────────────────────────────
# Channel → (default_required_approver, max_auto_approve_risk)
# An approval can be auto-approved (still recorded) only if its
# risk_level <= max_auto_approve_risk for the channel. None means
# nothing is auto-approvable on that channel.
CHANNEL_POLICY: dict[str, dict[str, str | None]] = {
    "whatsapp":  {"required_approver": "founder", "max_auto_approve_risk": None},
    "email":     {"required_approver": "csm_or_founder", "max_auto_approve_risk": "low"},
    "linkedin":  {"required_approver": "founder", "max_auto_approve_risk": None},
    "phone":     {"required_approver": "founder", "max_auto_approve_risk": None},
    "dashboard": {"required_approver": "csm_or_founder", "max_auto_approve_risk": "medium"},
}

# Risk ordering — ``critical`` sits between ``high`` and ``blocked``.
# A critical action is still actionable (with approval + evidence +
# optional second review) whereas ``blocked`` can never be approved.
_RISK_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4, "blocked": 5}


def can_auto_approve(req: ApprovalRequest) -> bool:
    """Per-channel rule: returns True only if the channel allows
    auto-approval for this risk level. NEVER True for whatsapp/linkedin/phone.
    """
    policy = CHANNEL_POLICY.get((req.channel or "").lower())
    if not policy or not policy.get("max_auto_approve_risk"):
        return False
    max_allowed = _RISK_ORDER.get(policy["max_auto_approve_risk"] or "", 0)
    actual = _RISK_ORDER.get(req.risk_level or "low", 1)
    return actual <= max_allowed


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

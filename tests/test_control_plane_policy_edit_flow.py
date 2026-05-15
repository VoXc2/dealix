"""Enterprise Control Plane — policy / config changes are approval-gated.

A change to control-plane policy is a high-risk action: it routes
through ``decide()`` to an escalation and through the Approval Center
before it can be considered effective. A change parked as ``blocked``
can never be approved.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from auto_client_acquisition.governance_os.runtime_decision import decide


def _policy_change_request(tenant_id: str = "t1", mode: str = "approval_required") -> ApprovalRequest:
    return ApprovalRequest(
        tenant_id=tenant_id,
        object_type="governance_policy",
        object_id="forbidden_actions",
        action_type="policy_change",
        action_mode=mode,
        risk_level="high",
        summary_en="Edit forbidden-actions policy",
    )


def test_policy_change_escalates_in_decide():
    """A policy/config-mutating action with a high risk score escalates."""
    result = decide(action="policy_change", risk_score=0.8)
    assert result.is_escalation
    assert result.approval_required is True


def test_policy_change_starts_pending_not_effective():
    store = ApprovalStore()
    req = store.create(_policy_change_request())
    assert ApprovalStatus(req.status) == ApprovalStatus.PENDING
    # It is visible in the tenant's pending queue — not silently applied.
    assert any(r.approval_id == req.approval_id for r in store.list_pending(tenant_id="t1"))


def test_policy_change_takes_effect_only_after_approval():
    store = ApprovalStore()
    req = store.create(_policy_change_request())
    approved = store.approve(req.approval_id, who="founder")
    assert ApprovalStatus(approved.status) == ApprovalStatus.APPROVED


def test_blocked_policy_change_cannot_be_approved():
    store = ApprovalStore()
    req = store.create(_policy_change_request(mode="blocked"))
    assert ApprovalStatus(req.status) == ApprovalStatus.BLOCKED
    with pytest.raises(ValueError, match="blocked"):
        store.approve(req.approval_id, who="founder")

"""Enterprise Control Plane — self-evolving proposals are approval-gated.

Check #9 of the verify contract: a self-improvement proposal can never
apply itself. The Self-Improvement OS is suggest-only, and any "apply"
is modelled as an Approval Center ticket that must be granted by a
human before it can take effect.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


def test_self_improvement_os_hard_gates():
    """The router declares the non-negotiable self-evolving gates."""
    from api.routers.self_improvement_os import _HARD_GATES

    assert _HARD_GATES["no_self_modifying_code"] is True
    assert _HARD_GATES["no_automatic_pr"] is True
    assert _HARD_GATES["approval_required_for_external_actions"] is True


async def test_weekly_learning_is_suggest_only():
    """Every improvement the OS emits is a suggestion — never auto-applied."""
    from api.routers.self_improvement_os import weekly_learning

    payload = await weekly_learning()
    suggestions = payload["suggestions"]
    assert suggestions
    assert all(s["action_mode"] == "suggest_only" for s in suggestions)


def test_self_evolving_apply_cannot_take_effect_without_approval():
    store = ApprovalStore()
    proposal = store.create(
        ApprovalRequest(
            tenant_id="t1",
            object_type="improvement_proposal",
            object_id="prop_001",
            action_type="self_improvement_apply",
            action_mode="approval_required",
            risk_level="high",
            summary_en="Apply prompt-quality improvement to outreach drafts",
        ),
    )
    # Starts pending — not applied.
    assert ApprovalStatus(proposal.status) == ApprovalStatus.PENDING
    # Becomes applicable only after a human grants it.
    granted = store.approve(proposal.approval_id, who="founder")
    assert ApprovalStatus(granted.status) == ApprovalStatus.APPROVED


def test_blocked_self_evolving_proposal_cannot_be_approved():
    store = ApprovalStore()
    proposal = store.create(
        ApprovalRequest(
            tenant_id="t1",
            object_type="improvement_proposal",
            object_id="prop_002",
            action_type="self_improvement_apply",
            action_mode="blocked",
            risk_level="blocked",
            summary_en="Self-modifying code change",
        ),
    )
    assert ApprovalStatus(proposal.status) == ApprovalStatus.BLOCKED
    with pytest.raises(ValueError, match="blocked"):
        store.approve(proposal.approval_id, who="founder")

"""Agentic operations governance tests (contract suite)."""

from __future__ import annotations

from auto_client_acquisition.agentic_operations_os.agent_auditability_card import (
    AgentAuditabilityCard,
    agent_auditability_card_valid,
)
from auto_client_acquisition.agentic_operations_os.agent_governance import governance_decision_for_proposed_action
from auto_client_acquisition.agentic_operations_os.agent_identity import (
    AgentIdentityCard,
    agent_identity_valid,
    agent_operating_level_allowed_in_mvp,
)
from auto_client_acquisition.agentic_operations_os.agent_lifecycle import should_decommission
from auto_client_acquisition.agentic_operations_os.agent_permissions import (
    ToolClass,
    agent_tool_forbidden,
    permission_change_requires_audit,
    tool_class_allowed_in_mvp,
)
from auto_client_acquisition.agentic_operations_os.agent_risk_score import (
    AgentRiskDimensions,
    agent_risk_band,
    agent_risk_score,
)
from auto_client_acquisition.agentic_operations_os.agentic_operations_board import board_decision_for_tool_request
from auto_client_acquisition.agentic_operations_os.handoff import (
    HandoffObject,
    handoff_valid,
    pii_output_requires_handoff,
)


def test_agent_requires_identity_card() -> None:
    card = AgentIdentityCard(
        agent_id="",
        name="X",
        business_unit="Rev",
        owner="O",
        purpose="P",
        operating_level=2,
        status="active",
        created_at="2026-05-14",
        last_reviewed_at="2026-05-14",
    )
    ok, err = agent_identity_valid(card)
    assert not ok and "agent_id_required" in err


def test_agent_requires_owner() -> None:
    card = AgentIdentityCard(
        agent_id="AGT-1",
        name="X",
        business_unit="Rev",
        owner="",
        purpose="P",
        operating_level=2,
        status="active",
        created_at="2026-05-14",
        last_reviewed_at="2026-05-14",
    )
    ok, err = agent_identity_valid(card)
    assert not ok and "owner_required" in err


def test_agent_autonomy_mvp_limit() -> None:
    assert agent_operating_level_allowed_in_mvp(1) is True
    assert agent_operating_level_allowed_in_mvp(4) is True
    assert agent_operating_level_allowed_in_mvp(5) is False
    assert agent_operating_level_allowed_in_mvp(0) is False


def test_agent_forbidden_external_action() -> None:
    assert tool_class_allowed_in_mvp(ToolClass.EXTERNAL_ACTION, internal_write_approved=True) is False


def test_agent_no_scraping_tool() -> None:
    assert agent_tool_forbidden("scrape_web") is True


def test_agent_no_cold_whatsapp() -> None:
    assert agent_tool_forbidden("send_whatsapp") is True


def test_agent_tool_permission_audited() -> None:
    assert permission_change_requires_audit(frozenset(), frozenset({"a"})) is True


def test_agent_output_requires_governance() -> None:
    g = governance_decision_for_proposed_action(
        agent_id="AGT-1",
        proposed_action="send_proposal_email",
        contains_pii=False,
        external_channel=True,
    )
    assert g.decision == "DRAFT_ONLY"
    assert "external_action_requires_approval" in g.matched_rules


def test_agent_handoff_required_for_pii() -> None:
    assert not pii_output_requires_handoff(
        contains_pii=True,
        handoff_to="",
        required_action="review",
    )
    assert pii_output_requires_handoff(
        contains_pii=True,
        handoff_to="Owner",
        required_action="review_and_approve_or_reject",
    )


def test_agent_decommission_if_no_owner() -> None:
    assert should_decommission(owner_present=False, policy_violation=False) is True
    assert should_decommission(owner_present=True, policy_violation=False) is False


def test_handoff_valid() -> None:
    h = HandoffObject(
        handoff_id="H1",
        agent_id="AGT-1",
        output_id="OUT-1",
        handoff_to="",
        reason="r",
        required_action="a",
        deadline="d",
    )
    ok, err = handoff_valid(h)
    assert not ok


def test_agent_auditability_card_mvp() -> None:
    bad = AgentAuditabilityCard(
        agent_id="AGT-1",
        audit_scope=("inputs",),
        action_recoverability="required",
        lifecycle_coverage="full",
        policy_checkability="required",
        responsibility_attribution="required",
        evidence_integrity="append_only_logs_mvp",
        external_actions_allowed=True,
    )
    ok, err = agent_auditability_card_valid(bad)
    assert not ok and "external_actions_not_allowed_mvp" in err


def test_agent_risk_score_band() -> None:
    d = AgentRiskDimensions(10, 10, 10, 0, 90, 90, 0)
    s = agent_risk_score(d)
    assert s <= 35
    assert agent_risk_band(s) == "low"


def test_board_denies_external_tool_request() -> None:
    dec, _why = board_decision_for_tool_request(
        agent_name="Revenue Intelligence Agent",
        requested_tool="send_whatsapp",
    )
    assert dec == "deny_permission_keep_draft_only"


def test_governance_whatsapp_draft() -> None:
    g = governance_decision_for_proposed_action(
        agent_id="AGT-1",
        proposed_action="generate_whatsapp_draft",
        contains_pii=True,
        external_channel=False,
    )
    assert g.decision == "DRAFT_ONLY"
    assert "no_cold_whatsapp_automation" in g.matched_rules

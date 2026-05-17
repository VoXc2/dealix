"""Contract tests for Dealix Revenue Factory policy engine."""

from __future__ import annotations

from auto_client_acquisition.revenue_factory_os import (
    DEFAULT_AGENT_CONTRACTS,
    ApprovalRiskLevel,
    ApprovalType,
    AutomationLevel,
    approval_risk_for_type,
    classify_automation_level,
    contract_safety_violations,
    founder_approval_required,
    get_agent_contract,
    route_event_to_agents,
    validate_governed_event_chain,
)


def test_classify_automation_level_for_known_levels() -> None:
    assert classify_automation_level("lead_capture") == AutomationLevel.FULLY_AUTOMATED
    assert classify_automation_level("best_message") == AutomationLevel.AGENT_ASSISTED
    assert classify_automation_level("invoice_send") == AutomationLevel.FOUNDER_APPROVAL_REQUIRED


def test_external_like_action_defaults_to_founder_approval() -> None:
    assert classify_automation_level("send_partner_email") == AutomationLevel.FOUNDER_APPROVAL_REQUIRED


def test_founder_approval_required_flags_sensitive_impact() -> None:
    assert founder_approval_required("scope_draft") is False
    assert founder_approval_required("scope_draft", impacts_client=True) is True


def test_approval_risk_for_type_returns_expected_risk() -> None:
    assert approval_risk_for_type(ApprovalType.SECURITY_CLAIM) == ApprovalRiskLevel.CRITICAL
    assert approval_risk_for_type("external_message") == ApprovalRiskLevel.MEDIUM
    assert approval_risk_for_type("unknown_type") == ApprovalRiskLevel.CRITICAL


def test_validate_governed_event_chain_passes_valid_event() -> None:
    event = {
        "signal": "reply_received",
        "source": "linkedin_dm",
        "approval": "approved_by_founder",
        "action": "send_followup_email",
        "evidence": "evt_1001",
        "decision": "continue_conversation",
        "value": "meeting_booked",
        "asset": "objection_library_entry",
    }
    valid, errors = validate_governed_event_chain(event)
    assert valid is True
    assert errors == ()


def test_validate_governed_event_chain_blocks_external_without_approval() -> None:
    event = {
        "signal": "meeting_done",
        "source": "meeting_notes",
        "approval": "none",
        "action": "send_scope_email",
        "evidence": "evt_1002",
        "decision": "scope_next",
        "value": "scope_requested",
        "asset": "scope_template_v2",
    }
    valid, errors = validate_governed_event_chain(event)
    assert valid is False
    assert "external_action_without_approval" in errors


def test_route_event_to_agents_uses_governed_fallback() -> None:
    assert route_event_to_agents("meeting_done") == ("SalesCallCoachAgent", "ScopeBuilderAgent")
    assert route_event_to_agents("totally_new_event") == ("GovernanceRiskAgent",)


def test_has_fifteen_agent_contracts() -> None:
    assert len(DEFAULT_AGENT_CONTRACTS) == 15


def test_outreach_contract_is_draft_only_and_approval_gated() -> None:
    outreach = get_agent_contract("OutreachPersonalizationAgent")
    assert "external_send" in outreach.forbidden_actions
    assert "external_send" in outreach.approval_required_for


def test_all_contracts_enforce_source_and_external_send_rules() -> None:
    violations = {
        contract.name: contract_safety_violations(contract)
        for contract in DEFAULT_AGENT_CONTRACTS
    }
    # GovernanceRiskAgent is the only policy enforcer contract that is
    # allowed to not include external_send in approval_required_for.
    assert violations["GovernanceRiskAgent"] == ()
    for name, errs in violations.items():
        if name == "GovernanceRiskAgent":
            continue
        assert errs == (), f"{name} has safety violations: {errs}"

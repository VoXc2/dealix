"""Tests for the AI Workforce registry contract.

The registry is the source of truth for the 12 specialized agents.
These tests pin the hard rules (forbidden tools, approval-required
guard, no live action modes) so a future edit can't silently relax
the policy.
"""
from __future__ import annotations

from auto_client_acquisition.ai_workforce import (
    AGENT_REGISTRY,
    AgentSpec,
    AutonomyLevel,
    list_agents,
)


_EXPECTED_AGENTS: tuple[str, ...] = (
    "OrchestratorAgent",
    "CompanyBrainAgent",
    "MarketRadarAgent",
    "SalesStrategistAgent",
    "SaudiCopyAgent",
    "PartnershipAgent",
    "DeliveryAgent",
    "ProofAgent",
    "ComplianceGuardAgent",
    "ExecutiveBriefAgent",
    "FinanceAgent",
    "CustomerSuccessAgent",
)


def test_all_twelve_agents_present():
    """Registry must contain exactly the 12 specialized agents."""
    assert len(AGENT_REGISTRY) == 12
    for agent_id in _EXPECTED_AGENTS:
        assert agent_id in AGENT_REGISTRY, f"missing agent {agent_id}"
    assert {a.agent_id for a in list_agents()} == set(_EXPECTED_AGENTS)


def test_each_agent_has_required_fields_populated():
    """Every AgentSpec must have all required fields populated with sensible values."""
    for agent_id, spec in AGENT_REGISTRY.items():
        assert isinstance(spec, AgentSpec)
        assert spec.agent_id == agent_id
        assert spec.role_ar, f"{agent_id} missing role_ar"
        assert spec.role_en, f"{agent_id} missing role_en"
        assert spec.allowed_inputs, f"{agent_id} missing allowed_inputs"
        assert spec.allowed_outputs, f"{agent_id} missing allowed_outputs"
        assert spec.autonomy_level in {lvl.value for lvl in AutonomyLevel}
        assert spec.default_action_mode
        assert spec.cost_budget_usd >= 0


def test_compliance_guard_uses_approval_required_autonomy():
    """ComplianceGuardAgent's veto power MUST be expressed as approval_required."""
    spec = AGENT_REGISTRY["ComplianceGuardAgent"]
    assert spec.autonomy_level == AutonomyLevel.APPROVAL_REQUIRED.value


def test_saudi_copy_forbids_all_five_hard_rule_tools():
    """SaudiCopyAgent forbidden_tools must include the 5 cold/scrape tokens."""
    spec = AGENT_REGISTRY["SaudiCopyAgent"]
    required = {
        "cold_whatsapp",
        "linkedin_automation",
        "scrape_web",
        "send_email_live",
        "send_whatsapp_live",
    }
    assert required.issubset(set(spec.forbidden_tools))


def test_finance_agent_forbids_charge_payment_live():
    """FinanceAgent must forbid the live-charge token."""
    spec = AGENT_REGISTRY["FinanceAgent"]
    assert "charge_payment_live" in spec.forbidden_tools


def test_no_agent_has_live_default_action_mode():
    """No agent's default_action_mode may be a live-send/charge token."""
    forbidden_modes = {
        "live_send", "live_charge", "scrape", "linkedin_automation", "cold_whatsapp",
    }
    for agent_id, spec in AGENT_REGISTRY.items():
        assert spec.default_action_mode not in forbidden_modes, (
            f"{agent_id} has live default_action_mode {spec.default_action_mode!r}"
        )


def test_get_agent_raises_keyerror_for_unknown():
    """``get_agent`` must reject unknown agent_ids loudly."""
    from auto_client_acquisition.ai_workforce import get_agent

    import pytest

    with pytest.raises(KeyError):
        get_agent("NonExistentAgent")

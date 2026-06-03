"""Agent governance: registry completeness, permission bounds, and the rule
that no agent may autonomously perform a forbidden action or widen workflows."""

import pytest

from core.agents.registry import (
    AGENT_REGISTRY, REQUIRED_AGENT_FIELDS, list_agents, agents_by_permission_level,
)
from core.safety.constants import FORBIDDEN_ACTIONS, PERMISSION_LEVELS, RISK_LEVELS
from core.safety.permissions import (
    can_perform, is_forbidden_action, agent_can_change_workflow_permissions,
)

EXPECTED_AGENTS = [
    "Founder Command Agent", "Brand Guard Agent", "Offer Catalog Agent",
    "Product Catalog Agent", "Sector Intelligence Agent", "Signal Detection Agent",
    "Prospect Research Agent", "Draft Factory Agent", "Personalization Guard Agent",
    "Compliance Gate Agent", "Deliverability Agent", "Approval Queue Agent",
    "Sending Ramp Agent", "Reply Handling Agent", "WhatsApp Concierge Agent",
    "Client Assessment Agent", "Action Card Agent", "Permission Guard Agent",
    "Proposal Agent", "Proof Pack Agent", "Payment Handoff Agent",
    "Delivery Handoff Agent", "Renewal Agent", "Customer Success Agent",
    "Content Agent", "Press Agent", "Partnership Agent", "Finance Agent",
    "Privacy Guard Agent", "Security Red Team Agent", "QA/Eval Agent",
    "Metrics Agent", "Repo Integration Agent", "Frontend UX Agent",
    "Procurement Agent", "Data Room Agent", "Legal/Compliance Agent",
    "Saudi Localization Agent", "Productized Services Agent",
    "Infrastructure Reliability Agent",
]


def test_all_forty_agents_present():
    assert len(AGENT_REGISTRY) == 40
    for name in EXPECTED_AGENTS:
        assert name in AGENT_REGISTRY, f"missing agent: {name}"


def test_every_agent_has_required_fields():
    for agent in list_agents():
        for field in REQUIRED_AGENT_FIELDS:
            assert field in agent, f"{agent.get('name')} missing field {field}"
            assert agent[field] not in (None, ""), f"{agent['name']} empty {field}"


def test_every_agent_carries_global_forbidden_actions():
    for agent in list_agents():
        for forbidden in FORBIDDEN_ACTIONS:
            assert forbidden in agent["forbidden_actions"], (
                f"{agent['name']} does not forbid {forbidden}"
            )


def test_no_agent_may_perform_forbidden_action():
    for agent in list_agents():
        for forbidden in FORBIDDEN_ACTIONS:
            assert can_perform(agent["name"], forbidden) is False


def test_permission_and_risk_levels_are_valid():
    for agent in list_agents():
        assert agent["permission_level"] in PERMISSION_LEVELS
        # No agent should sit at L6 (forbidden autonomous action).
        assert agent["permission_level"] != "L6"
        assert agent["risk_level"] in RISK_LEVELS


def test_send_related_agents_require_approval():
    for name in ["Draft Factory Agent", "WhatsApp Concierge Agent",
                 "Proposal Agent", "Payment Handoff Agent", "Approval Queue Agent"]:
        assert AGENT_REGISTRY[name]["required_approval"] is True


def test_no_agent_can_change_workflow_permissions():
    for agent in list_agents():
        assert agent_can_change_workflow_permissions(agent["name"]) is False


def test_forbidden_action_helper():
    assert is_forbidden_action("external_send") is True
    assert is_forbidden_action("production_deploy") is True
    assert is_forbidden_action("read") is False


def test_permission_level_distribution_reported():
    dist = agents_by_permission_level()
    # Every level key exists; most agents are read/report/data tier.
    assert set(dist.keys()) >= set(PERMISSION_LEVELS.keys())

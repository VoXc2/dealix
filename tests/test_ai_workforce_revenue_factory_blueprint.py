"""Tests for the canonical Dealix Revenue + AI Ops Factory view."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.ai_workforce import build_revenue_factory_blueprint
from auto_client_acquisition.ai_workforce.canonical_delegation import (
    CANONICAL_AGENTS,
    REVENUE_SPECIALIST_DELEGATION,
    SPECIALIST_ROLE_SEMANTICS,
)
from auto_client_acquisition.ai_workforce.revenue_factory_blueprint import AutomationLevel


def test_blueprint_doctrine_chain_is_canonical():
    bp = build_revenue_factory_blueprint()
    assert bp["doctrine_chain"] == [
        "signal",
        "source",
        "approval",
        "action",
        "evidence",
        "decision",
        "value",
        "asset",
    ]


def test_blueprint_has_five_canonical_agents_and_fifteen_specialist_roles():
    bp = build_revenue_factory_blueprint()
    roles = {item["agent_id"] for item in bp["agent_contracts"]}
    assert bp["canonical_agents_total"] == 5
    assert set(bp["canonical_agents"]) == set(CANONICAL_AGENTS)
    assert bp["specialist_roles_total"] == 15
    assert bp["specialist_role_semantics"] == SPECIALIST_ROLE_SEMANTICS
    assert roles == set(REVENUE_SPECIALIST_DELEGATION)
    assert {item["canonical_owner"] for item in bp["agent_contracts"]} <= set(CANONICAL_AGENTS)
    assert "GovernanceRiskAgent" in roles
    assert "ScopeBuilderAgent" in roles
    assert "DeliveryDiagnosticAgent" in roles


def test_every_specialist_role_forbids_autonomous_external_send():
    bp = build_revenue_factory_blueprint()
    for contract in bp["agent_contracts"]:
        forbidden = set(contract["forbidden_actions"])
        assert forbidden.intersection(
            {"send_external_message", "cold_whatsapp_live", "send_scope_to_client"}
        ), f"{contract['agent_id']} lacks external-send guardrail"
        assert contract["canonical_owner"] in CANONICAL_AGENTS
        assert contract["role_semantics"] == SPECIALIST_ROLE_SEMANTICS


def test_blueprint_has_thirty_automation_plays_and_all_levels():
    bp = build_revenue_factory_blueprint()
    plays = bp["automation_plays"]
    assert len(plays) == 30
    assert [play["automation_id"] for play in plays] == list(range(1, 31))
    assert {play["level"] for play in plays} == {
        AutomationLevel.FULLY_AUTOMATED.value,
        AutomationLevel.AGENT_ASSISTED.value,
        AutomationLevel.FOUNDER_APPROVAL_REQUIRED.value,
    }
    assert all(slot["canonical_owner"] in CANONICAL_AGENTS for slot in bp["daily_schedule"])


def test_revenue_factory_blueprint_endpoint_returns_canonical_agent_truth():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/revenue-factory-blueprint")
    assert resp.status_code == 200
    body = resp.json()
    assert body["model"] == "dealix_agentic_revenue_ai_ops_factory"
    assert body["north_star"] == "governed_value_decisions_created"
    assert body["canonical_agents_total"] == 5
    assert set(body["canonical_agents"]) == set(CANONICAL_AGENTS)
    assert body["specialist_roles_total"] == 15
    assert body["specialist_role_semantics"] == SPECIALIST_ROLE_SEMANTICS
    assert body["agents_total"] == 15
    assert body["agents_total_semantics"] == "DEPRECATED_SPECIALIST_ROLE_COUNT"
    assert body["automation_plays_total"] == 30

"""Tests for the Dealix Revenue + AI Ops Factory blueprint."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.ai_workforce.revenue_factory_blueprint import (
    AutomationLevel,
    build_revenue_factory_blueprint,
)


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


def test_blueprint_contains_fifteen_core_agents():
    bp = build_revenue_factory_blueprint()
    ids = {a["agent_id"] for a in bp["agent_contracts"]}
    assert len(ids) == 15
    assert "GovernanceRiskAgent" in ids
    assert "ScopeBuilderAgent" in ids
    assert "DeliveryDiagnosticAgent" in ids


def test_every_agent_forbids_autonomous_external_send():
    bp = build_revenue_factory_blueprint()
    for contract in bp["agent_contracts"]:
        forbidden = set(contract["forbidden_actions"])
        assert forbidden.intersection(
            {"send_external_message", "cold_whatsapp_live", "send_scope_to_client"}
        ), f"{contract['agent_id']} lacks external-send guardrail"


def test_blueprint_has_thirty_automation_plays_and_all_levels():
    bp = build_revenue_factory_blueprint()
    plays = bp["automation_plays"]
    assert len(plays) == 30
    assert [p["automation_id"] for p in plays] == list(range(1, 31))
    assert {p["level"] for p in plays} == {
        AutomationLevel.FULLY_AUTOMATED.value,
        AutomationLevel.AGENT_ASSISTED.value,
        AutomationLevel.FOUNDER_APPROVAL_REQUIRED.value,
    }


def test_revenue_factory_blueprint_endpoint_returns_contract_summary():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/revenue-factory-blueprint")
    assert resp.status_code == 200
    body = resp.json()
    assert body["model"] == "dealix_agentic_revenue_ai_ops_factory"
    assert body["north_star"] == "governed_value_decisions_created"
    assert body["agents_total"] == 15
    assert body["automation_plays_total"] == 30

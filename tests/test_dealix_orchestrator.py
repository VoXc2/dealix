"""Tests for the DealixOrchestrator (PR6)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.dealix_orchestrator import (
    get_default_task_queue,
    reset_default_task_queue,
    run_automation,
)
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    list_evidence_events,
    reset_default_evidence_ledger,
)


@pytest.fixture
def orch_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path / "ev"))
    reset_default_task_queue()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()
    yield
    reset_default_task_queue()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()


def test_low_risk_automation_enqueues_pending_task(orch_env):
    result = run_automation("on_lead", entity_id="lead_1")
    assert result["requires_approval"] is False
    assert result["task_status"] == "pending"
    assert result["approval_id"] is None


def test_high_risk_automation_queues_approval(orch_env):
    result = run_automation("on_qualified", entity_id="lead_2")
    assert result["action"] == "first_outreach"
    assert result["requires_approval"] is True
    assert result["task_status"] == "awaiting_approval"
    assert result["approval_id"] is not None

    pending = get_default_approval_store().list_pending()
    assert any(p.object_id == "lead_2" for p in pending)


def test_automation_writes_evidence(orch_env):
    run_automation("on_lead", entity_id="lead_3")
    events = list_evidence_events(entity_type="lead", entity_id="lead_3")
    assert any(e.event_type == "automation_on_lead" for e in events)
    assert any(e.actor == "dealix_orchestrator" for e in events)


def test_unknown_automation_raises(orch_env):
    with pytest.raises(ValueError):
        run_automation("on_nonsense", entity_id="x")


async def test_orchestrator_status_endpoint(orch_env, async_client):
    resp = await async_client.get("/api/v1/orchestrator/status")
    assert resp.status_code == 200
    body = resp.json()
    assert "on_qualified" in body["automations"]
    assert body["guardrails"]["high_risk_actions_always_approval_gated"] is True


async def test_orchestrator_agents_endpoint(orch_env, async_client):
    resp = await async_client.get("/api/v1/orchestrator/agents")
    assert resp.status_code == 200
    assert resp.json()["count"] == 11


async def test_orchestrator_trigger_endpoint(orch_env, async_client):
    resp = await async_client.post(
        "/api/v1/orchestrator/trigger/on_scope", json={"entity_id": "opp_1"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["requires_approval"] is True
    assert body["task_status"] == "awaiting_approval"

    tasks = await async_client.get("/api/v1/orchestrator/tasks")
    assert tasks.json()["count"] >= 1


async def test_policy_check_endpoint(orch_env, async_client):
    resp = await async_client.post(
        "/api/v1/orchestrator/policy/check",
        json={
            "action": "invoice_send",
            "claim": "we guarantee a 30% ROI",
            "source": None,
            "from_stage": "new_lead",
            "to_stage": "invoice_sent",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["action"]["requires_approval"] is True
    assert body["claim"]["ok"] is False
    assert body["stage_transition"]["allowed"] is False

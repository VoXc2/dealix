"""Integration tests for the /api/v1/sales-loop router."""
from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.sales_os import sales_loop_orchestrator as slo

pytestmark = pytest.mark.integration

_PAYLOAD = {
    "company": "Acme Retail",
    "email": "ops@acme-retail.sa",
    "sector": "retail",
    "region": "riyadh",
}


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_SALES_LOOP_LEDGER_PATH", str(tmp_path / "loop.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    monkeypatch.setenv("VALUE_LEDGER_BACKEND", "jsonl")
    slo.clear_for_test()
    get_default_pipeline().reset()
    yield


async def test_status_endpoint(async_client):
    resp = await async_client.get("/api/v1/sales-loop/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "sales_loop"
    assert body["hard_gates"]["approval_required_for_external_actions"] is True


async def test_start_then_get(async_client):
    start = await async_client.post(
        "/api/v1/sales-loop/start",
        json={"raw_payload": _PAYLOAD, "source": "manual", "customer_handle": "acme-co"},
    )
    assert start.status_code == 200
    loop_id = start.json()["loop"]["loop_id"]

    got = await async_client.get(f"/api/v1/sales-loop/{loop_id}")
    assert got.status_code == 200
    body = got.json()
    assert body["loop"]["stage"] == "message_drafted"
    assert "next_actions" in body
    assert "audit_events" in body


async def test_advance_with_open_gate_returns_409(async_client):
    start = await async_client.post(
        "/api/v1/sales-loop/start",
        json={"raw_payload": _PAYLOAD, "source": "manual", "customer_handle": "acme-co"},
    )
    loop_id = start.json()["loop"]["loop_id"]
    resp = await async_client.post(
        "/api/v1/sales-loop/advance",
        json={"loop_id": loop_id, "target_stage": "founder_sent_manually", "actor": "founder"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["error"] == "approval_gate_open"


async def test_resolve_approval_then_advance(async_client):
    start = await async_client.post(
        "/api/v1/sales-loop/start",
        json={"raw_payload": _PAYLOAD, "source": "manual", "customer_handle": "acme-co"},
    )
    loop = start.json()["loop"]
    loop_id, approval_id = loop["loop_id"], loop["pending_approval_id"]

    resolved = await async_client.post(
        f"/api/v1/sales-loop/{loop_id}/resolve-approval",
        json={"approval_id": approval_id, "decision": "approve", "who": "founder"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["loop"]["pending_approval_id"] is None

    advanced = await async_client.post(
        "/api/v1/sales-loop/advance",
        json={"loop_id": loop_id, "target_stage": "founder_sent_manually", "actor": "founder"},
    )
    assert advanced.status_code == 200
    assert advanced.json()["loop"]["stage"] == "founder_sent_manually"


async def test_unknown_loop_returns_404(async_client):
    got = await async_client.get("/api/v1/sales-loop/loop_missing")
    assert got.status_code == 404
    adv = await async_client.post(
        "/api/v1/sales-loop/advance",
        json={"loop_id": "loop_missing", "target_stage": "replied", "actor": "founder"},
    )
    assert adv.status_code == 404


async def test_invalid_transition_returns_400(async_client):
    start = await async_client.post(
        "/api/v1/sales-loop/start",
        json={"raw_payload": _PAYLOAD, "source": "manual", "customer_handle": "acme-co"},
    )
    loop = start.json()["loop"]
    loop_id, approval_id = loop["loop_id"], loop["pending_approval_id"]
    await async_client.post(
        f"/api/v1/sales-loop/{loop_id}/resolve-approval",
        json={"approval_id": approval_id, "decision": "approve", "who": "founder"},
    )
    # payment_received is a valid stage but an invalid transition from here.
    resp = await async_client.post(
        "/api/v1/sales-loop/advance",
        json={"loop_id": loop_id, "target_stage": "payment_received", "actor": "founder"},
    )
    assert resp.status_code == 400


async def test_list_loops(async_client):
    await async_client.post(
        "/api/v1/sales-loop/start",
        json={"raw_payload": _PAYLOAD, "source": "manual", "customer_handle": "acme-co"},
    )
    resp = await async_client.get("/api/v1/sales-loop")
    assert resp.status_code == 200
    assert len(resp.json()["loops"]) >= 1

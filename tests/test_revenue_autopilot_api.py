"""Revenue Autopilot router — TestClient round-trip."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.revenue_autopilot import orchestrator

client = TestClient(app)

_QUALIFIED_A = {
    "is_decision_maker": True, "is_b2b_company": True,
    "has_revenue_workflow": True, "uses_or_plans_ai": True,
}


@pytest.fixture(autouse=True)
def _reset():
    orchestrator.reset()
    yield
    orchestrator.reset()


def test_funnel_stages_endpoint():
    resp = client.get("/api/v1/revenue-autopilot/funnel/stages")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "new_lead" in body["stages"]
    assert "invoice_paid" in body["revenue_stages"]
    assert body["transitions"]["closed_lost"] == []


def test_capture_lead_and_read_engagement():
    resp = client.post(
        "/api/v1/revenue-autopilot/lead",
        json={"contact": {"company": "Acme"}, "signals": _QUALIFIED_A},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    engagement = body["engagement"]
    assert engagement["current_stage"] == "qualified_A"
    assert engagement["lead_score"]["points"] == 12
    assert body["hard_gates"]["no_live_send"] is True

    eid = engagement["engagement_id"]
    read = client.get(f"/api/v1/revenue-autopilot/engagements/{eid}")
    assert read.status_code == 200
    # First-response email draft is queued for approval, not sent.
    assert len(read.json()["pending_approvals"]) >= 1


def test_full_funnel_round_trip():
    eid = client.post(
        "/api/v1/revenue-autopilot/lead",
        json={"contact": {}, "signals": _QUALIFIED_A},
    ).json()["engagement"]["engagement_id"]

    base = f"/api/v1/revenue-autopilot/engagements/{eid}"
    assert client.post(f"{base}/automations/qualified_lead").status_code == 200
    assert client.post(f"{base}/automations/meeting_booked").status_code == 200
    assert client.post(
        f"{base}/automations/meeting_done", json={"scope_requested": True}
    ).status_code == 200
    assert client.post(f"{base}/automations/scope_requested").status_code == 200
    assert client.post(
        f"{base}/advance", json={"target": "invoice_sent"}
    ).status_code == 200
    assert client.post(f"{base}/automations/invoice_paid").status_code == 200
    assert client.post(f"{base}/automations/delivery").status_code == 200
    resp = client.post(f"{base}/automations/proof_pack_sent")
    assert resp.status_code == 200
    assert resp.json()["engagement"]["current_stage"] == "proof_pack_sent"


def test_illegal_automation_precondition_returns_400():
    eid = client.post(
        "/api/v1/revenue-autopilot/lead",
        json={"contact": {}, "signals": _QUALIFIED_A},
    ).json()["engagement"]["engagement_id"]
    # invoice_paid before invoice_sent — governed refusal.
    resp = client.post(
        f"/api/v1/revenue-autopilot/engagements/{eid}/automations/invoice_paid"
    )
    assert resp.status_code == 400


def test_unknown_engagement_returns_404():
    resp = client.get("/api/v1/revenue-autopilot/engagements/eng_does_not_exist")
    assert resp.status_code == 404

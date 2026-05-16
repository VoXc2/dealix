"""Tests for the /api/v1/board-decision-os/overview endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.revenue_memory.event_store import reset_default_store

client = TestClient(app)


def _record(customer_id: str, subject_id: str, next_state: str, **kwargs: object):
    payload = {
        "customer_id": customer_id,
        "subject_type": "account",
        "subject_id": subject_id,
        "next_state": next_state,
    }
    payload.update(kwargs)
    resp = client.post("/api/v1/evidence/events", json=payload)
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_overview_shape_with_no_events() -> None:
    reset_default_store()
    resp = client.get(
        "/api/v1/board-decision-os/overview", params={"customer_id": "cust_b0"}
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["north_star"]["metric"] == "Governed Value Decisions Created"
    assert body["north_star"]["count"] == 0
    assert set(body["gates"].keys()) == {
        "G1", "G2", "G3", "G4", "G5", "G6", "G7"
    }
    assert body["gates_passed"] == []
    assert body["cel_summary"]["engagements"] == 0
    assert body["governance_decision"] == "approval_required"


def test_overview_counts_north_star_on_invoice_paid() -> None:
    reset_default_store()
    cust = "cust_b1"
    sid = "acc_b1"
    _record(cust, sid, "prepared_not_sent")
    _record(cust, sid, "sent", founder_confirmed=True)
    _record(cust, sid, "replied_interested")
    _record(cust, sid, "meeting_booked")
    _record(cust, sid, "used_in_meeting", used_in_meeting=True)
    _record(cust, sid, "scope_requested", scope_or_intro_requested=True)
    _record(cust, sid, "invoice_sent")
    _record(cust, sid, "invoice_paid", invoice_paid=True)

    resp = client.get(
        "/api/v1/board-decision-os/overview", params={"customer_id": cust}
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    # One engagement reached CEL7_confirmed -> North Star count is 1.
    assert body["north_star"]["count"] == 1
    assert body["cel_summary"]["by_cel"].get("CEL7_confirmed") == 1
    # G2, G3, G4 should be passed for this paid engagement.
    assert body["gates"]["G4"]["passed"] is True
    assert "G4" in body["gates_passed"]


def test_overview_reflects_active_retainer_flag() -> None:
    reset_default_store()
    resp = client.get(
        "/api/v1/board-decision-os/overview",
        params={"customer_id": "cust_b2", "has_active_retainer": True},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["gates"]["G6"]["passed"] is True

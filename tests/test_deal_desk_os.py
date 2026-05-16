"""Deal Desk OS — draft only."""

from __future__ import annotations

from fastapi.testclient import TestClient

from auto_client_acquisition.commercial_engagements.deal_desk_os import (
    create_deal_desk_request,
    objection_intelligence_hints,
    record_approval,
    reset_store_for_tests,
    submit_for_approval,
)
from api.main import app

client = TestClient(app)


def setup_function() -> None:
    reset_store_for_tests()


def test_deal_desk_draft_flow() -> None:
    req = create_deal_desk_request(
        company="Acme SA",
        offer_tier="pilot_499",
        amount_sar=499.0,
        objection_tags=["price"],
    )
    assert req.status == "draft"
    hints = objection_intelligence_hints(["price"])
    assert hints
    submitted = submit_for_approval(req.request_id)
    assert submitted.status == "pending_approval"
    approved = record_approval(req.request_id, approved=True, approver_note="ok")
    assert approved.status == "approved"


def test_deal_desk_api_create() -> None:
    resp = client.post(
        "/api/v1/commercial/deal-desk/requests",
        json={
            "company": "Test Co",
            "offer_tier": "pilot_499",
            "amount_sar": 499,
            "objection_tags": ["trust"],
        },
    )
    assert resp.status_code == 200
    assert resp.json()["external_send"] is False

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.governed_revenue_ops_diagnostic import reset_store_for_tests


def _lead_payload() -> dict[str, object]:
    return {
        "name": "Sami",
        "company": "Dealix Test Co",
        "role": "Founder",
        "email": "sami@test.sa",
        "linkedin_url": "https://linkedin.com/in/sami",
        "industry": "B2B Services",
        "team_size": "35",
        "current_crm": "HubSpot",
        "ai_usage_today": "AI drafts in sales ops",
        "main_pain": "Pipeline follow-up is inconsistent and approval boundaries are unclear.",
        "urgency": "within 30 days",
        "budget_range": "5000+ SAR",
        "permission_to_contact": True,
        "source": "landing",
        "region": "Saudi Arabia",
    }


@pytest.mark.asyncio
async def test_status_and_sample_pack_endpoints_work() -> None:
    from api.main import app

    reset_store_for_tests()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        status_resp = await client.get("/api/v1/governed-diagnostic/status")
        sample_resp = await client.get("/api/v1/governed-diagnostic/sample-proof-pack")

    assert status_resp.status_code == 200
    assert status_resp.json()["guardrails"]["no_invoice_sent_before_scope_sent"] is True
    assert sample_resp.status_code == 200
    assert "Workflow Map" in sample_resp.json()["sections"]


@pytest.mark.asyncio
async def test_capture_and_progress_funnel() -> None:
    from api.main import app

    reset_store_for_tests()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        capture = await client.post("/api/v1/governed-diagnostic/lead-capture", json=_lead_payload())
        assert capture.status_code == 200
        body = capture.json()
        funnel_id = body["funnel_id"]
        assert body["state"] == "qualified_A"
        assert body["lead_grade"] == "A"

        invalid = await client.post(
            "/api/v1/governed-diagnostic/advance-state",
            json={"funnel_id": funnel_id, "target_state": "invoice_sent"},
        )
        assert invalid.status_code == 409

        meeting = await client.post(
            "/api/v1/governed-diagnostic/advance-state",
            json={"funnel_id": funnel_id, "target_state": "meeting_booked"},
        )
        assert meeting.status_code == 200

        brief = await client.post("/api/v1/governed-diagnostic/meeting-brief", json={"funnel_id": funnel_id})
        assert brief.status_code == 200
        assert len(brief.json()["meeting_brief"]["discovery_questions"]) == 3

        await client.post(
            "/api/v1/governed-diagnostic/advance-state",
            json={"funnel_id": funnel_id, "target_state": "meeting_done"},
        )
        await client.post(
            "/api/v1/governed-diagnostic/advance-state",
            json={"funnel_id": funnel_id, "target_state": "scope_requested"},
        )
        scope = await client.post(
            "/api/v1/governed-diagnostic/scope-draft",
            json={"funnel_id": funnel_id, "tier": "starter"},
        )
        assert scope.status_code == 200

        await client.post(
            "/api/v1/governed-diagnostic/advance-state",
            json={"funnel_id": funnel_id, "target_state": "scope_sent"},
        )
        invoice = await client.post(
            "/api/v1/governed-diagnostic/invoice-draft",
            json={
                "funnel_id": funnel_id,
                "tier": "starter",
                "payment_method": "payment_link_external",
            },
        )
        assert invoice.status_code == 200
        assert invoice.json()["invoice_draft"]["amount_sar"] == 4999

        board = await client.get("/api/v1/governed-diagnostic/daily-dashboard")
        assert board.status_code == 200
        assert board.json()["kpis"]["qualified_A"] >= 1

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_public_lead_capture_and_sales_flow() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        lead_resp = await client.post(
            "/api/v1/public/leads",
            json={
                "name": "Sami",
                "email": "sami@example.sa",
                "company": "Dealix Labs",
                "role": "Founder",
                "pain": "We need governed lead-to-cash automation",
                "budget": 8000,
                "urgency": "within 30 days",
                "consent": True,
            },
        )
        assert lead_resp.status_code == 200, lead_resp.text
        lead = lead_resp.json()["lead"]
        assert lead["lead_score"] >= 10
        assert lead["stage"] in {"qualified_A", "qualified_B", "nurture", "new_lead"}

        list_resp = await client.get("/api/v1/leads")
        assert list_resp.status_code == 200
        assert list_resp.json()["count"] >= 1

        draft_resp = await client.post(f"/api/v1/leads/{lead['id']}/draft-message", json={})
        assert draft_resp.status_code == 200, draft_resp.text
        draft_body = draft_resp.json()
        assert draft_body["requires_approval"] is True
        assert draft_body["approval"]["status"] == "pending"

        approvals_resp = await client.get("/api/v1/approvals")
        assert approvals_resp.status_code == 200
        assert approvals_resp.json()["pending_count"] >= 1


@pytest.mark.asyncio
async def test_support_knowledge_and_escalation_flow() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ticket_resp = await client.post(
            "/api/v1/support/tickets",
            json={
                "message": "I want a refund now.",
                "subject": "refund request",
                "channel": "email",
            },
        )
        assert ticket_resp.status_code == 200, ticket_resp.text
        ticket_body = ticket_resp.json()
        assert ticket_body["ticket"]["risk_level"] in {"high", "medium"}
        assert ticket_body["approval"] is not None

        suggest_resp = await client.post(
            "/api/v1/knowledge/suggest-answer",
            json={"question": "What is Dealix?", "locale": "en"},
        )
        assert suggest_resp.status_code == 200
        suggest_body = suggest_resp.json()
        assert suggest_body["found"] is True
        assert suggest_body["sources"]

        list_resp = await client.get("/api/v1/support/tickets")
        assert list_resp.status_code == 200
        assert list_resp.json()["count"] >= 1


@pytest.mark.asyncio
async def test_diagnostic_invoice_and_reporting_flow() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        diag_resp = await client.post("/api/v1/diagnostics", json={"lead_id": "lead_demo"})
        assert diag_resp.status_code == 200, diag_resp.text
        diagnostic_id = diag_resp.json()["diagnostic"]["id"]

        proof_resp = await client.post(f"/api/v1/diagnostics/{diagnostic_id}/generate-proof-pack")
        assert proof_resp.status_code == 200, proof_resp.text
        proof_body = proof_resp.json()
        assert proof_body["approval"]["type"] == "diagnostic_final"

        inv_resp = await client.post(
            "/api/v1/invoices/draft",
            json={
                "customer_email": "ops@example.sa",
                "tier_id": "diagnostic_499",
            },
        )
        assert inv_resp.status_code == 200, inv_resp.text
        invoice_id = inv_resp.json()["invoice"]["id"]

        approve_resp = await client.post(
            f"/api/v1/invoices/{invoice_id}/approve-send",
            json={"approved_by": "sami"},
        )
        assert approve_resp.status_code == 200
        assert approve_resp.json()["invoice"]["status"] == "approved_to_send"

        paid_resp = await client.post(
            f"/api/v1/invoices/{invoice_id}/mark-paid",
            json={"payment_ref": "pay_123"},
        )
        assert paid_resp.status_code == 200
        assert paid_resp.json()["invoice"]["status"] == "paid"

        overview_resp = await client.get("/api/v1/billing/overview")
        assert overview_resp.status_code == 200
        assert overview_resp.json()["paid_count"] >= 1

        report_resp = await client.get("/api/v1/reports/founder-command-center")
        assert report_resp.status_code == 200
        metrics = report_resp.json()["metrics"]
        assert "new_leads_today" in metrics
        assert "blocked_approvals" in metrics


@pytest.mark.asyncio
async def test_approval_alias_endpoints() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post(
            "/api/v1/approvals",
            json={
                "object_type": "scope",
                "object_id": "scope_1",
                "action_type": "delivery_task",
                "action_mode": "approval_required",
                "summary_ar": "مسودة نطاق",
                "summary_en": "Scope draft",
                "risk_level": "medium",
                "proof_impact": "scope_ready",
            },
        )
        assert create_resp.status_code == 200, create_resp.text
        approval_id = create_resp.json()["approval"]["approval_id"]

        edit_resp = await client.post(
            f"/api/v1/approvals/{approval_id}/request-edits",
            json={"who": "sami", "patch": {"summary_en": "Scope draft v2"}},
        )
        assert edit_resp.status_code == 200
        assert edit_resp.json()["approval"]["summary_en"] == "Scope draft v2"


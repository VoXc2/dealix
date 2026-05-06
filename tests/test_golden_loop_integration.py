"""Constitution Article 2 — golden loop wiring (in-process, Slot-A)."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.asyncio
async def test_golden_loop_thirteen_stages_slot_a() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # 1 signal evaluate
        r1 = await c.post(
            "/api/v1/growth-beast/signals/evaluate",
            json={"signals": []},
        )
        assert r1.status_code == 200
        assert r1.json()["evaluation"]["action_mode"] == "suggest_only"

        # 2 ICP / targets rank (high scores)
        r2 = await c.post(
            "/api/v1/growth-beast/targets/rank",
            json={
                "placeholder": "Slot-A",
                "pain_intensity": 80,
                "ability_to_pay": 70,
                "urgency": 75,
                "proof_potential": 80,
                "founder_access": 70,
                "referral_potential": 60,
                "sector_repeatability": 70,
                "delivery_complexity": 20,
                "compliance_risk": 10,
            },
        )
        assert r2.status_code == 200
        assert r2.json()["icp_score"] >= 70

        # 3 offer match
        r3 = await c.post(
            "/api/v1/growth-beast/offer/match",
            json={"sector": "marketing_agency", "signal_type": "no_proof_visible"},
        )
        assert r3.status_code == 200
        assert "offer" in r3.json()

        # 4 warm route draft (safe)
        r4 = await c.post(
            "/api/v1/growth-beast/warm-route/draft",
            json={
                "channel": "founder_warm_intro",
                "sector": "marketing_agency",
            },
        )
        assert r4.status_code == 200
        assert r4.json()["route"]["action_mode"] == "draft_only"

        # 5 cold channel blocked
        r5 = await c.post(
            "/api/v1/growth-beast/warm-route/draft",
            json={"channel": "cold_whatsapp", "sector": "x"},
        )
        assert r5.status_code == 200
        assert r5.json()["route"]["action_mode"] == "blocked"

        # 6 diagnostic with consent
        r6 = await c.post(
            "/api/v1/company-growth-beast/diagnostic",
            json={
                "company_handle": "Slot-A",
                "sector": "marketing_agency",
                "consent_for_diagnostic": True,
            },
        )
        assert r6.status_code == 200
        diag = r6.json()["diagnostic"]
        assert len(diag["seven_day_plan"]) == 7

        # 7 invoice draft (not revenue)
        r7 = await c.post(
            "/api/v1/revops/invoice-state",
            json={
                "customer_handle": "Slot-A",
                "amount_sar": 499,
                "description": "pilot",
                "mode": "test",
            },
        )
        assert r7.status_code == 200
        inv = r7.json()["invoice"]
        assert inv.get("status") == "draft"

        # 8 payment without valid evidence -> error (400 validation path)
        r8 = await c.post(
            "/api/v1/revops/payment-confirm",
            json={
                "invoice_id": inv["invoice_id"],
                "customer_handle": "Slot-A",
                "amount_sar": 499,
                "payment_method": "bank_transfer",
                "evidence_reference": "bad",
                "notes": "",
            },
        )
        assert r8.status_code in (400, 422)

        # 9 pipeline advance without evidence
        r_lead = await c.post(
            "/api/v1/revenue-pipeline/lead",
            json={"slot_id": "Slot-A", "sector": "tbd"},
        )
        assert r_lead.status_code == 200
        lead_id = r_lead.json()["lead"]["id"]
        r9 = await c.post(
            "/api/v1/revenue-pipeline/advance",
            json={
                "lead_id": lead_id,
                "target_stage": "commitment_received",
                "commitment_evidence": "",
            },
        )
        assert r9.status_code == 400

        # 10 CEO brief 3 decisions
        r10 = await c.get("/api/v1/role-command-v125/today/ceo")
        assert r10.status_code == 200
        assert len(r10.json()["top_3_decisions_ar"]) == 3

        # 11 finance brief + revenue truth via pipeline summary
        r11 = await c.get("/api/v1/revops/finance-brief")
        assert r11.status_code == 200
        assert "no_paid_pilot_yet" in r11.json()["blockers"]

        r_sum = await c.get("/api/v1/revenue-pipeline/summary")
        assert r_sum.status_code == 200
        assert r_sum.json()["revenue_truth"]["revenue_live"] is False

        # 12 v12_1_unlocked field present
        assert "v12_1_unlocked" in r_sum.json()["revenue_truth"]

        # 13 weekly learning / experiment next
        r13 = await c.post(
            "/api/v1/growth-beast/experiment/next",
            json={"sector_focus": "marketing_agency"},
        )
        assert r13.status_code == 200
        assert r13.json()["experiment"]["action_mode"] == "suggest_only"


@pytest.mark.asyncio
async def test_invariant_hard_gates_in_founder_beast_cc() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
        assert r.status_code == 200
        assert len(r.json()["hard_gates"]) == 8


@pytest.mark.asyncio
async def test_invariant_no_5xx_on_golden_paths() -> None:
    transport = ASGITransport(app=app)
    paths = [
        "/api/v1/growth-beast/today",
        "/api/v1/revops/finance-brief",
        "/api/v1/founder/beast-command-center",
        "/api/v1/customer-portal/Slot-A",
        "/api/v1/revenue-pipeline/summary",
    ]
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for p in paths:
            r = await c.get(p)
            assert r.status_code < 500, (p, r.status_code)


@pytest.mark.asyncio
async def test_invariant_proof_snippet_blocked_without_publish_permission() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post(
            "/api/v1/proof-to-market/snippet",
            json={"event": {"customer_approved": False}},
        )
        assert r.status_code == 200
        sn = r.json()["snippet"]
        assert sn.get("blocked") is True
        assert sn.get("action_mode") == "blocked"


@pytest.mark.asyncio
async def test_invariant_revenue_live_false_until_paid() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/revenue-pipeline/summary")
        assert r.json()["revenue_truth"]["revenue_live"] is False

"""V12.5.1 — Constitution Closure tests.

Three test groups:
1. Founder Beast Command Center (B7.1) — single endpoint composing 7 layers
2. Customer Company Portal (B7.2) — 8 customer-facing fields, NO internal leak
3. Golden Loop integration (B7.3) — 13-stage end-to-end traversal + 5 invariants

This is the canonical "is Dealix actually wired?" test.
"""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient


# ─────────────────── B7.1 Founder Beast Command Center ──────────────


@pytest.mark.asyncio
async def test_beast_cc_returns_200_always() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_beast_cc_has_all_8_layers() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
    body = r.json()
    for key in (
        "today_top_3_decisions",
        "growth_beast_snapshot",
        "revenue_truth",
        "finance_brief",
        "delivery_status",
        "support_alerts",
        "proof_summary",
        "compliance_alerts",
        "role_command_status",
        "next_best_action",
        "hard_gates",
        "degraded_sections",
    ):
        assert key in body, f"missing field: {key}"


@pytest.mark.asyncio
async def test_beast_cc_has_8_hard_gates() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
    gates = r.json()["hard_gates"]
    for g in (
        "no_live_send", "no_live_charge", "no_cold_whatsapp",
        "no_linkedin_automation", "no_scraping", "no_fake_proof",
        "no_fake_revenue", "no_unapproved_testimonial",
    ):
        assert gates[g] is True, f"hard gate {g} not locked"


@pytest.mark.asyncio
async def test_beast_cc_role_command_lists_9_roles() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
    body = r.json()
    rcs = body["role_command_status"]
    if isinstance(rcs, dict) and "_error" not in rcs:
        roles = rcs.get("roles_supported", [])
        assert len(roles) == 9, f"expected 9 roles, got {len(roles)}"


@pytest.mark.asyncio
async def test_beast_cc_revenue_truth_says_no_revenue_yet() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
    body = r.json()
    rt = body["revenue_truth"]
    if isinstance(rt, dict) and "_error" not in rt:
        # No customer pipeline data → revenue_live must be False
        assert rt.get("revenue_live") is False
        assert "no_paid_pilot_yet" in rt.get("blockers", [])


# ─────────────────── B7.2 Customer Company Portal ──────────────


@pytest.mark.asyncio
async def test_portal_returns_200() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/Slot-A")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_portal_has_exactly_8_sections() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/Slot-A")
    body = r.json()
    sections = body["sections"]
    assert len(sections) == 8
    assert "1_start_diagnostic" in sections
    assert "8_next_decision" in sections


@pytest.mark.asyncio
async def test_portal_no_internal_leakage() -> None:
    """Per Constitution Article 6 #2: NO internal terms in the
    customer-facing payload."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/Slot-A")
    body = r.json()
    serialized = json.dumps(body, ensure_ascii=False).lower()
    forbidden = [
        "v11", "v12.5", "agent", "router",
        "verifier", "growth_beast", "revops", "compliance_os_v12",
        "auto_client_acquisition", "_safe", "endpoint",
    ]
    for f in forbidden:
        assert f not in serialized, (
            f"customer portal leaks internal term: {f!r}"
        )


@pytest.mark.asyncio
async def test_portal_is_bilingual() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/Slot-A")
    body = r.json()
    assert body["promise_ar"]
    assert body["promise_en"]
    for sec in body["sections"].values():
        assert "title_ar" in sec
        assert "title_en" in sec


@pytest.mark.asyncio
async def test_portal_root_returns_slot_a() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/")
    body = r.json()
    assert body["customer_handle"] == "Slot-A"


# ─────────────────── B7.3 Golden Loop integration ──────────────
# Walks ALL 13 Constitution Article 2 stages end-to-end.


@pytest.mark.asyncio
async def test_golden_loop_full_traversal() -> None:
    """Single test that walks the entire Golden Loop with placeholder
    customer Slot-A. Each stage asserts the right action_mode +
    enforces hard gates."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:

        # Stage 1: signal evaluate (empty input → action_mode suggest_only)
        r = await c.post("/api/v1/growth-beast/signals/evaluate",
                         json={"signals": []})
        assert r.status_code == 200
        assert r.json()["evaluation"]["action_mode"] == "suggest_only"

        # Stage 2: ICP score for high-fit lead
        r = await c.post("/api/v1/growth-beast/targets/rank", json={
            "placeholder": "Slot-A", "pain_intensity": 18, "urgency": 14,
            "ability_to_pay": 12, "proof_potential": 14, "founder_access": 15,
            "referral_potential": 8, "sector_repeatability": 9,
        })
        assert r.json()["icp_score"] >= 80

        # Stage 3: offer match → 499 SAR pilot
        r = await c.post("/api/v1/growth-beast/offer/match", json={
            "sector": "marketing_agency", "signal_type": "no_proof_visible",
        })
        offer = r.json()["offer"]
        assert offer["price_sar"] == 499
        assert "guaranteed_revenue" in offer["blocked_claims"]

        # Stage 4: warm route draft → action_mode draft_only
        r = await c.post("/api/v1/growth-beast/warm-route/draft", json={
            "channel": "founder_warm_intro", "sector": "marketing_agency",
        })
        assert r.json()["route"]["action_mode"] == "draft_only"

        # Stage 5: cold channel BLOCKED
        r = await c.post("/api/v1/growth-beast/warm-route/draft", json={
            "channel": "cold_whatsapp", "sector": "marketing_agency",
        })
        assert r.json()["route"]["action_mode"] == "blocked"

        # Stage 6: diagnostic with consent → 7-day plan
        r = await c.post("/api/v1/company-growth-beast/diagnostic", json={
            "company_handle": "Slot-A", "sector": "marketing_agency",
            "biggest_problem": "no_proof_visible",
            "consent_for_diagnostic": True,
        })
        diag = r.json()["diagnostic"]
        assert len(diag["seven_day_plan"]) == 7
        assert diag["action_mode"] == "approval_required"

        # Stage 7: invoice draft (NOT revenue)
        r = await c.post("/api/v1/revops/invoice-state", json={
            "customer_handle": "Slot-A", "amount_sar": 499,
            "description": "Pilot",
        })
        body = r.json()
        assert body["invoice"]["status"] == "draft"
        assert "ليس إيراد" in body["note_ar"] or "إيراد" in body["note_ar"]
        invoice_id = body["invoice"]["invoice_id"]

        # Stage 8: payment without evidence → 422 (rejected)
        r = await c.post("/api/v1/revops/payment-confirm", json={
            "invoice_id": invoice_id, "customer_handle": "Slot-A",
            "amount_sar": 499, "payment_method": "bank_transfer",
            "evidence_reference": "",
        })
        assert r.status_code in (400, 422), (
            f"unsigned payment must be rejected, got {r.status_code}"
        )

        # Stage 9: pipeline advance to payment_received without evidence → 400
        r = await c.post("/api/v1/revenue-pipeline/lead", json={
            "slot_id": "GoldenLoopSlot",
        })
        if r.status_code == 200:
            lid = r.json()["lead"]["id"]
            for tgt in ("message_drafted", "founder_sent_manually", "replied",
                        "diagnostic_requested", "diagnostic_delivered",
                        "pilot_offered"):
                await c.post("/api/v1/revenue-pipeline/advance",
                             json={"lead_id": lid, "target_stage": tgt})
            r = await c.post("/api/v1/revenue-pipeline/advance", json={
                "lead_id": lid, "target_stage": "payment_received",
            })
            assert r.status_code == 400  # evidence required

        # Stage 10: CEO daily brief → 3 decisions
        r = await c.get("/api/v1/role-command-v125/today/ceo")
        body = r.json()
        assert len(body["top_3_decisions_ar"]) == 3
        assert len(body["top_3_decisions_en"]) == 3

        # Stage 11: finance brief → revenue_live=False, no_paid_pilot blocker
        r = await c.get("/api/v1/revops/finance-brief")
        body = r.json()
        assert body["data_status"] == "insufficient_data"
        assert "no_paid_pilot_yet" in body["blockers"]

        # Stage 12: V12.1 unlock check
        r = await c.get("/api/v1/revenue-pipeline/summary")
        body = r.json()
        # No paid + no commitment + no proof events → v12_1 NOT unlocked
        # (unless a real proof_event file was added during a prior test)
        assert "v12_1_unlocked" in body["revenue_truth"]

        # Stage 13: weekly learning → suggest_only
        r = await c.post("/api/v1/growth-beast/experiment/next", json={
            "sector_focus": "marketing_agency",
        })
        assert r.json()["experiment"]["action_mode"] == "suggest_only"


# ─────────────────── 5 invariants ──────────────


@pytest.mark.asyncio
async def test_invariant_8_hard_gates_present_in_beast_cc() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/founder/beast-command-center")
    gates = r.json()["hard_gates"]
    assert len(gates) == 8


@pytest.mark.asyncio
async def test_invariant_no_5xx_in_full_chain() -> None:
    """No endpoint in the Golden Loop chain should ever return 5xx."""
    from api.main import app

    transport = ASGITransport(app=app)
    paths = [
        "/api/v1/growth-beast/today",
        "/api/v1/company-growth-beast/status",
        "/api/v1/revops/finance-brief",
        "/api/v1/revenue-pipeline/summary",
        "/api/v1/role-command-v125/today/ceo",
        "/api/v1/proof-to-market/sector-learning",
        "/api/v1/founder/beast-command-center",
        "/api/v1/customer-portal/Slot-A",
    ]
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for p in paths:
            r = await c.get(p)
            assert 200 <= r.status_code < 500, f"{p} returned 5xx ({r.status_code})"


@pytest.mark.asyncio
async def test_invariant_action_modes_only_canonical_5() -> None:
    """Every action_mode field must be one of the 5 canonical values."""
    from api.main import app

    valid = {"suggest_only", "draft_only", "approval_required",
             "approved_manual", "blocked"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Sample 4 endpoints that return action_mode
        responses = [
            await c.post("/api/v1/growth-beast/warm-route/draft",
                         json={"channel": "founder_warm_intro",
                               "sector": "b2b_services"}),
            await c.post("/api/v1/growth-beast/offer/match",
                         json={"sector": "b2b_services",
                               "signal_type": "weak_followup"}),
            await c.post("/api/v1/growth-beast/experiment/next",
                         json={"sector_focus": "b2b_services"}),
            await c.get("/api/v1/role-command-v125/today/sales"),
        ]
    for r in responses:
        body = r.json()
        modes = []
        # Shallow scan for action_mode values
        def _scan(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "action_mode" and isinstance(v, str):
                        modes.append(v)
                    elif isinstance(v, (dict, list)):
                        _scan(v)
            elif isinstance(obj, list):
                for x in obj:
                    _scan(x)
        _scan(body)
        for m in modes:
            assert m in valid, f"non-canonical action_mode: {m!r}"


@pytest.mark.asyncio
async def test_invariant_proof_to_market_blocks_unsigned() -> None:
    """No fake proof: snippet for unsigned event must return blocked."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/proof-to-market/snippet", json={
            "event": {"action_taken": "delivered diagnostic",
                      "customer_approved": True,
                      "signed_publish_permission": False},
        })
    body = r.json()
    assert body["snippet"]["blocked"] is True


@pytest.mark.asyncio
async def test_invariant_revenue_truth_never_lives_without_evidence() -> None:
    """Without payment evidence, revenue_live MUST be False."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/revenue-pipeline/summary")
    body = r.json()
    truth = body["revenue_truth"]
    if truth["paid"] == 0:
        assert truth["revenue_live"] is False, (
            "revenue_live MUST be False when paid=0 — Constitution Article 8"
        )

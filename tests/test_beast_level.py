"""V12.5 Beast Level — combined tests for B2/B3/B4/B5 layers."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.growth_beast import (
    MarketSignal, compute_icp_score, draft_content, draft_warm_route,
    evaluate_signals, match_offer, next_experiment, proof_to_content_idea,
    rank_accounts, weekly_summary,
)
from auto_client_acquisition.company_growth_beast import (
    build_company_profile, build_growth_diagnostic, build_target_segments,
    build_offer_recommendation, build_content_pack, build_weekly_report,
    support_to_growth_insight,
)
from auto_client_acquisition.proof_to_market import (
    approval_gate_check, case_study_candidate, proof_to_snippet,
    sector_learning_summary, select_publishable_proofs,
)


# ─────────────── B2 Growth Beast ───────────────


def test_market_signal_accepts_public_source() -> None:
    s = MarketSignal(source_type="job_post", signal_type="hiring_sales_team",
                     signal_text_redacted="X hiring sales", confidence=0.8)
    assert s.public_only is True
    assert s.contains_personal_data is False


def test_evaluate_signals_empty() -> None:
    out = evaluate_signals([])
    assert out["total"] == 0
    assert out["action_mode"] == "suggest_only"


def test_evaluate_signals_aggregates() -> None:
    sigs = [
        MarketSignal(source_type="job_post", signal_type="hiring_sales_team",
                     signal_text_redacted="x", confidence=0.9),
        MarketSignal(source_type="press", signal_type="raised_funding",
                     signal_text_redacted="y", confidence=0.7),
        MarketSignal(source_type="job_post", signal_type="expanding_support",
                     signal_text_redacted="z", confidence=0.4),
    ]
    out = evaluate_signals(sigs)
    assert out["total"] == 3
    assert out["high_confidence_count"] == 2
    assert out["by_source"]["job_post"] == 2


def test_icp_score_zero_inputs_return_low() -> None:
    s = compute_icp_score()
    assert s.score == 0
    assert "غير مرشح" in s.reason_ar


def test_icp_score_high_inputs_return_high() -> None:
    s = compute_icp_score(
        pain_intensity=20, ability_to_pay=15, urgency=15,
        proof_potential=15, founder_access=15, referral_potential=10,
        sector_repeatability=10,
    )
    assert s.score == 100
    assert "ابدأ" in s.reason_ar


def test_rank_accounts_orders_by_score() -> None:
    a = compute_icp_score(pain_intensity=10)
    b = compute_icp_score(pain_intensity=20)
    ranked = rank_accounts([("X", a), ("Y", b)])
    assert ranked[0]["placeholder"] == "Y"


def test_offer_match_returns_499_pilot() -> None:
    offer = match_offer(sector="marketing_agency", signal_type="no_proof_visible")
    assert offer["price_sar"] == 499
    assert offer["price_halalah"] == 49900
    assert "guaranteed_revenue" in offer["blocked_claims"]


def test_offer_match_default_for_unknown() -> None:
    offer = match_offer(sector="unknown_sector", signal_type="unknown_problem")
    assert offer["price_sar"] == 499  # always pilot tier
    assert offer["approval_required"] is True


def test_content_engine_draft_only() -> None:
    out = draft_content(sector="marketing_agency", angle="proof_pack_visibility")
    assert out["action_mode"] == "draft_only"
    assert out["approval_required"] is True
    assert out["draft_ar"]
    assert out["draft_en"]


def test_warm_route_blocks_cold_channels() -> None:
    for ch in ("cold_whatsapp", "cold_email", "linkedin_dm_automation",
               "purchased_list_blast", "scrape_then_email"):
        out = draft_warm_route(channel=ch, sector="b2b_services")
        assert out["action_mode"] == "blocked"


def test_warm_route_allows_safe_channels() -> None:
    out = draft_warm_route(channel="founder_warm_intro", sector="b2b_services")
    assert out["action_mode"] == "draft_only"
    assert out["send_method"] == "manual_only"


def test_experiment_engine_baseline() -> None:
    exp = next_experiment()
    assert exp["safe_action"]
    assert exp["action_mode"] == "suggest_only"


def test_experiment_engine_low_reply_rate_pivots() -> None:
    exp = next_experiment(last_week_summary={"intros_sent": 10, "replies": 0})
    assert "rotate" in exp["safe_action"].lower() or "rotation" in exp["stop_condition"].lower()


def test_proof_to_content_blocks_without_approval() -> None:
    out = proof_to_content_idea(proof_event={
        "action_taken": "delivered diagnostic", "customer_approved": False,
    })
    assert out["blocked"] is True


def test_proof_to_content_with_approval() -> None:
    out = proof_to_content_idea(proof_event={
        "action_taken": "delivered diagnostic", "customer_approved": True,
    })
    assert out["blocked"] is False
    assert out["action_mode"] == "approval_required"


def test_weekly_summary_no_data() -> None:
    out = weekly_summary(signals={"total": 0})
    assert out["status"] == "no_data_yet"


def test_weekly_summary_low_reply_rate() -> None:
    out = weekly_summary(signals={"total": 5}, intros_sent=10, replies=1)
    assert out["status"] == "low_reply_rate"


def test_weekly_summary_first_revenue() -> None:
    out = weekly_summary(signals={}, intros_sent=10, replies=5,
                         diagnostics=3, pilots_offered=2, paid_pilots=1)
    assert out["status"] == "first_revenue"


# ─────────────── B3 Company Growth Beast ───────────────


def test_company_profile_creation() -> None:
    p = build_company_profile(company_handle="ClientCo-A", sector="marketing_agency",
                              biggest_problem="no_proof_visible",
                              consent_for_diagnostic=True)
    assert p.company_handle == "ClientCo-A"
    assert p.consent_for_diagnostic is True


def test_diagnostic_blocked_without_consent() -> None:
    p = build_company_profile(company_handle="X", consent_for_diagnostic=False)
    diag = build_growth_diagnostic(p)
    assert diag.get("blocked") is True


def test_diagnostic_with_consent_returns_seven_day_plan() -> None:
    p = build_company_profile(company_handle="X", sector="b2b_services",
                              biggest_problem="weak_followup",
                              consent_for_diagnostic=True)
    diag = build_growth_diagnostic(p)
    assert "seven_day_plan" in diag
    assert len(diag["seven_day_plan"]) >= 7
    assert diag["action_mode"] == "approval_required"


def test_target_segments_returns_top_3() -> None:
    p = build_company_profile(company_handle="X", sector="marketing_agency",
                              consent_for_diagnostic=True)
    segs = build_target_segments(p)
    assert len(segs) >= 1
    assert all("fit_score" in s for s in segs)


def test_offer_recommendation_uses_499() -> None:
    p = build_company_profile(company_handle="X", sector="marketing_agency",
                              biggest_problem="no_proof_visible",
                              consent_for_diagnostic=True)
    offer = build_offer_recommendation(p)
    assert offer["price_sar"] == 499


def test_content_pack_returns_5_items() -> None:
    p = build_company_profile(company_handle="X", sector="b2b_services",
                              consent_for_diagnostic=True)
    pack = build_content_pack(p)
    assert len(pack) == 5


def test_support_insight_no_data() -> None:
    out = support_to_growth_insight(ticket_categories={})
    assert out.get("insufficient_data") is True


def test_support_insight_with_data() -> None:
    out = support_to_growth_insight(ticket_categories={
        "billing": 12, "onboarding": 4, "technical": 7,
    })
    assert out.get("insufficient_data") is False
    assert out["top_repeated_question"] == "billing"


def test_weekly_report_insufficient_data() -> None:
    p = build_company_profile(company_handle="X", consent_for_diagnostic=True)
    rep = build_weekly_report(profile=p)
    assert rep["data_status"] == "insufficient_data"


def test_weekly_report_live_data() -> None:
    p = build_company_profile(company_handle="X", consent_for_diagnostic=True)
    rep = build_weekly_report(profile=p, diagnostics_done=2)
    assert rep["data_status"] == "live"


# ─────────────── B5 Proof-to-Market ───────────────


def test_select_publishable_filters_unsigned() -> None:
    events = [
        {"customer_approved": False, "signed_publish_permission": True},
        {"customer_approved": True, "signed_publish_permission": False},
        {"customer_approved": True, "signed_publish_permission": True,
         "audience": "internal_only"},
        {"customer_approved": True, "signed_publish_permission": True,
         "audience": "public_allowed"},
    ]
    pub = select_publishable_proofs(events)
    assert len(pub) == 1


def test_approval_gate_blocks_unsigned() -> None:
    d = approval_gate_check({"customer_approved": True,
                             "signed_publish_permission": False})
    assert d["allow"] is False


def test_approval_gate_allows_signed_public() -> None:
    d = approval_gate_check({"customer_approved": True,
                             "signed_publish_permission": True,
                             "audience": "public_allowed"})
    assert d["allow"] is True


def test_proof_to_snippet_blocks_internal_only() -> None:
    out = proof_to_snippet({"customer_approved": True,
                            "signed_publish_permission": True,
                            "audience": "internal_only"})
    assert out["blocked"] is True


def test_case_study_candidate_needs_3_signed() -> None:
    events = [
        {"customer_approved": True, "signed_publish_permission": True,
         "audience": "public_allowed", "action_taken": "x"},
    ]
    out = case_study_candidate(events, min_events=3)
    assert out["candidate"] is False


def test_sector_learning_no_events() -> None:
    out = sector_learning_summary([])
    assert out.get("insufficient_data") is True


def test_sector_learning_with_events() -> None:
    out = sector_learning_summary([
        {"sector_hint": "marketing_agency"},
        {"sector_hint": "marketing_agency"},
        {"sector_hint": "b2b_services"},
    ])
    assert out["top_sector"] == "marketing_agency"


# ─────────────── Routers (in-process) ───────────────


@pytest.mark.asyncio
async def test_growth_beast_status() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/growth-beast/status")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_growth_beast_today() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/growth-beast/today")
    assert r.status_code == 200
    body = r.json()
    assert "best_offer" in body
    assert "blocked_actions" in body
    assert "cold_whatsapp" in body["blocked_actions"]


@pytest.mark.asyncio
async def test_growth_beast_warm_route_blocks_cold() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/growth-beast/warm-route/draft",
                         json={"channel": "cold_whatsapp",
                               "sector": "b2b_services"})
    assert r.status_code == 200
    assert r.json()["route"]["action_mode"] == "blocked"


@pytest.mark.asyncio
async def test_company_growth_beast_status() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/company-growth-beast/status")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_company_growth_beast_diagnostic_blocked_without_consent() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/company-growth-beast/diagnostic",
                         json={"company_handle": "X",
                               "consent_for_diagnostic": False})
    body = r.json()
    assert body["diagnostic"].get("blocked") is True


@pytest.mark.asyncio
async def test_role_command_v125_status() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/role-command-v125/status")
    assert r.status_code == 200
    body = r.json()
    assert len(body["roles_supported"]) == 9


@pytest.mark.asyncio
async def test_role_command_v125_today_returns_role_payload() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for role in ("ceo", "growth", "sales", "support", "cs",
                     "delivery", "finance", "compliance", "ops"):
            r = await c.get(f"/api/v1/role-command-v125/today/{role}")
            assert r.status_code == 200, f"{role} failed"
            body = r.json()
            assert body["role"] == role
            assert len(body["top_3_decisions_ar"]) == 3


@pytest.mark.asyncio
async def test_role_command_v125_unknown_role_404() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/role-command-v125/today/random")
    assert r.status_code in (404, 422)


@pytest.mark.asyncio
async def test_proof_to_market_status() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/proof-to-market/status")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_proof_to_market_select() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/proof-to-market/select",
                         json={"events": [{"customer_approved": True,
                                           "signed_publish_permission": True,
                                           "audience": "public_allowed"}]})
    body = r.json()
    assert body["publishable_count"] == 1

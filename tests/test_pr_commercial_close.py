"""
PR-COMMERCIAL-CLOSE — comprehensive tests for the Saudi Revenue Command OS.

Coverage:
  Service Tower (contracts + excellence): 8 tests
  Proof Ledger + RWUs:                   12 tests
  Delivery state machine + SLA + QA:     10 tests
  Negotiation engine:                    10 tests
  Self-Growth Mode:                       8 tests
  Role briefs (sales/growth/CEO/RevOps/CS/agency/finance/compliance): 16 tests
  WhatsApp brief renderer + send-internal gate: 5 tests
  Call recommendation engine + dial-live gate:  6 tests
  Card priority ranker:                   4 tests
  New live-action gates:                  4 tests
  Frontend audit IN_SCOPE_FILES sanity:   1 test
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from auto_client_acquisition.business.commission_calculator import expected_monthly_commission
from auto_client_acquisition.negotiation_engine.close_plan import recommend, to_dict as plan_to_dict
from auto_client_acquisition.negotiation_engine.objection_classifier import classify, known_classes
from auto_client_acquisition.negotiation_engine.response_builder import build_response
from auto_client_acquisition.revenue_company_os.call_recommendation_engine import (
    ALLOWED_REASONS, BLOCKED_REASONS, can_dial_live, generate_script,
    recommend as call_recommend,
)
from auto_client_acquisition.revenue_company_os.card_priority_ranker import rank, score
from auto_client_acquisition.revenue_company_os.proof_ledger import record
from auto_client_acquisition.revenue_company_os.proof_pack_builder import build_pack
from auto_client_acquisition.revenue_company_os.revenue_work_units import (
    RWU_CATALOG, base_revenue_impact, is_valid_unit, known_unit_types, label_for, weight_for,
)
from auto_client_acquisition.revenue_company_os.role_brief_builder import SUPPORTED_ROLES, build
from auto_client_acquisition.revenue_company_os.self_growth_mode import (
    ALWAYS_FORBIDDEN_TODAY, build_daily_plan, build_weekly_learning, daily_plan_to_dict,
)
from auto_client_acquisition.revenue_company_os.whatsapp_brief_renderer import (
    can_send_internal_brief, render,
)
from auto_client_acquisition.service_delivery.qa_checklist import check_ready_to_deliver
from auto_client_acquisition.service_delivery.service_session import (
    DELIVERED_STATES, allowed_transitions,
)
from auto_client_acquisition.service_delivery.sla_tracker import status_for, summarize
from auto_client_acquisition.service_tower.contracts import (
    all_contracts, contract_to_dict, get_contract,
)
from auto_client_acquisition.service_tower.excellence_score import (
    all_excellence, compute_excellence,
)
from core.config.settings import get_settings
from db.models import (
    GrowthExperimentRecord, ObjectionEventRecord, PartnerRecord, ProofEventRecord,
    ServiceSessionRecord,
)
from scripts.forbidden_claims_audit import IN_SCOPE_FILES


# ── Service Tower ─────────────────────────────────────────────────


def test_service_tower_has_six_contracts():
    cs = all_contracts()
    assert len(cs) == 6
    ids = {c.service_id for c in cs}
    assert ids == {
        "free_diagnostic", "growth_starter", "data_to_revenue",
        "executive_growth_os", "partnership_growth", "full_growth_control_tower",
    }


def test_get_contract_returns_known():
    c = get_contract("growth_starter")
    assert c is not None
    assert c.pricing_sar == 499.0


def test_get_contract_returns_none_for_unknown():
    assert get_contract("nope") is None


def test_contract_to_dict_has_expected_keys():
    d = contract_to_dict(get_contract("growth_starter"))
    for k in ("service_id", "pricing_sar", "deliverables", "proof_metrics", "upgrade_path"):
        assert k in d


def test_excellence_all_services_sellable():
    """All 6 contracts must score >=80 (sellable gate)."""
    out = all_excellence()
    assert out["summary"]["total"] == 6
    assert out["summary"]["sellable"] == 6
    assert out["summary"]["internal_only"] == 0


def test_excellence_per_service_score_breakdown():
    out = compute_excellence(get_contract("growth_starter"))
    assert out["score"] >= 80
    assert out["gate"] == "sellable"
    rules = {r[0] for r in out["breakdown"]}
    assert "essentials" in rules
    assert "proof_metrics" in rules


def test_excellence_penalizes_forbidden_in_promise():
    """A custom contract with 'نضمن' in its promise must lose 20 points."""
    from auto_client_acquisition.service_tower.contracts import ServiceContract
    bad = ServiceContract(
        service_id="bad",
        arabic_name="bad",
        english_name="bad",
        bundle_tier="diagnostic",
        target_customer="anyone",
        pain="any",
        promise="نضمن لك زيادة 200% في المبيعات",
        forbidden_claims=("نضمن",),
        required_inputs=("a", "b"),
        workflow_steps=("a", "b", "c"),
        agents_used=("x",),
        human_approvals=("ok",),
        safe_tool_policy=("internal",),
        deliverables=("d1", "d2"),
        proof_metrics=("m1", "m2", "m3"),
        sla_hours=24,
        pricing_sar=0.0,
        pricing_label="مجاني",
        risks=("r1",),
        upgrade_path="growth_starter",
        frontend_page="x.html",
    )
    out = compute_excellence(bad)
    rule_names = {r[0] for r in out["breakdown"] if r[1] < 0}
    assert "forbidden_in_promise" in rule_names


def test_no_contract_has_guaranteed_in_promise():
    for c in all_contracts():
        assert "نضمن" not in c.promise, f"{c.service_id} promise contains forbidden claim"
        assert "guaranteed" not in c.promise.lower()


# ── Proof Ledger / RWUs ───────────────────────────────────────────


def test_rwu_catalog_has_required_units():
    types = set(known_unit_types())
    expected = {
        "opportunity_created", "target_ranked", "draft_created",
        "approval_collected", "meeting_drafted", "followup_created",
        "risk_blocked", "partner_suggested", "proof_generated", "payment_link_drafted",
    }
    assert expected.issubset(types)


def test_rwu_label_and_weight_lookup():
    assert label_for("opportunity_created") == "فرصة جديدة"
    assert weight_for("proof_generated") == 2.0
    assert base_revenue_impact("opportunity_created") == 500.0


def test_is_valid_unit_rejects_unknown():
    assert is_valid_unit("opportunity_created") is True
    assert is_valid_unit("not_a_unit") is False


def test_proof_pack_built_from_empty_events_gives_zero():
    out = build_pack([])
    assert out["totals"]["created_units"] == 0
    assert out["totals"]["estimated_revenue_impact_sar"] == 0.0
    assert "next_recommended_action_ar" in out


@pytest.mark.asyncio
async def test_proof_ledger_records_event(async_client):
    """Posts an event and reads it back through the customer pack endpoint."""
    cid = f"cust_{uuid.uuid4().hex[:8]}"
    r = await async_client.post("/api/v1/proof-ledger/events", json={
        "unit_type": "opportunity_created",
        "customer_id": cid,
    })
    assert r.status_code == 200
    pack = await async_client.get(f"/api/v1/proof-ledger/customer/{cid}/pack")
    assert pack.status_code == 200
    body = pack.json()
    assert body["event_count"] >= 1
    assert body["pack"]["totals"]["created_units"] >= 1


@pytest.mark.asyncio
async def test_proof_ledger_rejects_unknown_unit(async_client):
    r = await async_client.post("/api/v1/proof-ledger/events", json={
        "unit_type": "make_up_unit",
        "customer_id": "x",
    })
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_proof_ledger_batch(async_client):
    cid = f"cust_{uuid.uuid4().hex[:8]}"
    r = await async_client.post("/api/v1/proof-ledger/events/batch", json={
        "items": [
            {"unit_type": "opportunity_created", "customer_id": cid},
            {"unit_type": "draft_created", "customer_id": cid, "approval_required": True, "approved": False},
            {"unit_type": "risk_blocked", "customer_id": cid, "risk_level": "high"},
        ],
    })
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 3


@pytest.mark.asyncio
async def test_proof_ledger_units_endpoint(async_client):
    r = await async_client.get("/api/v1/proof-ledger/units")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == len(RWU_CATALOG)


@pytest.mark.asyncio
async def test_proof_pack_pending_approvals_counted(async_client):
    cid = f"cust_{uuid.uuid4().hex[:8]}"
    await async_client.post("/api/v1/proof-ledger/events", json={
        "unit_type": "draft_created", "customer_id": cid,
        "approval_required": True, "approved": False,
    })
    r = await async_client.get(f"/api/v1/proof-ledger/customer/{cid}/pack")
    assert r.json()["pack"]["totals"]["pending_approvals"] >= 1


def test_proof_pack_high_risk_blocked_counted():
    class FakeEvt:
        def __init__(self, unit_type, risk):
            self.unit_type = unit_type
            self.label_ar = label_for(unit_type)
            self.risk_level = risk
            self.approval_required = False
            self.approved = True
            self.revenue_impact_sar = 0
            self.occurred_at = datetime.now(timezone.utc)
    out = build_pack([FakeEvt("risk_blocked", "high"), FakeEvt("risk_blocked", "low")])
    assert out["totals"]["protected_units"] == 2
    assert out["totals"]["high_risk_blocked"] == 1


# ── Delivery state machine ───────────────────────────────────────


def test_allowed_transitions_new():
    nxt = allowed_transitions("new")
    assert "waiting_inputs" in nxt
    assert "in_progress" in nxt
    assert "delivered" not in nxt


def test_allowed_transitions_closed_is_terminal():
    assert allowed_transitions("closed") == []


def test_delivered_states_constant():
    assert "delivered" in DELIVERED_STATES
    assert "closed" in DELIVERED_STATES


@pytest.mark.asyncio
async def test_delivery_session_create_and_get(async_client):
    r = await async_client.post("/api/v1/delivery/sessions", json={
        "service_id": "growth_starter",
        "customer_id": f"cust_{uuid.uuid4().hex[:8]}",
        "inputs": {"company_name": "X"},
    })
    assert r.status_code == 200
    sid = r.json()["session_id"]
    g = await async_client.get(f"/api/v1/delivery/sessions/{sid}")
    assert g.status_code == 200
    assert g.json()["service_id"] == "growth_starter"


@pytest.mark.asyncio
async def test_delivery_session_unknown_service_400(async_client):
    r = await async_client.post("/api/v1/delivery/sessions", json={"service_id": "fake"})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_delivery_transition_legal(async_client):
    r = await async_client.post("/api/v1/delivery/sessions", json={"service_id": "growth_starter"})
    sid = r.json()["session_id"]
    t = await async_client.post(f"/api/v1/delivery/sessions/{sid}/transition", json={"to": "in_progress"})
    assert t.status_code == 200
    assert t.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_delivery_transition_illegal_400(async_client):
    r = await async_client.post("/api/v1/delivery/sessions", json={"service_id": "growth_starter"})
    sid = r.json()["session_id"]
    bad = await async_client.post(f"/api/v1/delivery/sessions/{sid}/transition", json={"to": "closed"})
    # 'new' → 'closed' IS allowed; pick a definitely illegal one:
    t = await async_client.post(f"/api/v1/delivery/sessions/{sid}/transition", json={"to": "delivered"})
    assert t.status_code == 400


def test_sla_tracker_marks_breach():
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    s = status_for(past)
    assert s.is_breached
    assert s.risk_level == "breach"


def test_sla_tracker_warning_window():
    near = datetime.now(timezone.utc) + timedelta(hours=2)
    s = status_for(near)
    assert not s.is_breached
    assert s.risk_level == "warning"


def test_sla_summarize_buckets():
    class FakeRow:
        def __init__(self, deadline):
            self.deadline_at = deadline
    rows = [FakeRow(datetime.now(timezone.utc) + timedelta(hours=10))]
    out = summarize(rows)
    assert out["ok"] == 1


def test_qa_checklist_flags_missing_inputs():
    class FakeSession:
        inputs_json = {}
        deliverables_json = []
        deadline_at = None
        started_at = None
    contract = get_contract("growth_starter")
    out = check_ready_to_deliver(FakeSession(), contract, [])
    assert not out.passed
    assert any("input:" in m for m in out.missing)


# ── Negotiation engine ───────────────────────────────────────────


@pytest.mark.parametrize("text,expected", [
    ("السعر مرتفع", "price"),
    ("ما عندي وقت الآن", "timing"),
    ("شركة جديدة، ما نعرفكم", "trust"),
    ("عندنا وكالة", "already_have_agency"),
    ("أحتاج رأي الفريق", "need_team_approval"),
    ("ليست أولوية الآن", "not_priority"),
    ("أرسل لي التفاصيل", "send_details"),
    ("هل تضمنون نتائج؟", "want_guarantee"),
])
def test_objection_classifier(text, expected):
    assert classify(text).objection_class == expected


def test_classifier_known_classes_count():
    assert len(known_classes()) == 8


def test_response_builder_proof_based():
    r = build_response("price")
    assert r is not None
    assert r.proof_based is True
    assert "نضمن" not in r.response_ar  # never use guarantee in response


@pytest.mark.asyncio
async def test_negotiation_classify_endpoint(async_client):
    r = await async_client.post("/api/v1/negotiation/classify", json={"text": "السعر غالي"})
    assert r.status_code == 200
    assert r.json()["objection_class"] == "price"


@pytest.mark.asyncio
async def test_negotiation_build_response_endpoint(async_client):
    r = await async_client.post("/api/v1/negotiation/build-response", json={
        "text": "السعر مرتفع", "has_list": False,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["objection_class"] == "price"
    assert body["close_plan"]["plan_id"] in ("offer_pilot_499", "offer_proof_review", "escalate_human")


def test_close_plan_for_guarantee_escalates():
    plan = recommend(objection_class="want_guarantee")
    assert plan.plan_id == "escalate_human"


def test_close_plan_for_has_list():
    plan = recommend(objection_class="price", has_list=True)
    assert plan.plan_id == "offer_data_to_revenue"


# ── Self-Growth Mode ─────────────────────────────────────────────


def test_daily_plan_includes_forbidden_today():
    p = daily_plan_to_dict(build_daily_plan())
    assert "cold_whatsapp" in p["forbidden_today"]
    assert "linkedin_auto_dm" in p["forbidden_today"]


def test_daily_plan_segment_rotates_deterministic():
    import datetime as _dt
    plan_a = build_daily_plan(_dt.date(2026, 5, 4))
    plan_b = build_daily_plan(_dt.date(2026, 5, 4))
    assert plan_a.focus_segment_id == plan_b.focus_segment_id


def test_daily_plan_channel_count_caps():
    p = daily_plan_to_dict(build_daily_plan())
    total = sum(int(c.get("count", 0)) for c in p["channel_plan"])
    assert total <= 50  # safety cap


def test_always_forbidden_today_constant():
    assert "cold_whatsapp" in ALWAYS_FORBIDDEN_TODAY
    assert "scrape_linkedin" in ALWAYS_FORBIDDEN_TODAY


def test_weekly_learning_with_no_events():
    out = build_weekly_learning([])
    assert out["no_unsafe_action_executed"] is True
    assert "bottleneck_ar" in out


@pytest.mark.asyncio
async def test_self_growth_today_endpoint(async_client):
    r = await async_client.get("/api/v1/self-growth/today")
    assert r.status_code == 200
    body = r.json()
    assert "focus_segment_ar" in body
    assert "cold_whatsapp" in body["forbidden_today"]


@pytest.mark.asyncio
async def test_self_growth_weekly_learning_endpoint(async_client):
    r = await async_client.get("/api/v1/self-growth/weekly-learning")
    assert r.status_code == 200
    assert r.json()["learning"]["no_unsafe_action_executed"] is True


@pytest.mark.asyncio
async def test_self_growth_experiment_create(async_client):
    r = await async_client.post("/api/v1/self-growth/experiments", json={
        "week_iso": "2026-W18",
        "hypothesis_ar": "اختبر افتتاحية Co-branded Proof Pack",
        "segment": "agencies_riyadh_b2b",
        "channel": "linkedin_manual",
    })
    assert r.status_code == 200
    assert r.json()["week_iso"] == "2026-W18"


# ── Role Briefs ──────────────────────────────────────────────────


def test_role_brief_builder_lists_supported_roles():
    assert "ceo" in SUPPORTED_ROLES
    assert "sales_manager" in SUPPORTED_ROLES
    assert "growth_manager" in SUPPORTED_ROLES
    assert "compliance" in SUPPORTED_ROLES
    # PR-VISION-CLOSE adds meeting_intelligence as the 9th role.
    assert len(SUPPORTED_ROLES) >= 8


def test_role_brief_builder_unknown_role_raises():
    with pytest.raises(ValueError, match="unknown_role"):
        build("ufo", data={})


def test_sales_brief_uses_top_3_max():
    out = build("sales_manager", data={"deals": [], "sessions": [], "objection_events": []})
    assert len(out["top_decisions"]) <= 3


def test_growth_brief_includes_blocked_today():
    out = build("growth_manager", data={"yesterday_events": []})
    assert "cold_whatsapp" in out["blocked_today_ar"]


def test_ceo_brief_arabic_blocked_lines():
    out = build("ceo", data={
        "sales_summary": {"deals_at_risk": 0, "pilot_offers_ready": 0},
        "growth_summary": {"focus_segment": "agencies"},
        "proof_summary": {"totals": {"pending_approvals": 0}},
        "partner_summary": {"hot_partners": 0},
    })
    assert any("cold WhatsApp" in line for line in out["blocked_today_ar"])


def test_revops_brief_picks_weakest_stage():
    out = build("revops", data={"funnel_event_counts": {"lead": 100, "mql": 1, "sql": 0, "pilot": 0, "paying": 0, "renewed": 0, "churned": 0}})
    # weakest stage from rate calc
    assert out["top_decisions"]
    assert "weakest" in out["top_decisions"][0]["title_ar"] or out["top_decisions"][0]["type"] == "funnel_focus"


def test_cs_brief_p0_first():
    class T:
        priority = "P0"; status = "open"; partner_id = None; customer_id = None
    out = build("customer_success", data={"customers": [], "tickets": [T()], "sessions": []})
    assert any(d["type"] == "support_p0" for d in out["top_decisions"])


def test_finance_brief_invoice_decision_when_session_ready():
    class S:
        service_id = "growth_starter"; status = "ready_to_deliver"; deadline_at = None
    out = build("finance", data={"sessions": [S()], "payments": [], "expected_partner_commission_sar": 0.0})
    assert any(d["type"] == "invoice_ready" for d in out["top_decisions"])


def test_compliance_brief_surfaces_gates():
    class FakeSettings:
        whatsapp_allow_live_send = False
        whatsapp_allow_internal_send = False
        whatsapp_allow_customer_send = False
        gmail_allow_live_send = False
        moyasar_allow_live_charge = False
        linkedin_allow_auto_dm = False
        resend_allow_live_send = False
        calls_allow_live_dial = False
    out = build("compliance", data={"proof_events": [], "settings": FakeSettings()})
    assert out["live_action_gates"]["MOYASAR_ALLOW_LIVE_CHARGE"] is False


def test_agency_brief_requires_partner():
    out = build("agency_partner", data={"partner": None, "customers": [], "sessions": [], "expected_commission_sar": 0.0})
    assert out["role"] == "agency_partner"


@pytest.mark.asyncio
async def test_role_briefs_endpoint_known(async_client):
    r = await async_client.get("/api/v1/role-briefs/daily?role=growth_manager")
    assert r.status_code == 200
    body = r.json()
    assert body["role"] == "growth_manager"
    assert len(body["top_decisions"]) <= 3


@pytest.mark.asyncio
async def test_role_briefs_endpoint_unknown_400(async_client):
    r = await async_client.get("/api/v1/role-briefs/daily?role=ufo")
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_role_briefs_agency_requires_partner_id(async_client):
    r = await async_client.get("/api/v1/role-briefs/daily?role=agency_partner")
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_role_briefs_compliance_includes_gates(async_client):
    r = await async_client.get("/api/v1/role-briefs/daily?role=compliance")
    assert r.status_code == 200
    gates = r.json()["live_action_gates"]
    assert gates["WHATSAPP_ALLOW_INTERNAL_SEND"] is False
    assert gates["CALLS_ALLOW_LIVE_DIAL"] is False


@pytest.mark.asyncio
async def test_roles_list_endpoint(async_client):
    r = await async_client.get("/api/v1/role-briefs/roles")
    assert r.status_code == 200
    assert "ceo" in r.json()["roles"]


# ── WhatsApp Brief Renderer ──────────────────────────────────────


def test_whatsapp_render_arabic_max_3_decisions():
    brief = {
        "role": "sales_manager",
        "summary": {"deals_at_risk": 5},
        "top_decisions": [
            {"title_ar": f"قرار {i}", "why_now_ar": "x", "recommended_action_ar": "y",
             "risk_level": "low", "buttons_ar": ["a", "b", "c", "d"]}
            for i in range(5)
        ],
        "blocked_today_ar": ["لا cold WhatsApp"],
    }
    text = render(brief)
    assert "صباح الخير" in text
    # Only 3 decisions rendered
    assert text.count("لماذا الآن:") <= 3


def test_whatsapp_render_rejects_unknown_role_gracefully():
    text = render({"role": "alien", "top_decisions": []})
    # Should still render with a fallback header
    assert "Dealix" in text or "ملخص" in text


def test_can_send_internal_brief_default_blocked():
    class S:
        whatsapp_allow_internal_send = False
        whatsapp_allow_live_send = False
    allowed, _ = can_send_internal_brief(S())
    assert allowed is False


def test_can_send_internal_brief_blocks_when_live_master_off():
    class S:
        whatsapp_allow_internal_send = True
        whatsapp_allow_live_send = False
    allowed, reason = can_send_internal_brief(S())
    assert allowed is False
    assert "LIVE_SEND" in reason or "live-send" in reason


@pytest.mark.asyncio
async def test_whatsapp_brief_endpoint_returns_text(async_client):
    r = await async_client.get("/api/v1/whatsapp/brief?role=sales_manager")
    assert r.status_code == 200
    assert "text" in r.json()
    assert r.json()["decision_count"] <= 3


@pytest.mark.asyncio
async def test_whatsapp_send_internal_blocked_default(async_client):
    r = await async_client.post("/api/v1/whatsapp/brief/send-internal", json={"role": "sales_manager"})
    assert r.status_code == 403


# ── Call Recommendation Engine ───────────────────────────────────


def test_allowed_reasons_constant():
    assert "price_question" in ALLOWED_REASONS
    assert "support_p0" in ALLOWED_REASONS


def test_blocked_reasons_constant():
    assert "no_permission" in BLOCKED_REASONS
    assert "cold_list" in BLOCKED_REASONS


def test_recommend_blocks_cold_list():
    r = call_recommend(reason="cold_list", has_user_permission=True)
    assert not r.allowed
    assert r.blocked_reason == "cold_list"


def test_recommend_blocks_without_permission():
    r = call_recommend(reason="price_question", has_user_permission=False)
    assert not r.allowed
    assert r.blocked_reason == "no_permission"


def test_recommend_allows_high_intent():
    r = call_recommend(reason="price_question", has_user_permission=True, customer_label="X")
    assert r.allowed
    assert r.duration_minutes > 0


def test_can_dial_live_default_blocked():
    class S:
        calls_allow_live_dial = False
        calls_allow_recommend = True
    allowed, _ = can_dial_live(S())
    assert allowed is False


@pytest.mark.asyncio
async def test_calls_recommend_endpoint(async_client):
    r = await async_client.post("/api/v1/calls/recommend", json={
        "reason": "pilot_accepted",
        "has_user_permission": True,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["allowed"] is True
    assert "call_id" in body


@pytest.mark.asyncio
async def test_calls_dial_live_always_403(async_client):
    r = await async_client.post("/api/v1/calls/dial-live")
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_calls_script_endpoint(async_client):
    r = await async_client.post("/api/v1/calls/test_call_id/script", json={
        "call_reason": "pilot_accepted",
        "customer": "شركة س",
    })
    assert r.status_code == 200
    assert "Pilot" in r.json()["script_ar"]


def test_generate_script_includes_anti_claim():
    script = generate_script(call_reason="price_question", customer="X")
    assert "لا نضمن" in script  # must explicitly disclaim guarantees


# ── Card Priority Ranker ─────────────────────────────────────────


def test_ranker_picks_high_risk_high_revenue_first():
    cards = [
        {"type": "executive_decision", "risk_level": "high", "recommended_action_ar": "x", "proof_impact": ["a"]},
        {"type": "channel_health",     "risk_level": "low",  "recommended_action_ar": "y", "proof_impact": ["b"]},
    ]
    ranked = rank(cards)
    assert ranked[0]["type"] == "executive_decision"


def test_ranker_drops_cards_without_action_or_proof():
    cards = [
        {"type": "executive_decision", "risk_level": "high"},  # no action / no proof
        {"type": "channel_health", "risk_level": "low", "recommended_action_ar": "y", "proof_impact": ["b"]},
    ]
    ranked = rank(cards)
    assert len(ranked) == 1
    assert ranked[0]["type"] == "channel_health"


def test_ranker_top_n_default_is_three():
    cards = [
        {"type": "executive_decision", "risk_level": r, "recommended_action_ar": "x", "proof_impact": ["a"]}
        for r in ["low", "medium", "high", "high", "high"]
    ]
    assert len(rank(cards)) == 3


def test_score_is_deterministic():
    card = {"type": "deal_followup", "risk_level": "high", "proof_impact": ["x"]}
    assert score(card) == score(card)


# ── New live-action gates ─────────────────────────────────────────


def test_whatsapp_internal_send_default_false():
    s = get_settings()
    assert s.whatsapp_allow_internal_send is False


def test_whatsapp_customer_send_default_false():
    s = get_settings()
    assert s.whatsapp_allow_customer_send is False


def test_calls_live_dial_default_false():
    s = get_settings()
    assert s.calls_allow_live_dial is False


def test_calls_recommend_default_true():
    """We DO recommend (read-only) — default True."""
    s = get_settings()
    assert s.calls_allow_recommend is True


# ── Frontend audit IN_SCOPE_FILES sanity ─────────────────────────


def test_audit_scope_includes_login_and_existing_pages():
    s = set(IN_SCOPE_FILES)
    must = {"login.html", "command-center.html", "trust-center.html", "agency-partner.html"}
    assert must.issubset(s)

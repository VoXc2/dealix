"""Tests for Dealix Revenue + Customer Ops Autopilot core."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator
from dealix.revenue_ops_autopilot.policies import stage_transition_allowed
from dealix.revenue_ops_autopilot.scoring import compute_lead_score, suggested_stage_from_score
from dealix.revenue_ops_autopilot.store import get_autopilot_store, reset_autopilot_store_for_tests
from dealix.revenue_ops_autopilot.war_room import (
    build_daily_summary,
    normalize_lead,
    outreach_transition_allowed,
    war_room_row,
)
from dealix.revenue_ops_autopilot.war_room_mapping import STAGE_TO_WAR_ROOM


@pytest.fixture(autouse=True)
def _isolated_autopilot_store() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        p = Path(fh.name)
    store = reset_autopilot_store_for_tests(path=p)
    yield
    store._path.unlink(missing_ok=True)


def test_lead_score_and_stage_tiers():
    hi = {
        "role": "founder",
        "company": "Tech Co",
        "industry": "services",
        "country": "Saudi Arabia",
        "pain": "we need clearer approval boundaries across revenue ops and CRM quality",
        "ai_usage": "planning AI agents soon",
        "budget_range": "10000 SAR",
        "urgency": "within 30 days",
    }
    score, _bd = compute_lead_score(hi)
    assert score >= 15
    stage = suggested_stage_from_score(score=score, is_partner_candidate=False)
    assert stage == "qualified_A"

    lo = {"role": "", "pain": "test", "company": ""}
    score2, _ = compute_lead_score(lo)
    assert suggested_stage_from_score(score=score2, is_partner_candidate=False) == "closed_lost"

    assert suggested_stage_from_score(score=9, is_partner_candidate=False) == "nurture"
    assert suggested_stage_from_score(score=10, is_partner_candidate=False) == "qualified_B"
    assert suggested_stage_from_score(score=5, is_partner_candidate=False) == "closed_lost"


def test_stage_guard_invoice_requires_payment_proof():
    ok, reason = stage_transition_allowed(
        "invoice_sent",
        "invoice_paid",
        has_payment_proof=False,
    )
    assert not ok
    assert reason == "needs_payment_proof"


def test_stage_guard_delivery_requires_payment():
    ok, reason = stage_transition_allowed(
        "invoice_sent",
        "delivery_started",
        has_payment_proof=False,
    )
    assert not ok
    assert reason in ("yaml_transition_not_allowed", "needs_invoice_paid_before_delivery")


def test_proof_pack_generator_has_sections():
    from dealix.revenue_ops_autopilot.proof_pack import (
        PROOF_PACK_SECTIONS,
        build_proof_pack_draft,
    )

    draft = build_proof_pack_draft(company="Acme", locale="ar")
    assert len(draft["sections"]) == len(PROOF_PACK_SECTIONS)
    assert draft["governance"]["no_fake_kpi"] is True


def test_public_capture_lead_api():
    from api.main import app

    cli = TestClient(app)
    res = cli.post(
        "/api/v1/public/leads",
        json={
            "name": "Layla Ops",
            "email": "layla.ops@example.com",
            "company": "Saudi Logistics",
            "country": "Saudi Arabia",
            "pain": "we use hubspot ai automation crm unclear sources",
            "ai_usage": "automation rollout",
            "budget_range": "15000 SAR",
            "role": "head of ops",
            "consent_proof_pack": True,
            "hold_stage": True,
        },
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["lead_id"].startswith("lea_")
    assert data["lead_score"] >= 1


@pytest.mark.parametrize(
    ("verb", "url", "body"),
    (
        ("GET", "/api/v1/public/services", None),
        ("GET", "/api/v1/public/proof-pack/sample", None),
        (
            "POST",
            "/api/v1/public/risk-score",
            {"role": "", "pain": "", "country": "", "notes": "", "company": ""},
        ),
    ),
)
def test_public_reads_and_riskscore(verb: str, url: str, body: dict[str, str] | None):
    from api.main import app

    cli = TestClient(app)
    if verb == "POST":
        r = cli.post(url, json=body or {})
        assert r.status_code == 200, r.text
    else:
        r = cli.get(url)
        assert r.status_code == 200


def test_public_partner_apply_requires_consent():
    from api.main import app

    cli = TestClient(app)
    r = cli.post(
        "/api/v1/public/partner-apply",
        json={
            "name": "Partner Co",
            "email": "p@example.com",
            "company": "CRM Shop",
            "partner_type": "referral",
            "consent": False,
        },
    )
    assert r.status_code == 422


def test_public_partner_apply_ok():
    from api.main import app

    cli = TestClient(app)
    r = cli.post(
        "/api/v1/public/partner-apply",
        json={
            "name": "Partner Co",
            "email": "partner@example.com",
            "company": "CRM Shop",
            "partner_type": "referral",
            "message": "we implement hubspot",
            "consent": True,
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["lead_id"].startswith("lea_")


def test_outreach_guard_sent_manual_requires_approval():
    ok, reason = outreach_transition_allowed("message_drafted", "sent_manual")
    assert not ok
    assert reason == "needs_approved_before_sent_manual"
    ok2, _ = outreach_transition_allowed("approved_to_send", "sent_manual")
    assert ok2


def test_normalize_lead_backfills_war_room_from_stage():
    from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord

    raw = FunnelLeadRecord(
        id="lea_test1",
        company="Agency X",
        stage="meeting_booked",
        pain="follow-up chaos",
    )
    n = normalize_lead(raw)
    assert n.war_room_status == STAGE_TO_WAR_ROOM["meeting_booked"]
    assert n.pain_hypothesis == "follow-up chaos"
    row = war_room_row(n)
    assert row["target"] == "Agency X"
    assert len(row) >= 7


def test_war_room_api_admin_flow(monkeypatch):
    import os

    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-war-room")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-admin-war-room"}

    orch = get_default_orchestrator()
    lead = orch.capture_lead(
        {
            "name": "Sara",
            "email": "sara@agency.sa",
            "company": "Riyadh Marketing Co",
            "pain": "leads lost after campaigns",
            "source": "war_room_test",
        },
    )

    r_list = cli.get("/api/v1/ops-autopilot/war-room", headers=headers)
    assert r_list.status_code == 200, r_list.text
    assert r_list.json()["count"] >= 1

    r_sum = cli.get("/api/v1/ops-autopilot/war-room/summary", headers=headers)
    assert r_sum.status_code == 200
    assert "today" in r_sum.json()

    r_patch = cli.patch(
        f"/api/v1/ops-autopilot/war-room/{lead.id}",
        headers=headers,
        json={
            "war_room_status": "message_drafted",
            "next_action": "Prepare agency DM draft",
            "next_action_due": "2026-05-18",
        },
    )
    assert r_patch.status_code == 200, r_patch.text

    r_patch2 = cli.patch(
        f"/api/v1/ops-autopilot/war-room/{lead.id}",
        headers=headers,
        json={"war_room_status": "approved_to_send"},
    )
    assert r_patch2.status_code == 200

    r_patch3 = cli.patch(
        f"/api/v1/ops-autopilot/war-room/{lead.id}",
        headers=headers,
        json={"war_room_status": "sent_manual"},
    )
    assert r_patch3.status_code == 200

    evs = get_autopilot_store().list_evidence(limit=20)
    types = {e.event_type for e in evs}
    assert "war_room_approved_to_send" in types
    assert "war_room_sent_manual" in types

    r_create = cli.post(
        "/api/v1/ops-autopilot/war-room",
        headers=headers,
        json={
            "name": "Omar",
            "company": "CRM Partners",
            "email": "omar@crmp.sa",
            "segment": "agency_partner",
            "pain_hypothesis": "proof for clients",
        },
    )
    assert r_create.status_code == 201, r_create.text


def test_build_daily_summary_counts():
    from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord

    leads = [
        FunnelLeadRecord(id="l1", company="A", war_room_status="replied", lead_score=20),
        FunnelLeadRecord(id="l2", company="B", war_room_status="meeting_booked", lead_score=15),
    ]
    s = build_daily_summary(leads)
    assert s["revenue"]["meetings"] >= 1


def test_outreach_templates_segment():
    from dealix.revenue_ops_autopilot.outreach_templates import build_outreach_draft

    text = build_outreach_draft(
        company="وكالة الرياض",
        contact="أحمد",
        segment="agency_wedge",
        pain="متابعة ضعيفة",
    )
    assert "وكالة" in text or "الرياض" in text
    assert "Risk Score" in text or "Proof" in text


def test_war_room_today_pack_and_import(monkeypatch):
    import os

    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-pack-import")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-pack-import"}

    r_pack = cli.get("/api/v1/ops-autopilot/war-room/today-pack", headers=headers)
    assert r_pack.status_code == 200, r_pack.text
    assert "targets" in r_pack.json() or "store_top_leads" in r_pack.json()

    r_imp = cli.post(
        "/api/v1/ops-autopilot/war-room/import-targets",
        headers=headers,
        json={"use_default_csv": True},
    )
    assert r_imp.status_code == 200, r_imp.text
    assert r_imp.json().get("imported", 0) >= 0


def test_founder_dashboard_sovereign_gtm_keys(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-sovereign-gtm")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-sovereign-gtm"}
    r = cli.get("/api/v1/ops-autopilot/founder-dashboard", headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    gtm = body.get("sovereign_gtm")
    assert isinstance(gtm, dict)
    assert "sovereign_gtm_path" in gtm
    assert "social_post_due_today" in gtm or gtm.get("social_post_due_today") is None
    assert "war_room_top_targets" in gtm
    assert "marketing_stats" in gtm
    assert "targeting_today_top5" in gtm
    assert "bridge_events_7d" in gtm
    cp = body.get("comprehensive_plan")
    assert isinstance(cp, dict)
    assert "weekly_one_decision" in cp
    assert "master_execution_phase" in cp
    assert cp["master_execution_phase"].get("active_phase") is not None


def test_founder_ceo_master_plan_endpoint(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-ceo-master-plan")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-ceo-master-plan"}
    r = cli.get("/api/v1/ops-autopilot/founder/ceo-master-plan", headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("overall_verdict") in ("PASS", "IN_PROGRESS")
    assert "p0_revenue_close" in body
    assert body.get("daily_five_metrics", {}).get("metrics")


def test_founder_comprehensive_plan_endpoint(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-comprehensive-plan")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-comprehensive-plan"}
    r = cli.get("/api/v1/ops-autopilot/founder/comprehensive-plan", headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("max_ops_backlog", {}).get("total", 0) >= 50


def test_founder_cockpit_run_unified_quick(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-unified-day")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-unified-day"}
    r = cli.post(
        "/api/v1/ops-autopilot/founder/cockpit/run-unified-day",
        headers=headers,
        json={"quick": True, "top_n": 5, "run_optional_scripts": False},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("unified_day_run", {}).get("verdict") in ("PASS", "DEGRADED")
    assert body.get("cockpit_verdict")


def test_marketing_social_today_and_mark(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-social")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-social"}

    r = cli.get("/api/v1/ops-autopilot/marketing/social-today", headers=headers)
    assert r.status_code == 200, r.text
    post = r.json().get("post")
    if post and post.get("week") is not None:
        w, d = int(post["week"]), int(post["day"])
        r2 = cli.post(
            "/api/v1/ops-autopilot/marketing/social-today/mark",
            headers=headers,
            json={"week": w, "day": d, "status": "approved"},
        )
        assert r2.status_code == 200, r2.text


def test_targeting_pool_and_p0(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-targeting")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-targeting"}
    r_pool = cli.get("/api/v1/ops-autopilot/targeting/pool", headers=headers)
    assert r_pool.status_code == 200, r_pool.text
    assert r_pool.json().get("total", 0) >= 0
    r_p0 = cli.get("/api/v1/ops-autopilot/targeting/p0-today", headers=headers)
    assert r_p0.status_code == 200, r_p0.text
    assert "items" in r_p0.json()


def test_meeting_brief_objection_hints(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-brief-obj")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-brief-obj"}
    orch = get_default_orchestrator()
    lead = orch.capture_lead(
        {
            "name": "Sara",
            "email": "sara@test.sa",
            "company": "CRM Agency",
            "pain": "عندنا CRM و هبسبوت",
            "hold_stage": True,
        },
    )
    r = cli.get(
        f"/api/v1/ops-autopilot/leads/{lead.id}/meeting-brief",
        headers=headers,
    )
    assert r.status_code == 200, r.text
    hints = r.json().get("objection_hints") or []
    assert isinstance(hints, list)
    assert len(hints) >= 1


def test_meeting_brief_endpoint(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-brief")
    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "test-brief"}
    orch = get_default_orchestrator()
    lead = orch.capture_lead(
        {"name": "Ali", "email": "ali@test.sa", "company": "Brief Co", "hold_stage": True},
    )
    r = cli.get(
        f"/api/v1/ops-autopilot/leads/{lead.id}/meeting-brief",
        headers=headers,
        params={"locale": "ar"},
    )
    assert r.status_code == 200, r.text
    assert "discovery_questions_ar" in r.json()


def test_kb_public_answer_handles_unknown_question():
    from api.main import app

    cli = TestClient(app)
    q = "zzzzzzzunknown topic about moon phase revenue"
    r = cli.get("/api/v1/public/knowledge/answer", params={"q": q})
    assert r.status_code == 200
    assert "risk_level" in r.json()


def test_config_loader_routing_thresholds():
    from dealix.revenue_ops_autopilot.config_loader import routing_thresholds

    th = routing_thresholds()
    assert th["qualified_a_min"] >= 10
    assert th["nurture_min"] >= 1


def test_calendly_webhook_handler():
    from dealix.revenue_ops_autopilot.webhook_handlers import handle_calendly_webhook

    r = handle_calendly_webhook(
        {
            "event": "invitee.created",
            "payload": {"email": "cal@test.sa", "name": "Cal Guest"},
        },
    )
    assert r.get("handled") is True
    assert r.get("lead_id")


def test_objection_draft_endpoint(monkeypatch):
    from api.main import app

    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-obj")
    cli = TestClient(app)
    r = cli.get(
        "/api/v1/ops-autopilot/marketing/objection-draft",
        headers={"X-Admin-API-Key": "test-obj"},
        params={"slug": "crm_exists"},
    )
    assert r.status_code == 200, r.text
    assert "response_draft_ar" in r.json()


def test_booking_request_includes_calendly(monkeypatch):
    from api.main import app

    monkeypatch.setenv("CALENDLY_URL", "https://calendly.com/test/demo")
    cli = TestClient(app)
    r = cli.post(
        "/api/v1/public/booking-request",
        json={"email": "book@test.sa", "preferred_channel": "email", "notes": "hi"},
    )
    assert r.status_code == 200, r.text
    assert r.json().get("calendly_url") == "https://calendly.com/test/demo"

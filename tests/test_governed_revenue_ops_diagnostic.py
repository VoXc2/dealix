from __future__ import annotations

import pytest

from auto_client_acquisition.governed_revenue_ops_diagnostic import (
    LeadCaptureInput,
    advance_state,
    build_invoice_draft,
    build_meeting_brief,
    build_scope_draft,
    capture_lead,
    daily_dashboard,
    reset_store_for_tests,
    score_lead,
)


def _a_grade_payload() -> LeadCaptureInput:
    return LeadCaptureInput(
        name="Sami",
        company="Acme B2B",
        role="Founder",
        email="sami@acme.sa",
        linkedin_url="https://linkedin.com/in/sami",
        industry="B2B SaaS",
        team_size="25",
        current_crm="HubSpot",
        ai_usage_today="AI follow-up drafts + automation tests",
        main_pain="CRM pipeline quality is weak and approvals are unclear.",
        urgency="within 30 days",
        budget_range="5000-10000 SAR",
        permission_to_contact=True,
        source="landing",
        region="Saudi Arabia",
    )


def setup_function() -> None:
    reset_store_for_tests()


def test_score_lead_returns_a_for_strong_icp() -> None:
    result = score_lead(_a_grade_payload())
    assert result.grade == "A"
    assert result.score_total >= 10
    assert result.recommended_state == "qualified_A"


def test_score_lead_returns_c_for_partner_profile() -> None:
    payload = LeadCaptureInput(
        name="Partner",
        company="",
        role="HubSpot consultant partner",
        email="partner@example.com",
        linkedin_url="",
        industry="Consulting",
        team_size="1",
        current_crm="",
        ai_usage_today="",
        main_pain="Exploring partner collaboration.",
        urgency="later",
        budget_range="",
        permission_to_contact=True,
        source="linkedin",
        region="Saudi Arabia",
    )
    result = score_lead(payload)
    assert result.grade == "C"
    assert result.recommended_state == "nurture"


def test_capture_lead_requires_permission_to_contact() -> None:
    payload = _a_grade_payload().model_copy(update={"permission_to_contact": False})
    with pytest.raises(ValueError, match="permission_to_contact"):
        capture_lead(payload)


def test_state_machine_enforces_scope_before_invoice_and_happy_path() -> None:
    rec = capture_lead(_a_grade_payload())
    assert rec.state == "qualified_A"
    assert any(item.action_type == "send_booking_link_draft" for item in rec.approval_queue)

    rec = advance_state(funnel_id=rec.funnel_id, target_state="meeting_booked")
    build_meeting_brief(funnel_id=rec.funnel_id)
    rec = advance_state(funnel_id=rec.funnel_id, target_state="meeting_done")
    rec = advance_state(funnel_id=rec.funnel_id, target_state="scope_requested")

    with pytest.raises(ValueError, match="scope_sent"):
        build_invoice_draft(funnel_id=rec.funnel_id, tier="starter")

    scope = build_scope_draft(funnel_id=rec.funnel_id, tier="starter")
    assert scope["amount_sar"] == 4999
    rec = advance_state(funnel_id=rec.funnel_id, target_state="scope_sent")

    invoice = build_invoice_draft(funnel_id=rec.funnel_id, tier="starter")
    assert invoice["amount_sar"] == 4999
    rec = advance_state(funnel_id=rec.funnel_id, target_state="invoice_sent")
    rec = advance_state(funnel_id=rec.funnel_id, target_state="invoice_paid")
    rec = advance_state(funnel_id=rec.funnel_id, target_state="delivery_started")
    rec = advance_state(funnel_id=rec.funnel_id, target_state="proof_pack_sent")
    rec = advance_state(funnel_id=rec.funnel_id, target_state="upsell_sprint")
    assert rec.state == "upsell_sprint"


def test_daily_dashboard_exposes_ops_kpis() -> None:
    capture_lead(_a_grade_payload())
    board = daily_dashboard()
    assert board["kpis"]["qualified_A"] >= 1
    assert board["guardrails"]["all_external_actions_approval_required"] is True

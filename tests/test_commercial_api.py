"""Commercial API contract tests for the current one-product first-launch path."""

from __future__ import annotations

import os

from fastapi.testclient import TestClient

os.environ.setdefault("APP_ENV", "test")

from api.main import app

client = TestClient(app)


START_GATE_REFS = {
    "approved_duration_days": 20,
    "approved_duration_ref": "duration://acme/20d-v1",
    "approved_scope_ref": "scope://acme/v1",
    "baseline_source_ref": "proof://baseline/acme",
    "approved_data_boundary_ref": "data-boundary://minimum-data/acme",
    "approval_path_ref": "approval://acme/pilot",
    "acceptance_criteria_ref": "acceptance://acme/v1",
    "customer_specific_quote_ref": "quote://acme/approved-v1",
    "customer_acceptance_ref": "acceptance-evidence://acme/v1",
    "start_condition_ref": "start-condition://acme/v1",
}


def test_commercial_status() -> None:
    response = client.get("/api/v1/commercial/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready_for_governed_internal_commercial_ops"
    assert data["wedge"] == "Revenue + Proof + Command"
    assert data["quote_only_after_discovery"] is True
    assert data["public_fixed_price"] is False
    assert data["live_charge"] is False
    assert data["automatic_upsell"] is False
    assert data["external_send"] is False
    assert data["components"]["pilot_delivery"] == "customer_specific_duration_start_gated"
    assert data["components"]["payment_link"] == "blocked_no_live_charge"


def test_warm_intro_requires_real_context_reference() -> None:
    response = client.post(
        "/api/v1/commercial/warm-intro/generate",
        json={
            "name": "محمد",
            "company": "شركة تجريبية",
            "role": "CEO",
            "sector": "b2b_services",
            "known_pain": "عمليات يدوية",
            "relationship": "warm_intro",
            "referrer_name": "شريك معروف",
        },
    )
    assert response.status_code == 422


def test_warm_intro_drafts_only_no_send_authority() -> None:
    response = client.post(
        "/api/v1/commercial/warm-intro/generate",
        json={
            "name": "محمد",
            "company": "شركة تجريبية",
            "role": "CEO",
            "sector": "b2b_services",
            "known_pain": "عمليات يدوية",
            "relationship": "warm_intro",
            "referrer_name": "شريك معروف",
            "warm_context_ref": "relationship://founder-intro/001",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "draft_only"
    assert data["external_send_allowed"] is False
    assert data["next_action"] == "founder_review_only"
    assert data["warm_context_ref"] == "relationship://founder-intro/001"


def test_warm_intro_templates_do_not_imply_consent() -> None:
    response = client.get("/api/v1/commercial/warm-intro/templates")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "internal_reference_only"
    assert data["external_send_allowed"] is False
    assert "consent" in data["message"].lower()


def test_pilot_start_fails_without_current_start_gate_refs() -> None:
    response = client.post(
        "/api/v1/commercial/pilot/start",
        json={
            "account_id": "acc_test",
            "company_name": "شركة اختبار",
            "sector": "b2b_services",
            "pain_points": ["عمليات يدوية"],
        },
    )
    assert response.status_code == 422


def test_pilot_start_is_customer_specific_governed_plan() -> None:
    response = client.post(
        "/api/v1/commercial/pilot/start",
        json={
            "account_id": "acc_test",
            "company_name": "شركة اختبار",
            "sector": "b2b_services",
            "pain_points": ["عمليات يدوية"],
            "start_date": "2026-08-16",
            **START_GATE_REFS,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "plan_prepared_approval_required"
    assert data["external_send_allowed"] is False
    assert data["live_charge_allowed"] is False
    plan = data["plan"]
    assert plan["launch_authority"] == "customer_specific_governed_pilot"
    assert plan["start_date"] == "2026-08-16"
    assert plan["end_date"] == "2026-09-04"
    assert plan["approved_duration_days"] == 20
    assert plan["approved_duration_ref"] == "duration://acme/20d-v1"
    assert plan["duration_authority"] == "customer_specific_approved_duration_only"
    assert plan["legacy_fixed_duration_authority"] is False
    assert plan["legacy_aliases_authoritative"] is False
    assert "revenue_command_pilot_30d" in plan["legacy_launch_authority_aliases"]
    assert plan["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert plan["external_send_allowed"] is False
    assert plan["live_charge_allowed"] is False
    assert [row["day"] for row in plan["day_plans"]] == [1, 4, 7, 11, 14, 17, 20]
    assert all(row["draft_messages_ar"] == [] for row in plan["day_plans"])
    blob = str(plan)
    assert "499" not in blob
    assert "2,999" not in blob
    assert "4,999" not in blob
    assert "STOP" in plan["upsell_script"]
    assert "EXPAND" in plan["upsell_script"]
    assert "REDESIGN" in plan["upsell_script"]


def test_pilot_duration_is_not_defaulted_to_30_days() -> None:
    payload = {
        "account_id": "acc_duration",
        "company_name": "Duration Co",
        "sector": "b2b_services",
        "pain_points": [],
        "start_date": "2026-08-16",
        **START_GATE_REFS,
    }
    payload["approved_duration_days"] = 45
    payload["approved_duration_ref"] = "duration://duration-co/45d-v1"
    response = client.post("/api/v1/commercial/pilot/start", json=payload)
    assert response.status_code == 200
    plan = response.json()["plan"]
    assert plan["end_date"] == "2026-09-29"
    assert plan["day_plans"][-1]["day"] == 45
    assert plan["day_plans"][-1]["day"] != 30


def test_pilot_duration_reference_is_required() -> None:
    payload = {
        "account_id": "acc_duration_missing_ref",
        "company_name": "Duration Missing Ref Co",
        "start_date": "2026-08-16",
        **START_GATE_REFS,
    }
    payload.pop("approved_duration_ref")
    response = client.post("/api/v1/commercial/pilot/start", json=payload)
    assert response.status_code == 422


def test_pilot_weekly_template_requires_started_plan() -> None:
    response = client.get("/api/v1/commercial/pilot/week1-template")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "template_only"
    assert data["launch_authority"] == "customer_specific_governed_pilot"
    assert data["external_send_allowed"] is False


def test_upsell_path_is_manual_review_without_offer_or_price() -> None:
    response = client.get(
        "/api/v1/commercial/upsell/check",
        params={
            "account_id": "acc_test",
            "events_count": 100,
            "proof_pack_generated": True,
            "days_active": 90,
            "nps_score": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "manual_review_required"
    assert data["eligible_for_automatic_expansion"] is False
    assert data["offer"] is None
    assert data["price_sar"] is None
    assert data["next_step"] == "STOP_OR_EXPAND_OR_REDESIGN_FROM_SOURCE_BACKED_PROOF"


def test_payment_link_is_hard_blocked_by_current_launch_authority() -> None:
    response = client.post(
        "/api/v1/commercial/payment/link",
        json={
            "account_id": "acc_test",
            "customer_email": "test@example.com",
            "tier": "pilot",
            "price_sar": 499,
        },
    )
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["code"] == "NO_LIVE_CHARGE"


def test_payment_tiers_are_retired_from_public_first_launch() -> None:
    response = client.get("/api/v1/commercial/payment/tiers")
    assert response.status_code == 200
    data = response.json()
    assert data["tiers"] == []
    assert data["product_count"] == 1
    assert data["public_fixed_price"] is False
    assert data["quote_only"] is True
    assert data["live_checkout"] is False
    assert data["live_charge"] is False
    assert data["price_authority"] == "founder_approved_named_customer_quote"


def test_roi_estimate_is_not_customer_value_or_guarantee() -> None:
    response = client.post(
        "/api/v1/commercial/roi/estimate",
        json={
            "company_name": "Internal estimate test",
            "manual_hours_per_week": 20,
            "hourly_cost_sar": 60,
            "lost_leads_per_month": 5,
            "avg_deal_value_sar": 10_000,
            "recovered_conversion_pct": 10,
            "setup_cost_sar": 0,
            "monthly_cost_sar": 0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "internal_estimate_only"
    assert data["customer_value_claim"] is False
    assert data["guarantee"] is False
    assert "result" in data


def test_revenue_run_is_dry_run_only() -> None:
    response = client.post(
        "/api/v1/commercial/revenue/run",
        json={"trigger": "pytest", "dry_run": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["dry_run"] is True
    assert "results" in data
    assert data["commercial_authority"]["external_send_allowed"] is False
    assert data["commercial_authority"]["live_charge_allowed"] is False
    assert data["commercial_authority"]["public_fixed_price"] is False


def test_daily_brief_has_no_synthetic_outreach_or_payment_ready_claim() -> None:
    response = client.get("/api/v1/commercial/daily-brief")
    assert response.status_code == 200
    data = response.json()
    assert data["warm_intro_status"] == "draft_only_requires_real_warm_context_ref"
    assert data["payment"]["status"] == "blocked_no_live_charge"
    assert data["payment"]["tiers"] == []
    assert data["expansion"]["automatic_upsell"] is False
    assert "NO_LIVE_SEND" in data["reminders"]
    assert "NO_LIVE_CHARGE" in data["reminders"]
    assert "messages" not in data


def test_transformation_modules_are_internal_post_proof_planning_only() -> None:
    response = client.get("/api/v1/commercial/transformation/modules")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "internal_post_proof_planning_only"
    assert data["safe_to_send"] is False
    assert data["commercial_quote_authority"] is False
    assert "registry" in data


def test_transformation_proposal_requires_pilot_proof_and_scope_refs() -> None:
    response = client.post(
        "/api/v1/commercial/transformation/proposal",
        json={
            "customer_id": "acme",
            "selected_modules": ["company_brain"],
        },
    )
    assert response.status_code == 422

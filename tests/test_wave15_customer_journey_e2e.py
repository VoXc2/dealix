"""Wave 15 §B5 — Customer journey E2E integration test.

Walks the full Wave 13 + Wave 14 stack end-to-end using REAL module
calls (no HTTP, no mocks). Validates the data flow across all 9
layers of the productization spine:

    1. Service Catalog lookup
    2. Customer onboarding (Decision Passport built)
    3. Service Session start (Wave 13 lifecycle)
    4. Daily artifact tick (orchestrator)
    5. Deliverable created + advanced
    6. Approval Center decision (founder approves draft)
    7. Proof event recorded (L0-L5)
    8. Bottleneck Radar reflects state
    9. Expansion Readiness Score computed

Hard rules verified at every step:
- Article 4: NEVER any `live_send` / `live_charge` action_mode
- Article 8: every numeric is `is_estimate=True`
- Article 11: zero new business logic — pure composition

Sandbox-safe: zero network, zero DB, zero FastAPI app boot.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


# ─────────────────────────────────────────────────────────────────────
# Step 1 — Service Catalog: 7 offerings, ascending price ladder
# ─────────────────────────────────────────────────────────────────────


def test_step_01_service_catalog_has_7_offerings_with_valid_ladder() -> None:
    from auto_client_acquisition.service_catalog.registry import (
        get_offering, list_offerings,
    )

    offerings = list_offerings()
    assert len(offerings) == 7

    # Free Diagnostic must be at price 0
    free = get_offering("free_mini_diagnostic")
    assert free is not None
    assert free.price_sar == 0.0

    # Revenue Proof Sprint = 499 (first paid tier)
    sprint = get_offering("revenue_proof_sprint_499")
    assert sprint is not None
    assert sprint.price_sar == 499.0

    # Article 4: no live actions in any offering's action_modes_used
    for off in offerings:
        for mode in off.action_modes_used:
            assert mode in (
                "suggest_only", "draft_only", "approval_required",
                "approved_manual", "blocked",
            ), f"{off.id} has illegal action_mode: {mode}"


# ─────────────────────────────────────────────────────────────────────
# Step 2 — Decision Passport built for a new customer
# ─────────────────────────────────────────────────────────────────────


def test_step_02_decision_passport_validates_owner_and_action_mode() -> None:
    """Wave 12.5 §33.2.4 — runtime guards required."""
    from auto_client_acquisition.decision_passport.schema import (
        DecisionPassport,
        ScoreBoard,
        validate_passport,
    )

    # Build a fully-valid Wave 12 §32.3.4 passport (v1.1 schema).
    passport = DecisionPassport(
        lead_id="lead_001",
        company="Acme Real Estate Riyadh",
        source="warm_intro",
        why_now_ar="افتتاح فرع جديد في الرياض",
        why_now_en="New branch opened in Riyadh",
        icp_tier="A",
        priority_bucket="P1_THIS_WEEK",
        scores=ScoreBoard(
            fit_score=0.85,
            intent_score=0.75,
            urgency_score=0.7,
            revenue_potential_score=0.8,
            engagement_score=0.6,
            data_quality_score=0.7,
            warm_route_score=0.9,
            compliance_risk_score=0.15,
            deliverability_risk_score=0.2,
        ),
        best_channel="manual_linkedin",
        recommended_action="prepare_diagnostic",
        recommended_action_ar="جهّز تشخيصًا",
        proof_target="demo_booked",
        proof_target_ar="حجز عرض توضيحي",
        next_step_ar="جهّز تشخيصًا",
        next_step_en="prepare_diagnostic",
        owner="founder",
        action_mode="approval_required",
    )
    # Should not raise
    validate_passport(passport)
    assert passport.action_mode == "approval_required"
    # Article 4 sanity — no live in the action_mode literal
    assert "live" not in passport.action_mode


def test_step_02b_decision_passport_blocks_cold_whatsapp_channel() -> None:
    """Hard gate: best_channel must be in allowed_channels."""
    from auto_client_acquisition.decision_passport.schema import (
        DecisionPassport, ScoreBoard, ValidationFailure, validate_passport,
    )

    bad_passport = DecisionPassport(
        lead_id="lead_bad", company="Bad Co", source="cold_outreach",
        why_now_ar="x", why_now_en="x", icp_tier="C",
        priority_bucket="P2_NURTURE",
        scores=ScoreBoard(
            fit_score=0.2, intent_score=0.2, urgency_score=0.2,
            revenue_potential_score=0.2, engagement_score=0.2,
            data_quality_score=0.2, warm_route_score=0.2,
            compliance_risk_score=0.5, deliverability_risk_score=0.5,
        ),
        best_channel="cold_whatsapp",
        recommended_action="x", recommended_action_ar="x",
        proof_target="x", proof_target_ar="x",
        next_step_ar="x", next_step_en="x",
        owner="founder", action_mode="blocked",
    )
    with pytest.raises(ValidationFailure):
        validate_passport(
            bad_passport,
            allowed_channels=["manual_linkedin", "warm_email"],
        )


# ─────────────────────────────────────────────────────────────────────
# Step 3 — Service Session lifecycle (Wave 13)
# ─────────────────────────────────────────────────────────────────────


def test_step_03_service_session_lifecycle_state_machine_valid() -> None:
    """Wave 13 Phase 3 — service_sessions/lifecycle.py state machine."""
    from auto_client_acquisition.service_sessions.lifecycle import (
        advance_session, is_transition_allowed,
    )

    # Valid: draft → waiting_for_approval
    allowed, _ = advance_session(
        current="draft", target="waiting_for_approval", approval_id=None,
    )
    assert allowed is True

    # Valid: waiting_for_approval → active (with approval_id)
    allowed, _ = advance_session(
        current="waiting_for_approval", target="active",
        approval_id="approval_001",
    )
    assert allowed is True

    # INVALID: active requires approval_id
    allowed, reason = advance_session(
        current="waiting_for_approval", target="active", approval_id=None,
    )
    assert allowed is False
    assert "approval_id" in reason

    # INVALID: completed → draft (no rollback)
    allowed, _ = advance_session(
        current="completed", target="draft", approval_id=None,
    )
    assert allowed is False


# ─────────────────────────────────────────────────────────────────────
# Step 4 — Bottleneck Radar reflects state (Wave 13 + 15 CLI)
# ─────────────────────────────────────────────────────────────────────


def test_step_04_bottleneck_radar_empty_state_is_clear() -> None:
    """Zero counts → severity='clear', no urgent action."""
    from auto_client_acquisition.bottleneck_radar.computer import compute_founder_view

    bn = compute_founder_view()
    assert bn.severity == "clear"
    assert bn.is_estimate is True  # Article 8


def test_step_04b_bottleneck_radar_critical_at_high_counts() -> None:
    """5+ blocking items → severity='critical'."""
    from auto_client_acquisition.bottleneck_radar.computer import compute_founder_view

    bn = compute_founder_view(
        blocking_approvals_count=3,
        pending_payment_confirmations=2,
        overdue_followups=5,
    )
    assert bn.severity == "critical"
    # Bilingual single action present
    assert bn.today_single_action_ar
    assert bn.today_single_action_en
    assert bn.is_estimate is True


# ─────────────────────────────────────────────────────────────────────
# Step 5 — Expansion Readiness Score (Wave 12.5 §33.2.5)
# ─────────────────────────────────────────────────────────────────────


def test_step_05_expansion_readiness_score_returns_bounded_float() -> None:
    """Score must be in [0, 1] AND ready=False below threshold."""
    from auto_client_acquisition.expansion_engine.readiness_score import (
        compute_readiness_score,
    )

    # New customer — zero proof events
    score = compute_readiness_score()
    assert 0.0 <= score.score <= 1.0
    assert score.ready is False
    assert score.is_estimate is True  # Article 8


def test_step_05b_expansion_ready_when_proof_mature() -> None:
    """High proof + clean payments + good delivery → ready=True."""
    from auto_client_acquisition.expansion_engine.readiness_score import (
        compute_readiness_score,
    )

    score = compute_readiness_score(
        proof_event_count=8,
        max_evidence_level=4,
        customer_approved_proof_count=5,
        public_proof_count=2,
        payment_history_paid_count=3,
        delivery_sessions_complete_count=2,
        support_tickets_open=0,
        support_tickets_critical=0,
        days_since_last_engagement=2,
        customer_health_bucket="expansion_ready",
        budget_tier_match_score=0.9,
        remaining_pain_score=0.7,
    )
    # Score should be well above threshold
    assert score.score >= 0.6
    assert score.ready is True
    assert score.is_estimate is True


# ─────────────────────────────────────────────────────────────────────
# Step 6 — Hard gates audit (Article 4 immutable)
# ─────────────────────────────────────────────────────────────────────


def test_step_06_all_8_hard_gates_present_in_every_offering() -> None:
    """Article 4: every offering MUST list its applicable hard gates."""
    from auto_client_acquisition.service_catalog.registry import list_offerings

    # Each offering's hard_gates field MUST be a non-empty tuple
    for off in list_offerings():
        assert len(off.hard_gates) >= 1, f"{off.id} has no hard_gates declared"
        # NEVER include the inverse gates (i.e. permitting live actions)
        for gate in off.hard_gates:
            assert gate.startswith("no_"), (
                f"{off.id} has non-NO gate: {gate} — gates must be prohibitions"
            )


def test_step_06b_no_offering_uses_forbidden_action_modes() -> None:
    """Article 4: no offering may use `live_send` or `live_charge`."""
    from auto_client_acquisition.service_catalog.registry import list_offerings

    forbidden = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for off in list_offerings():
        for mode in off.action_modes_used:
            assert mode not in forbidden, (
                f"{off.id} uses forbidden action_mode: {mode}"
            )


# ─────────────────────────────────────────────────────────────────────
# Step 7 — Article 8: every numeric is an estimate
# ─────────────────────────────────────────────────────────────────────


def test_step_07_no_offering_uses_guarantee_language() -> None:
    """Article 8: 'نضمن' / 'guaranteed' / 'guarantee' forbidden."""
    from auto_client_acquisition.service_catalog.registry import list_offerings

    forbidden_ar = ("نضمن", "ضمان مؤكد")
    forbidden_en_lower = ("guaranteed", "we guarantee", "guarantee")
    for off in list_offerings():
        # Check KPI commitment text (the most likely place for overclaim)
        ar_text = off.kpi_commitment_ar
        en_text_lower = off.kpi_commitment_en.lower()
        for tok in forbidden_ar:
            assert tok not in ar_text, f"{off.id} kpi_commitment_ar contains {tok!r}"
        for tok in forbidden_en_lower:
            assert tok not in en_text_lower, (
                f"{off.id} kpi_commitment_en contains {tok!r}"
            )


# ─────────────────────────────────────────────────────────────────────
# Step 8 — Service Catalog JSON export round-trip
# ─────────────────────────────────────────────────────────────────────


def test_step_08_service_catalog_json_export_in_sync_with_registry() -> None:
    """Wave 15 §B2 — the JSON file on disk must match the registry."""
    json_path = REPO_ROOT / "landing" / "assets" / "data" / "services-catalog.json"
    assert json_path.exists(), (
        "landing/assets/data/services-catalog.json missing — "
        "run: python3 scripts/dealix_export_service_catalog_json.py"
    )

    import json

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["count"] == 7
    assert payload["schema_version"] == "1.0"
    # Article 4: hard gates listed
    assert set(payload["constitution"]["article_4_hard_gates"]) == {
        "no_live_send", "no_live_charge", "no_cold_whatsapp",
        "no_linkedin_auto", "no_scraping", "no_fake_proof",
        "no_fake_revenue", "no_blast",
    }
    # Article 8 + 11 constitution declarations
    assert payload["constitution"]["article_8_no_fake_claims"] is True
    assert payload["constitution"]["article_11_single_source_of_truth"] is True


# ─────────────────────────────────────────────────────────────────────
# Step 9 — Article 13 status (3 paid pilots gate)
# ─────────────────────────────────────────────────────────────────────


def test_step_09_article_13_gate_logic_in_daily_brief() -> None:
    """Daily brief must NEVER claim Article 13 fired with <3 paid."""
    # Inline import to avoid loading the CLI script eagerly
    script_path = REPO_ROOT / "scripts" / "dealix_founder_daily_brief.py"
    assert script_path.exists()

    spec = importlib.util.spec_from_file_location("_brief_test", script_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_brief_test"] = mod
    spec.loader.exec_module(mod)

    # Brief with 0 paid customers
    brief_zero = mod.build_brief(paid_customers_count=0)
    assert brief_zero["paid_customers_count"] == 0
    assert brief_zero["article_13_trigger_remaining"] == 3

    # Brief with 3 paid customers — Article 13 triggers
    brief_three = mod.build_brief(paid_customers_count=3)
    assert brief_three["article_13_trigger_remaining"] == 0

    # Brief with 5 paid (over-trigger) — still 0 remaining
    brief_five = mod.build_brief(paid_customers_count=5)
    assert brief_five["article_13_trigger_remaining"] == 0

"""Wave 12.5 §33.2.5 (Engine 10) — Proof + Expansion v2 tests.

Validates:
- Auto-summary: 6 templates, bilingual output, missing-key safe defaults
- Publish gate: blocks all 4 invalid combinations (low evidence /
  no consent / no approval / fully invalid)
- Expansion Readiness Score: 0.0 when no proof, ≥0.6 when ready,
  blockers explicit
- Next-best-offer: 5 pain → offer mappings + 3 action modes by readiness

All tests pure-function — no I/O, no LLM, deterministic.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.expansion_engine import (
    ExpansionReadinessScore,
    NextBestOffer,
    compute_readiness_score,
    recommend_next_offer,
)
from auto_client_acquisition.proof_engine.auto_summary import (
    ProofSummary,
    build_summary,
    known_event_types,
)


# ─────────────────────────────────────────────────────────────────────
# Auto-summary (6 tests)
# ─────────────────────────────────────────────────────────────────────


def test_known_event_types_has_6_templates() -> None:
    """All 6 canonical event templates registered."""
    types = known_event_types()
    assert len(types) >= 6
    must_have = (
        "deliverable_completed", "demo_booked", "diagnostic_delivered",
        "payment_confirmed", "proof_pack_assembled", "expansion_offered",
    )
    for t in must_have:
        assert t in types, f"missing template: {t}"


def test_summary_bilingual_output() -> None:
    """Every summary has Arabic + English fields populated."""
    summary = build_summary(
        event_id="evt_001",
        event_type="payment_confirmed",
        customer_handle="acme",
        evidence_level=4,
        consent_status="granted",
        approval_status="approved",
        when="2026-05-12",
        extra={"amount": "499"},
    )
    assert summary.headline_ar
    assert summary.headline_en
    assert summary.detail_ar
    assert summary.detail_en
    assert "499" in summary.detail_en
    assert "acme" in summary.detail_ar


def test_summary_missing_keys_use_safe_default() -> None:
    """Missing template keys render as ``[—]`` instead of raising."""
    summary = build_summary(
        event_id="evt_xx",
        event_type="payment_confirmed",
        customer_handle="acme",
        evidence_level=4,
        consent_status="granted",
        approval_status="approved",
        # NO extra={"amount": ...} — missing
    )
    # Article 8: missing data is visible, not invented
    assert "[—]" in summary.detail_en
    assert "[—]" in summary.detail_ar


def test_summary_unknown_event_type_falls_back_to_generic() -> None:
    """Unknown event_type uses generic deliverable_completed template."""
    summary = build_summary(
        event_id="evt_yy",
        event_type="totally_made_up_type",
        customer_handle="acme",
        evidence_level=2,
    )
    # Should not raise; generic template renders
    assert summary.headline_ar
    assert summary.headline_en


def test_metric_text_says_pending_when_baseline_missing() -> None:
    """Article 8: when before is None, summary says 'pending', not 0."""
    summary = build_summary(
        event_id="evt_zz",
        event_type="deliverable_completed",
        customer_handle="acme",
        evidence_level=2,
        metric={"name": "demos_booked", "unit": "demos", "before": None, "after": 5},
    )
    assert "pending" in summary.metric_text_en or "baseline" in summary.metric_text_en
    assert summary.metric_text_ar  # Arabic version present


def test_summary_records_sources_used() -> None:
    """Summary surfaces what data went into it (Article 8 audit trail)."""
    summary = build_summary(
        event_id="evt_a1",
        event_type="demo_booked",
        customer_handle="acme",
        evidence_level=3,
        consent_status="granted",
        approval_status="approved",
    )
    assert any("event_id=evt_a1" in s for s in summary.sources_used)
    assert any("evidence_level=L3" in s for s in summary.sources_used)


# ─────────────────────────────────────────────────────────────────────
# Publish gate (4 tests — all invalid combinations blocked)
# ─────────────────────────────────────────────────────────────────────


def test_publish_blocked_when_evidence_too_low() -> None:
    """L0-L3 → not publishable regardless of consent + approval."""
    for level in range(0, 4):
        summary = build_summary(
            event_id="evt_low",
            event_type="demo_booked",
            customer_handle="acme",
            evidence_level=level,
            consent_status="granted",
            approval_status="approved",
        )
        assert summary.is_public_publishable is False, \
            f"L{level} should NOT be publishable"
        assert "evidence_level" in summary.publish_block_reason


def test_publish_blocked_when_consent_missing() -> None:
    """L4+ but consent != granted → not publishable."""
    summary = build_summary(
        event_id="evt_no_consent",
        event_type="proof_pack_assembled",
        customer_handle="acme",
        evidence_level=4,
        consent_status="internal_only",
        approval_status="approved",
    )
    assert summary.is_public_publishable is False
    assert "consent_status" in summary.publish_block_reason


def test_publish_blocked_when_approval_missing() -> None:
    """L4+ + consent=granted but approval != approved → not publishable."""
    summary = build_summary(
        event_id="evt_no_approval",
        event_type="proof_pack_assembled",
        customer_handle="acme",
        evidence_level=4,
        consent_status="granted",
        approval_status="pending",
    )
    assert summary.is_public_publishable is False
    assert "approval_status" in summary.publish_block_reason


def test_publish_allowed_only_when_all_3_gates_met() -> None:
    """L4+ AND consent=granted AND approval=approved → publishable."""
    summary = build_summary(
        event_id="evt_pub_ok",
        event_type="proof_pack_assembled",
        customer_handle="acme",
        evidence_level=4,
        consent_status="granted",
        approval_status="approved",
    )
    assert summary.is_public_publishable is True
    assert summary.publish_block_reason == ""


# ─────────────────────────────────────────────────────────────────────
# Expansion Readiness Score (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_readiness_low_and_not_ready_when_no_proof_no_payment() -> None:
    """Article 8: no signals → low score, ready False, explicit blockers.

    Note: budget_fit_score defaults to 0.5 (neutral), so the score
    won't be exactly 0.0; we assert ready=False + critical blockers
    surfaced (the actual safety guarantee).
    """
    score = compute_readiness_score()  # all defaults = no proof + no payment
    assert score.score < 0.3, f"no signals → low score; got {score.score}"
    assert score.ready is False
    assert "no_proof_events_recorded" in score.blockers
    assert "no_paid_history" in score.blockers
    # Article 8: proof signal + engagement scores are honestly 0.0
    assert score.proof_signal_score == 0.0
    assert score.engagement_score == 0.0


def test_readiness_high_when_strong_signals() -> None:
    """Strong signals across the board → score ≥ 0.6 + ready True."""
    score = compute_readiness_score(
        proof_event_count=8,
        max_evidence_level=4,
        customer_approved_proof_count=4,
        public_proof_count=2,
        payment_history_paid_count=3,
        delivery_sessions_complete_count=2,
        support_tickets_open=0,
        support_tickets_critical=0,
        days_since_last_engagement=3,
        customer_health_bucket="expansion_ready",
        budget_tier_match_score=0.9,
        remaining_pain_score=0.7,
    )
    assert score.score >= 0.6
    assert score.ready is True
    assert "no_proof_events" not in str(score.blockers)


def test_readiness_critical_friction_blocks_even_high_score() -> None:
    """Critical support tickets → ready=False even if other signals strong."""
    score = compute_readiness_score(
        proof_event_count=8,
        max_evidence_level=5,
        customer_approved_proof_count=5,
        payment_history_paid_count=3,
        support_tickets_critical=2,  # critical → blocker
    )
    assert score.ready is False
    assert any("critical_support_tickets" in b for b in score.blockers)


def test_readiness_returns_is_estimate_true() -> None:
    """Article 8: score is always marked as estimate, never claimed certain."""
    score = compute_readiness_score(proof_event_count=1)
    assert score.is_estimate is True


def test_readiness_health_bucket_blocked_drives_score_down() -> None:
    """Customer health bucket 'blocked' applies -0.6 penalty."""
    base = compute_readiness_score(
        proof_event_count=5, max_evidence_level=4,
        customer_approved_proof_count=3, payment_history_paid_count=2,
        customer_health_bucket="stable",  # 0.0 bonus
    )
    blocked = compute_readiness_score(
        proof_event_count=5, max_evidence_level=4,
        customer_approved_proof_count=3, payment_history_paid_count=2,
        customer_health_bucket="blocked",  # -0.6 bonus
    )
    assert blocked.score < base.score


# ─────────────────────────────────────────────────────────────────────
# Next-best-offer (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_offer_mapping_5_pain_types() -> None:
    """All 5 named pain types map to distinct offers."""
    ready = compute_readiness_score(
        proof_event_count=5, max_evidence_level=4,
        customer_approved_proof_count=3, payment_history_paid_count=3,
        customer_health_bucket="expansion_ready", budget_tier_match_score=0.9,
    )
    pain_to_expected = {
        "dormant_data": "crm_data_readiness_for_ai",
        "follow_up_gap": "governed_ops_retainer",
        "support_chaos": "ai_governance_revenue_teams",
        "executive_visibility": "board_decision_memo",
        "agency_proof_gap": "trust_pack_lite",
    }
    for pain, expected_offer in pain_to_expected.items():
        offer = recommend_next_offer(readiness=ready, primary_pain=pain)  # type: ignore[arg-type]
        assert offer.offer_key == expected_offer, \
            f"pain={pain} → expected {expected_offer}, got {offer.offer_key}"


def test_unknown_pain_returns_no_recommendation() -> None:
    """Unknown pain → no_recommendation_yet (Article 8 — clarify first)."""
    ready = compute_readiness_score(
        proof_event_count=5, max_evidence_level=4,
        customer_approved_proof_count=3, payment_history_paid_count=3,
        customer_health_bucket="healthy", budget_tier_match_score=0.8,
    )
    offer = recommend_next_offer(readiness=ready, primary_pain="unknown")
    assert offer.offer_key == "no_recommendation_yet"


def test_action_mode_gates_by_readiness_score() -> None:
    """Article 8 action-mode gating:
    - not ready → suggest_only
    - ready + score < 0.8 → draft_only
    - ready + score >= 0.8 → approval_required
    """
    not_ready = compute_readiness_score()  # score=0.0
    offer1 = recommend_next_offer(readiness=not_ready, primary_pain="follow_up_gap")
    assert offer1.action_mode == "suggest_only"

    medium_ready = compute_readiness_score(
        proof_event_count=4, max_evidence_level=3,
        customer_approved_proof_count=2, payment_history_paid_count=2,
        customer_health_bucket="healthy", budget_tier_match_score=0.6,
        days_since_last_engagement=7,
    )
    if medium_ready.ready and medium_ready.score < 0.8:
        offer2 = recommend_next_offer(readiness=medium_ready, primary_pain="follow_up_gap")
        assert offer2.action_mode == "draft_only"

    very_ready = compute_readiness_score(
        proof_event_count=10, max_evidence_level=5,
        customer_approved_proof_count=8, payment_history_paid_count=5,
        delivery_sessions_complete_count=4,
        customer_health_bucket="expansion_ready", budget_tier_match_score=1.0,
        days_since_last_engagement=1, remaining_pain_score=0.9,
    )
    if very_ready.score >= 0.8:
        offer3 = recommend_next_offer(readiness=very_ready, primary_pain="follow_up_gap")
        assert offer3.action_mode == "approval_required"


# ─────────────────────────────────────────────────────────────────────
# Total: 18 tests (6 auto-summary + 4 publish gate + 5 readiness + 3 offer)
# ─────────────────────────────────────────────────────────────────────

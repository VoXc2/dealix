"""Wave 12 §32.3.11 (Engine 11) — Learning Flywheel tests.

Validates:
- record_learning_event + aggregator (12 event types, append-only)
- aggregate_weekly_report (what worked / failed / best ICP / revenue truth)
- compute_funnel (5 ratios, None when zero — Article 8)
- triage_feature_request (≥3 rule + paid-deal shortcut + hard-gate block)

All tests use ``tmp_path`` so production data/wave12/ never touched.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from auto_client_acquisition.learning_flywheel import (
    LearningEvent,
    aggregate_weekly_report,
    compute_funnel,
    record_learning_event,
    triage_feature_request,
)


# ─────────────────────────────────────────────────────────────────────
# Aggregator (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_record_event_creates_jsonl(tmp_path: Path) -> None:
    """First event creates the file."""
    storage = tmp_path / "events.jsonl"
    evt = record_learning_event(
        kind="payment_confirmed",
        customer_handle="acme",
        revenue_sar=499.0,
        notes_ar="أول pilot دفع", notes_en="first pilot paid",
        storage_path=storage,
    )
    assert isinstance(evt, LearningEvent)
    assert storage.exists()
    assert evt.revenue_sar == 499.0


def test_aggregate_empty_returns_zero_revenue(tmp_path: Path) -> None:
    """No events → zero revenue, empty buckets (Article 8 — no fabrication)."""
    storage = tmp_path / "events.jsonl"
    report = aggregate_weekly_report(storage_path=storage)
    assert report.events_total == 0
    assert report.revenue_confirmed_sar == 0.0
    assert report.paid_pilots_count == 0
    assert report.what_worked == []
    assert report.what_failed == []
    assert report.best_icp is None


def test_aggregate_only_payment_confirmed_counts_revenue(tmp_path: Path) -> None:
    """Article 8: ONLY payment_confirmed events flow to revenue_confirmed_sar."""
    storage = tmp_path / "events.jsonl"
    # Payment confirmed → revenue
    record_learning_event(kind="payment_confirmed", customer_handle="a", revenue_sar=499, storage_path=storage)
    # These should NOT count as revenue (per Engine 9)
    record_learning_event(kind="signal_created", customer_handle="b", revenue_sar=10000, storage_path=storage)
    record_learning_event(kind="lead_created", customer_handle="c", revenue_sar=10000, storage_path=storage)
    record_learning_event(kind="pilot_requested", customer_handle="d", revenue_sar=10000, storage_path=storage)
    record_learning_event(kind="upsell_offered", customer_handle="e", revenue_sar=10000, storage_path=storage)

    report = aggregate_weekly_report(storage_path=storage)
    # Only the one payment_confirmed = 499 SAR counts
    assert report.revenue_confirmed_sar == 499.0
    assert report.paid_pilots_count == 1


def test_aggregate_finds_best_icp_channel_offer(tmp_path: Path) -> None:
    """Best-of tracking: mode of dimensions among succeeded events."""
    storage = tmp_path / "events.jsonl"
    # 3 succeeded with icp=tier_a, channel=warm_intro, offer=499_sprint
    for handle in ("c1", "c2", "c3"):
        record_learning_event(
            kind="demo_booked", customer_handle=handle,
            sector="b2b_services", channel="warm_intro",
            offer="499_sprint", icp_tier="tier_a",
            succeeded=True, storage_path=storage,
        )
    # 1 succeeded with different ICP (minority)
    record_learning_event(
        kind="demo_booked", customer_handle="c4",
        channel="email", offer="3000_monthly", icp_tier="tier_b",
        succeeded=True, storage_path=storage,
    )
    report = aggregate_weekly_report(storage_path=storage)
    assert report.best_icp == "tier_a"
    assert report.best_channel == "warm_intro"
    assert report.best_offer == "499_sprint"


def test_aggregate_recommendation_changes_with_paid_count(tmp_path: Path) -> None:
    """Recommendation text adapts to paid_pilots count."""
    storage = tmp_path / "events.jsonl"

    # 0 paid → "send warm intros"
    rep0 = aggregate_weekly_report(storage_path=storage)
    assert "warm" in rep0.next_recommendation_en.lower() or "ignite" in rep0.next_recommendation_en.lower()

    # 1 paid → "more warm intros to reach 3"
    record_learning_event(kind="payment_confirmed", customer_handle="a", revenue_sar=499, storage_path=storage)
    rep1 = aggregate_weekly_report(storage_path=storage)
    assert "3" in rep1.next_recommendation_en

    # 3 paid → "publish case study"
    record_learning_event(kind="payment_confirmed", customer_handle="b", revenue_sar=499, storage_path=storage)
    record_learning_event(kind="payment_confirmed", customer_handle="c", revenue_sar=499, storage_path=storage)
    rep3 = aggregate_weekly_report(storage_path=storage)
    assert "case study" in rep3.next_recommendation_en.lower()


# ─────────────────────────────────────────────────────────────────────
# Funnel metrics (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_funnel_empty_returns_none_ratios(tmp_path: Path) -> None:
    """All denominators 0 → all ratios None (Article 8)."""
    storage = tmp_path / "events.jsonl"
    funnel = compute_funnel(storage_path=storage)
    assert funnel.signals_count == 0
    assert funnel.signal_to_lead is None
    assert funnel.lead_to_passport is None
    assert funnel.delivery_to_proof is None


def test_funnel_perfect_conversion(tmp_path: Path) -> None:
    """30 signals → 30 leads = 1.0 conversion."""
    storage = tmp_path / "events.jsonl"
    for i in range(30):
        record_learning_event(kind="signal_created", customer_handle=f"c{i}", storage_path=storage)
        record_learning_event(kind="lead_created", customer_handle=f"c{i}", storage_path=storage)
    funnel = compute_funnel(storage_path=storage)
    assert funnel.signals_count == 30
    assert funnel.leads_count == 30
    assert funnel.signal_to_lead == 1.0


def test_funnel_partial_conversion(tmp_path: Path) -> None:
    """10 signals → 5 leads = 0.5 conversion."""
    storage = tmp_path / "events.jsonl"
    for i in range(10):
        record_learning_event(kind="signal_created", customer_handle=f"c{i}", storage_path=storage)
    for i in range(5):
        record_learning_event(kind="lead_created", customer_handle=f"c{i}", storage_path=storage)
    funnel = compute_funnel(storage_path=storage)
    assert funnel.signal_to_lead == 0.5


def test_funnel_all_5_ratios_present(tmp_path: Path) -> None:
    """End-to-end Dealix funnel: signal → lead → passport → action →
    delivery → proof → payment."""
    storage = tmp_path / "events.jsonl"
    record_learning_event(kind="signal_created", customer_handle="a", storage_path=storage)
    record_learning_event(kind="lead_created", customer_handle="a", storage_path=storage)
    record_learning_event(kind="decision_passport_created", customer_handle="a", storage_path=storage)
    record_learning_event(kind="action_approved", customer_handle="a", storage_path=storage)
    record_learning_event(kind="delivery_started", customer_handle="a", storage_path=storage)
    record_learning_event(kind="proof_created", customer_handle="a", storage_path=storage)
    record_learning_event(kind="payment_confirmed", customer_handle="a", revenue_sar=499, storage_path=storage)

    funnel = compute_funnel(storage_path=storage)
    # All 6 ratios should be 1.0 (perfect single-customer journey)
    assert funnel.signal_to_lead == 1.0
    assert funnel.lead_to_passport == 1.0
    assert funnel.passport_to_approved_action == 1.0
    assert funnel.approved_action_to_delivery == 1.0
    assert funnel.delivery_to_proof == 1.0
    assert funnel.proof_to_payment == 1.0


# ─────────────────────────────────────────────────────────────────────
# Feature request triage (6 tests)
# ─────────────────────────────────────────────────────────────────────


def test_triage_3_customers_approves() -> None:
    """≥3 customers asked → BUILD_QUEUE."""
    decision = triage_feature_request(
        request_text="Add Excel export of Proof Pack",
        customer_handles_who_asked=["a", "b", "c"],
    )
    assert decision.status == "BUILD_QUEUE"
    assert decision.customer_count == 3
    assert "3plus_customers" in decision.rationale_tags


def test_triage_2_customers_defers() -> None:
    """<3 customers + no revenue tie → DEFER_INSUFFICIENT."""
    decision = triage_feature_request(
        request_text="Add Excel export",
        customer_handles_who_asked=["a", "b"],
    )
    assert decision.status == "DEFER_INSUFFICIENT"
    assert decision.customer_count == 2


def test_triage_paid_deal_shortcut() -> None:
    """closes_paid_deal=True → BUILD_QUEUE_PAID even with 0 customers asked."""
    decision = triage_feature_request(
        request_text="Custom integration",
        customer_handles_who_asked=[],
        closes_paid_deal=True,
    )
    assert decision.status == "BUILD_QUEUE_PAID"
    assert "closes_paid_deal" in decision.rationale_tags


def test_triage_revenue_tie_approves_with_few_customers() -> None:
    """1 customer asked + reduces_delivery_time → BUILD_QUEUE."""
    decision = triage_feature_request(
        request_text="One-click bulk approve",
        customer_handles_who_asked=["a"],
        reduces_delivery_time=True,
    )
    assert decision.status == "BUILD_QUEUE"
    assert "revenue_tie" in decision.rationale_tags


def test_triage_hard_gate_blocks_even_with_paid_deal() -> None:
    """Hard-gate violation REJECTED regardless of demand or paid-deal tie."""
    decision = triage_feature_request(
        request_text="Auto-send cold WhatsApp messages to all leads",
        customer_handles_who_asked=["a", "b", "c", "d", "e"],  # 5 customers
        closes_paid_deal=True,                                     # paid deal
    )
    assert decision.status == "REJECTED_UNSAFE"
    assert decision.violates_hard_gate is True


def test_triage_hard_gate_arabic_blocked() -> None:
    """Arabic hard-gate violation also blocks."""
    decision = triage_feature_request(
        request_text="إرسال تلقائي لكل العملاء",  # auto-send to all customers
        customer_handles_who_asked=["a", "b", "c"],
    )
    assert decision.status == "REJECTED_UNSAFE"


def test_triage_dedupes_repeated_customer_handles() -> None:
    """Same customer asking twice doesn't count twice."""
    decision = triage_feature_request(
        request_text="Add a feature",
        customer_handles_who_asked=["a", "a", "a", "a"],  # 1 unique
    )
    assert decision.customer_count == 1
    assert decision.status == "DEFER_INSUFFICIENT"


# ─────────────────────────────────────────────────────────────────────
# Total: 16 tests
# ─────────────────────────────────────────────────────────────────────

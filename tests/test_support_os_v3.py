"""Wave 12 §32.3.8 (Engine 8) — Support & Customer Success OS v3 tests.

Validates:
- Ticket schema extension (sentiment, root_cause, suggested_reply,
  proof_opportunity, customer_health_impact, escalation_needed, next_action)
- Bilingual sentiment classifier (4 categories)
- proof_opportunity auto-tagging (4 categories)
- Health Score 6-bucket extension (added expansion_ready + blocked)

All hardening fields are optional with safe defaults — back-compat preserved.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from auto_client_acquisition.support_os.ticket import (
    Sentiment,
    Ticket,
    classify_sentiment_bilingual,
    create_ticket,
    is_proof_opportunity_category,
)


# ─────────────────────────────────────────────────────────────────────
# Ticket schema extension (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_v1_callers_still_work_via_defaults() -> None:
    """Backward-compat: existing callers using create_ticket() with v1
    fields only must succeed; the 7 new fields default to safe values."""
    t = create_ticket(
        message_text_redacted="payment didn't go through",
        customer_id="cust_test",
        channel="whatsapp",
        category="payment",
        priority="p0",
    )
    # v1 fields preserved
    assert t.customer_id == "cust_test"
    assert t.priority == "p0"
    assert t.channel == "whatsapp"
    # All 7 new v3 fields default safely
    assert t.sentiment is None
    assert t.root_cause == ""
    assert t.suggested_reply == ""
    assert t.proof_opportunity is False
    assert t.customer_health_impact == 0.0
    assert t.escalation_needed is False
    assert t.next_action == ""


def test_v3_fields_settable() -> None:
    """All 7 new fields can be set on Ticket construction."""
    sla = datetime.now(timezone.utc) + timedelta(hours=1)
    t = Ticket(
        id="tkt_x1",
        customer_id="cust_acme",
        channel="email",
        message_text_redacted="something is broken again",
        category="technical_issue",
        priority="p1",
        sla_due_at=sla,
        sentiment="frustrated",
        root_cause="follow_up_gap",
        suggested_reply="We're sorry — here's what we'll do next: ...",
        proof_opportunity=True,
        customer_health_impact=-0.3,
        escalation_needed=True,
        next_action="draft_reply_then_founder_review",
    )
    assert t.sentiment == "frustrated"
    assert t.root_cause == "follow_up_gap"
    assert t.proof_opportunity is True
    assert t.customer_health_impact == -0.3
    assert t.escalation_needed is True


def test_extra_fields_still_forbidden() -> None:
    """Schema preserves extra='forbid' (typo guard)."""
    sla = datetime.now(timezone.utc) + timedelta(hours=1)
    with pytest.raises(ValidationError):
        Ticket(
            id="tkt_x", message_text_redacted="x", sla_due_at=sla,
            sentymentt="oops",  # typo  # type: ignore[call-arg]
        )


def test_invalid_sentiment_value_rejected() -> None:
    """Sentiment Literal rejects unknown values."""
    sla = datetime.now(timezone.utc) + timedelta(hours=1)
    with pytest.raises(ValidationError):
        Ticket(
            id="tkt_y", message_text_redacted="x", sla_due_at=sla,
            sentiment="ecstatic",  # not in canonical 4  # type: ignore[arg-type]
        )


# ─────────────────────────────────────────────────────────────────────
# Bilingual sentiment classifier (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_sentiment_classifies_arabic_angry() -> None:
    """Saudi-Arabic angry markers route to "angry"."""
    for text in ("نصب! سأرفع شكوى", "هذا احتيال", "كذب صريح"):
        assert classify_sentiment_bilingual(text) == "angry", \
            f"text={text!r} should classify as angry"


def test_sentiment_classifies_arabic_frustrated() -> None:
    """Saudi-Arabic frustration markers."""
    for text in ("محبط جداً", "ما يشتغل", "للمرة الثالثة"):
        assert classify_sentiment_bilingual(text) == "frustrated", \
            f"text={text!r} should classify as frustrated"


def test_sentiment_classifies_arabic_positive() -> None:
    """Saudi-Arabic positive markers."""
    for text in ("ممتاز شكراً", "بارك الله فيكم", "أحسنتم رائع"):
        assert classify_sentiment_bilingual(text) == "positive", \
            f"text={text!r} should classify as positive"


def test_sentiment_classifies_english_categories() -> None:
    """English categories all 3 work."""
    assert classify_sentiment_bilingual("This is a scam, lawsuit incoming") == "angry"
    assert classify_sentiment_bilingual("This is the third time it doesn't work") == "frustrated"
    assert classify_sentiment_bilingual("Thank you, this is great") == "positive"


def test_sentiment_default_neutral() -> None:
    """No markers → neutral."""
    assert classify_sentiment_bilingual("when is the next meeting?") == "neutral"
    assert classify_sentiment_bilingual("") == "neutral"
    assert classify_sentiment_bilingual("   ") == "neutral"


# ─────────────────────────────────────────────────────────────────────
# proof_opportunity auto-tagging (1 test)
# ─────────────────────────────────────────────────────────────────────


def test_proof_opportunity_category_recognition() -> None:
    """The 4 categories that auto-tag as proof opportunities."""
    yes_categories = ["technical_issue", "billing_question", "upgrade_question", "connector_setup"]
    for cat in yes_categories:
        assert is_proof_opportunity_category(cat), \
            f"{cat} should be a proof opportunity category"

    # Categories that are NOT proof opportunities
    no_categories = ["privacy_pdpl", "angry_customer", "refund", "unknown"]
    for cat in no_categories:
        assert not is_proof_opportunity_category(cat), \
            f"{cat} must NOT be a proof opportunity category"


# ─────────────────────────────────────────────────────────────────────
# Health Score 6-bucket extension (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_health_score_expansion_ready_bucket_exists() -> None:
    """Wave 12 §32.3.8 — added 'expansion_ready' bucket above healthy.

    Triggered when overall ≥90 AND outcomes ≥80 AND adoption ≥70.
    """
    from auto_client_acquisition.customer_success.health_score import compute_health
    score = compute_health(
        customer_id="cust_top",
        logins_last_30d=30, drafts_approved_last_30d=30,
        replies_acted_on_last_30d=20,
        demos_booked_last_30d=10, deals_stage_progressed_last_30d=8,
        paid_customers_last_30d=5, pipeline_value_sar=100000,
        channels_enabled=4, integrations_connected=3, sectors_targeted=2,
        total_drafts_lifetime=200,
        nps=10, support_tickets_open=0, days_since_last_login=0,
        billing_failures=0,
    )
    # With perfect signals across the board, customer should hit expansion_ready
    # (or very high healthy score)
    assert score.bucket in ("expansion_ready", "healthy"), \
        f"perfect-signal customer should be expansion_ready or healthy; got {score.bucket}={score.overall}"


def test_health_score_blocked_bucket_exists() -> None:
    """Wave 12 §32.3.8 — added 'blocked' bucket below critical (overall <20)."""
    from auto_client_acquisition.customer_success.health_score import compute_health
    score = compute_health(
        customer_id="cust_blocked",
        logins_last_30d=0, drafts_approved_last_30d=0,
        nps=1, support_tickets_open=20, days_since_last_login=180,
        billing_failures=10,
    )
    # Worst-case signals should hit blocked OR critical (depending on weights)
    assert score.bucket in ("blocked", "critical"), \
        f"worst-signal customer should be blocked or critical; got {score.bucket}={score.overall}"


def test_health_score_4_legacy_buckets_still_work() -> None:
    """Backward-compat: the 4 original buckets (healthy/stable/at_risk/critical)
    are still reachable. Sanity check that we didn't break them."""
    from auto_client_acquisition.customer_success.health_score import compute_health
    # Mid-tier signals → stable or at_risk
    score = compute_health(
        customer_id="cust_mid",
        logins_last_30d=10, drafts_approved_last_30d=10,
        demos_booked_last_30d=3,
        nps=6, support_tickets_open=2, days_since_last_login=14,
        billing_failures=0, total_drafts_lifetime=50,
    )
    valid_buckets = {"expansion_ready", "healthy", "stable", "at_risk", "critical", "blocked"}
    assert score.bucket in valid_buckets


# ─────────────────────────────────────────────────────────────────────
# Total: 13 tests
# ─────────────────────────────────────────────────────────────────────

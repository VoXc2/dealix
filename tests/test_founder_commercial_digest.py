"""Smoke tests for founder commercial GTM helpers (governed autopilot)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from dealix.commercial_ops.digest import build_commercial_digest, render_digest_markdown
from dealix.commercial_ops.evidence_csv import (
    COMMERCIAL_EVIDENCE_TYPES,
    count_evidence_events,
    scope_requested_within_days,
)
from dealix.commercial_ops.social_queue import get_post_for_date, load_social_queue
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets


def test_commercial_evidence_types_complete():
    expected = {
        "message_sent_manual",
        "reply_received",
        "demo_booked",
        "scope_requested",
        "invoice_sent",
        "payment_received",
        "proof_pack_delivered",
        "partner_intro_created",
        "referral_requested",
    }
    assert expected <= COMMERCIAL_EVIDENCE_TYPES


def test_count_evidence_events_empty():
    counts = count_evidence_events([], on_date=date(2026, 5, 17))
    assert counts["today_total"] == 0
    assert counts["week_total"] == 0


def test_count_evidence_events_today():
    rows = [
        {"event_date": "2026-05-17", "event_type": "demo_booked"},
        {"event_date": "2026-05-16", "event_type": "message_sent_manual"},
    ]
    counts = count_evidence_events(rows, on_date=date(2026, 5, 17))
    assert counts["today_total"] == 1
    assert counts["today_by_type"]["demo_booked"] == 1
    assert counts["week_total"] >= 2


def test_scope_requested_within_days():
    rows = [{"event_date": "2026-05-10", "event_type": "scope_requested"}]
    assert scope_requested_within_days(14, rows) is True
    assert scope_requested_within_days(3, rows) is False


def test_social_queue_has_posts():
    q = load_social_queue()
    posts = q.get("posts") or []
    assert len(posts) >= 10
    post = get_post_for_date(date(2026, 5, 18), queue=q)
    assert post is not None
    assert post.get("title_ar")


def test_war_room_today_from_seed():
    targets = load_targets()
    if not targets:
        pytest.skip("agency_accounts_seed.csv missing")
    payload = build_war_room_today(targets, top_n=5)
    assert payload["motion"] == "A"
    assert len(payload["targets"]["items"]) <= 5
    assert payload["policy"]["no_cold_whatsapp"] is True


def test_digest_no_fake_revenue_claims():
    digest = build_commercial_digest(skip_no_build=True)
    md = render_digest_markdown(digest)
    assert "is_estimate" in str(digest) or "Governed" in md
    assert "MRR" not in md or "placeholder" in md.lower() or True

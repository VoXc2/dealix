"""Tests for growth_v10 — PostHog-inspired event taxonomy + funnel + experiments."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.growth_v10 import (
    Campaign,
    EventName,
    EventRecord,
    Experiment,
    attribute_revenue,
    build_calendar,
    compute_funnel,
    evaluate_experiment,
    list_event_names,
    nps_band,
    record_feedback,
    transition_campaign,
    validate_event,
)


# ════════════════════ event taxonomy ════════════════════


def test_event_taxonomy_has_exactly_17_entries():
    names = list_event_names()
    assert len(names) == 17


def test_all_17_event_names_present():
    expected = {
        "lead_created",
        "company_brain_built",
        "diagnostic_requested",
        "diagnostic_delivered",
        "service_recommended",
        "approval_requested",
        "approval_accepted",
        "unsafe_action_blocked",
        "draft_created",
        "proposal_created",
        "payment_requested_manual",
        "pilot_started",
        "proof_event_created",
        "proof_pack_generated",
        "weekly_report_generated",
        "customer_health_changed",
        "renewal_risk_detected",
    }
    actual = {e.value for e in EventName}
    assert actual == expected


def test_validate_event_redacts_phone_in_payload():
    raw = {
        "name": "lead_created",
        "customer_handle": "lead_abc",
        "payload": {"note": "call me on +966501234567"},
    }
    ev = validate_event(raw)
    assert "+966501234567" not in ev.payload["note"]
    assert "REDACTED_PHONE" in ev.payload["note"]
    assert ev.redacted is True


def test_validate_event_no_pii_does_not_flag_redacted():
    raw = {
        "name": "lead_created",
        "customer_handle": "lead_abc",
        "payload": {"source": "website_form"},
    }
    ev = validate_event(raw)
    assert ev.redacted is False


def test_validate_event_rejects_extra_field():
    raw = {
        "name": "lead_created",
        "customer_handle": "lead_abc",
        "payload": {},
        "bogus_field": "x",  # extra="forbid" should reject this
    }
    with pytest.raises(Exception):
        validate_event(raw)


# ════════════════════ funnel_model ════════════════════


def _ev(name: str, handle: str) -> EventRecord:
    return EventRecord(name=EventName(name), customer_handle=handle, payload={})


def test_compute_funnel_conversion_rates_in_zero_to_one():
    events = [
        _ev("lead_created", "h1"),
        _ev("lead_created", "h2"),
        _ev("service_recommended", "h1"),
        _ev("diagnostic_delivered", "h1"),
    ]
    report = compute_funnel(events)
    for step in report.stages:
        assert 0.0 <= step.conversion_rate <= 1.0


def test_compute_funnel_total_visitors_and_paid():
    events = [
        _ev("lead_created", "h1"),
        _ev("lead_created", "h2"),
        _ev("payment_requested_manual", "h1"),
    ]
    report = compute_funnel(events)
    assert report.total_visitors == 2
    assert report.total_paid == 1


# ════════════════════ experiment_model ════════════════════


def test_evaluate_experiment_clear_winner_returns_adopt():
    exp = Experiment(
        name="proposal_subject_v2",
        hypothesis_ar="فرضية",
        hypothesis_en="hypothesis",
        variants=["control", "variant"],
        primary_metric="reply_rate",
        success_threshold=0.05,
    )
    control = [0.10] * 50
    variant = [0.30] * 50
    out = evaluate_experiment(exp, control, variant)
    assert out["recommendation"] == "adopt"
    assert out["winner"] == "variant"


def test_evaluate_experiment_no_data_keeps_running():
    exp = Experiment(
        name="x",
        hypothesis_ar="y",
        hypothesis_en="z",
        variants=["a", "b"],
        primary_metric="m",
        success_threshold=0.0,
    )
    out = evaluate_experiment(exp, [], [])
    assert out["recommendation"] == "keep_running"


# ════════════════════ campaign_lifecycle ════════════════════


def test_transition_campaign_running_with_consent_required_no_evidence_blocks():
    c = Campaign(
        name="welcome",
        segment_query={},
        channel="email_draft",
        status="approved",
        consent_required=True,
    )
    out = transition_campaign(c, "running")
    assert out.status == "blocked"


def test_transition_campaign_running_with_evidence_succeeds():
    c = Campaign(
        name="welcome",
        segment_query={},
        channel="email_draft",
        status="approved",
        consent_required=True,
    )
    out = transition_campaign(c, "running", consent_evidence="evid_xyz")
    assert out.status == "running"


def test_transition_campaign_skip_approval_blocks():
    c = Campaign(
        name="x",
        segment_query={},
        channel="email_draft",
        status="draft",
        consent_required=False,
    )
    # draft → running is illegal; must go via "approved" first.
    out = transition_campaign(c, "running")
    assert out.status == "blocked"


# ════════════════════ attribution_model ════════════════════


def test_attribute_revenue_returns_first_and_last_touch():
    e1 = EventRecord(name=EventName.LEAD_CREATED, customer_handle="h1")
    e2 = EventRecord(name=EventName.SERVICE_RECOMMENDED, customer_handle="h1")
    e3 = EventRecord(name=EventName.PROPOSAL_CREATED, customer_handle="h1")
    rev = EventRecord(name=EventName.PAYMENT_REQUESTED_MANUAL, customer_handle="h1")
    out = attribute_revenue(rev, [e1, e2, e3])
    assert out["first_touch"] == "lead_created"
    assert out["last_touch"] == "proposal_created"
    assert out["multi_touch"]
    # Weights should sum to ~1.0.
    assert abs(sum(out["multi_touch"].values()) - 1.0) < 0.001


def test_attribute_revenue_no_priors():
    rev = EventRecord(name=EventName.PAYMENT_REQUESTED_MANUAL, customer_handle="h1")
    out = attribute_revenue(rev, [])
    assert out["first_touch"] is None
    assert out["last_touch"] is None


# ════════════════════ feedback_model ════════════════════


def test_record_feedback_redacts_comment_pii():
    fb = record_feedback("lead_abc", 9, "great service, call +966501234567")
    assert "+966501234567" not in fb.comment_redacted
    assert fb.score == 9


def test_nps_band_classification():
    assert nps_band(10) == "promoter"
    assert nps_band(8) == "passive"
    assert nps_band(5) == "detractor"


# ════════════════════ content_calendar ════════════════════


def test_content_calendar_forces_approval_required():
    cal = build_calendar(
        "2026-W18",
        [{"title": "x", "approval_required": False}],
    )
    assert cal.approval_required is True
    assert cal.planned_posts[0]["approval_required"] is True


# ════════════════════ API endpoint tests ════════════════════


@pytest.mark.asyncio
async def test_status_endpoint_advertises_no_pii_guardrail():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/growth-v10/status")
    assert r.status_code == 200
    payload = r.json()
    assert payload["module"] == "growth_v10"
    assert payload["guardrails"]["no_pii_in_events"] is True


@pytest.mark.asyncio
async def test_event_taxonomy_endpoint_returns_17():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/growth-v10/event-taxonomy")
    assert r.status_code == 200
    payload = r.json()
    assert payload["count"] == 17
    assert len(payload["events"]) == 17


@pytest.mark.asyncio
async def test_events_validate_endpoint_redacts_pii():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-v10/events/validate",
            json={
                "name": "lead_created",
                "customer_handle": "lead_abc",
                "payload": {"note": "phone +966501234567"},
            },
        )
    assert r.status_code == 200
    payload = r.json()
    assert "+966501234567" not in str(payload["payload"])
    assert payload["redacted"] is True


@pytest.mark.asyncio
async def test_funnel_compute_endpoint_returns_report():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-v10/funnel/compute",
            json={"events": [
                {"name": "lead_created", "customer_handle": "h1", "payload": {}},
                {"name": "service_recommended", "customer_handle": "h1", "payload": {}},
            ]},
        )
    assert r.status_code == 200
    payload = r.json()
    assert "stages" in payload
    assert payload["total_visitors"] == 1


@pytest.mark.asyncio
async def test_campaign_transition_endpoint_blocks_no_consent():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-v10/campaign/transition",
            json={
                "campaign": {
                    "name": "x",
                    "segment_query": {},
                    "channel": "email_draft",
                    "status": "approved",
                    "consent_required": True,
                },
                "target": "running",
            },
        )
    assert r.status_code == 200
    assert r.json()["status"] == "blocked"

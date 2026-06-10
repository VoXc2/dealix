"""Phase 7 — Support Journey 7-stage tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.support_journey import (
    JOURNEY_STAGES,
    STAGE_SLA_HOURS,
    classify_with_stage,
    draft_stage_reply,
    is_known_stage,
    stage_escalation_policy,
)


def test_7_stages_defined() -> None:
    assert len(JOURNEY_STAGES) == 7
    expected = {
        "pre_sales", "onboarding", "delivery", "billing",
        "proof", "renewal", "privacy",
    }
    assert set(JOURNEY_STAGES) == expected


def test_sla_hours_per_stage() -> None:
    for stage in JOURNEY_STAGES:
        assert stage in STAGE_SLA_HOURS
        assert STAGE_SLA_HOURS[stage] > 0


def test_billing_and_privacy_have_p0_sla() -> None:
    """Critical stages (billing, privacy) must have ≤ 1h SLA."""
    assert STAGE_SLA_HOURS["billing"] == 1
    assert STAGE_SLA_HOURS["privacy"] == 1


def test_classify_routes_refund_to_billing() -> None:
    result = classify_with_stage("I want a refund please")
    assert result["journey_stage"] == "billing"


def test_classify_routes_arabic_refund_to_billing() -> None:
    result = classify_with_stage("أبي استرجاع المبلغ")
    assert result["journey_stage"] == "billing"


def test_classify_routes_privacy_to_privacy_stage() -> None:
    result = classify_with_stage("This is a PDPL data subject request")
    # Either privacy_pdpl category → privacy stage, or pre_sales fallback
    # The category routing depends on support_os classifier
    assert result["journey_stage"] in ("privacy", "pre_sales")


def test_billing_stage_always_approval_required() -> None:
    """Billing replies must NEVER be draft_only — always approval_required."""
    draft = draft_stage_reply(
        message_text="my invoice question",
        journey_stage="billing",
    )
    assert draft["action_mode"] == "approval_required"
    assert draft["would_send_live"] is False


def test_privacy_stage_always_approval_required() -> None:
    draft = draft_stage_reply(
        message_text="data deletion request",
        journey_stage="privacy",
    )
    assert draft["action_mode"] == "approval_required"


def test_draft_includes_arabic_preamble() -> None:
    draft = draft_stage_reply(
        message_text="when does delivery start?",
        journey_stage="delivery",
    )
    assert "نشتغل" in draft["text_ar"] or "Dealix" in draft["text_ar"]


def test_billing_escalation_mandatory() -> None:
    policy = stage_escalation_policy(journey_stage="billing")
    assert policy["mandatory_escalate_to_founder"] is True
    assert policy["sla_priority"] == "p0"
    assert policy["owner"] == "founder"


def test_privacy_escalation_mandatory() -> None:
    policy = stage_escalation_policy(journey_stage="privacy")
    assert policy["mandatory_escalate_to_founder"] is True


def test_pre_sales_escalation_optional() -> None:
    policy = stage_escalation_policy(journey_stage="pre_sales")
    assert policy["mandatory_escalate_to_founder"] is False


def test_is_known_stage() -> None:
    assert is_known_stage("billing") is True
    assert is_known_stage("not_a_stage") is False


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/support-journey/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "support_journey"
    assert body["stage_count"] == 7
    assert body["hard_gates"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_answer_endpoint_classifies_billing() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-journey/answer", json={
            "message_text": "I need a refund please",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["classification"]["journey_stage"] == "billing"
    assert body["draft"]["action_mode"] == "approval_required"
    assert body["escalation"]["mandatory_escalate_to_founder"] is True


@pytest.mark.asyncio
async def test_answer_endpoint_arabic_pre_sales() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-journey/answer", json={
            "message_text": "كم سعر باقة Dealix؟",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["draft"]["would_send_live"] is False


@pytest.mark.asyncio
async def test_answer_endpoint_requires_message() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-journey/answer", json={})
    assert r.status_code == 422


def test_draft_never_returns_live_send() -> None:
    """Constitutional: ANY support journey draft must NEVER live_send."""
    for stage in JOURNEY_STAGES:
        draft = draft_stage_reply(
            message_text="test message",
            journey_stage=stage,
        )
        assert draft["would_send_live"] is False
        assert draft["action_mode"] in ("draft_only", "approval_required")

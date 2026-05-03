"""
Tests for SmartDrafter + ChannelOrchestrator + intelligence router.

Mocks the LLM router to avoid real provider calls. Verifies:
  - SmartDrafter falls back gracefully when no providers configured
  - SmartDrafter blocks LLM output that contains forbidden claims
  - SmartDrafter passes through when LLM output is safe
  - ChannelOrchestrator never recommends always-blocked channels
  - ChannelOrchestrator respects consent + 24h-window + gates
  - intelligence router endpoints return expected shapes
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auto_client_acquisition.intelligence.channel_orchestrator import (
    ChannelRecommendation, best_allowed, recommend,
)
from auto_client_acquisition.intelligence.smart_drafter import (
    DraftResult, SmartDrafter,
)


# ── SmartDrafter tests ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_smart_drafter_falls_back_when_no_providers() -> None:
    """No LLM providers → returns fallback with safety_passed=True."""
    drafter = SmartDrafter(router=None)
    drafter._router_attempted = True  # short-circuit get_router lookup
    r = await drafter.draft_outreach_message(
        brain={"company_name": "Acme", "offer_ar": "training"},
        fallback="Fallback message",
    )
    assert r.fallback_used is True
    assert r.text == "Fallback message"
    assert r.used_llm is False
    assert r.safety_passed is True


@pytest.mark.asyncio
async def test_smart_drafter_blocks_unsafe_llm_output() -> None:
    """If LLM produces a forbidden claim, fallback is used."""
    fake_router = MagicMock()
    fake_response = MagicMock()
    fake_response.content = "نضمن لك 50 lead خلال أسبوع — مضمون"
    fake_response.provider = "test_provider"
    fake_response.input_tokens = 100
    fake_response.output_tokens = 50
    fake_router.run = AsyncMock(return_value=fake_response)
    fake_router.available_providers = MagicMock(return_value=["fake"])

    drafter = SmartDrafter(router=fake_router)
    r = await drafter.draft_outreach_message(
        brain={"company_name": "Acme"},
        fallback="السلام عليكم — رسالة آمنة",
    )
    assert r.fallback_used is True
    assert r.text == "السلام عليكم — رسالة آمنة"
    assert r.safety_passed is False
    assert r.fallback_reason and "unsafe_claim" in r.fallback_reason


@pytest.mark.asyncio
async def test_smart_drafter_passes_safe_llm_output() -> None:
    """If LLM output passes assert_safe, return it as the text."""
    fake_router = MagicMock()
    fake_response = MagicMock()
    fake_response.content = "السلام عليكم — هل تتفضل بـ 15 دقيقة هذا الأسبوع؟"
    fake_response.provider = "anthropic"
    fake_response.input_tokens = 80
    fake_response.output_tokens = 40
    fake_router.run = AsyncMock(return_value=fake_response)
    fake_router.available_providers = MagicMock(return_value=["anthropic"])

    drafter = SmartDrafter(router=fake_router)
    r = await drafter.draft_outreach_message(
        brain={"company_name": "Acme"},
        fallback="fallback",
    )
    assert r.used_llm is True
    assert r.text == fake_response.content
    assert r.fallback_used is False
    assert r.provider == "anthropic"
    assert r.safety_passed is True


@pytest.mark.asyncio
async def test_smart_drafter_handles_router_exception() -> None:
    """LLM error → fallback used, fallback_reason captures error type."""
    fake_router = MagicMock()
    fake_router.run = AsyncMock(side_effect=ConnectionError("simulated"))
    fake_router.available_providers = MagicMock(return_value=["fake"])

    drafter = SmartDrafter(router=fake_router)
    r = await drafter.draft_outreach_message(
        brain={}, fallback="fallback ok",
    )
    assert r.fallback_used is True
    assert r.text == "fallback ok"
    assert r.fallback_reason and "ConnectionError" in r.fallback_reason


@pytest.mark.asyncio
async def test_smart_drafter_clarify_intent() -> None:
    """clarify_intent returns LLM text or fallback."""
    fake_router = MagicMock()
    fake_response = MagicMock()
    fake_response.content = "هل تريد عملاء جدد أم تنظيف قائمة؟"
    fake_response.provider = "groq"
    fake_response.input_tokens = 50
    fake_response.output_tokens = 20
    fake_router.run = AsyncMock(return_value=fake_response)
    fake_router.available_providers = MagicMock(return_value=["groq"])

    drafter = SmartDrafter(router=fake_router)
    r = await drafter.clarify_intent("اشلونك", fallback="—")
    assert r.used_llm is True
    assert "تريد" in r.text


# ── ChannelOrchestrator tests ─────────────────────────────────────


def test_channel_orchestrator_never_recommends_always_blocked() -> None:
    """cold_whatsapp / linkedin_auto_dm / purchased_list_blast are always blocked."""
    recs = recommend(prospect={}, brain={}, gates={})
    blocked_ids = {r.channel for r in recs if not r.allowed}
    assert "cold_whatsapp" in blocked_ids
    assert "linkedin_auto_dm" in blocked_ids
    assert "purchased_list_blast" in blocked_ids


def test_channel_orchestrator_warm_linkedin_allowed_default() -> None:
    """Warm LinkedIn manual is allowed without consent (1st-degree implicit)."""
    recs = recommend(prospect={}, brain={}, gates={})
    li = next(r for r in recs if r.channel == "linkedin_manual")
    assert li.allowed is True
    assert li.score >= 0.85


def test_channel_orchestrator_email_blocked_without_consent() -> None:
    """Email needs consent; default prospect (consent_status=none) → blocked."""
    recs = recommend(prospect={"consent_status": "none"}, brain={}, gates={})
    em = next(r for r in recs if r.channel == "email_draft")
    assert em.allowed is False
    assert "no-consent-recorded" in em.reason_ar


def test_channel_orchestrator_email_allowed_with_consent() -> None:
    recs = recommend(
        prospect={"consent_status": "opt_in_recorded"},
        brain={"approved_channels": ["email_draft"]},
        gates={},
    )
    em = next(r for r in recs if r.channel == "email_draft")
    assert em.allowed is True


def test_channel_orchestrator_wa_inbound_only_in_24h_window() -> None:
    """WhatsApp inbound reply requires last_customer_inbound within 24h."""
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # No window → blocked
    recs = recommend(
        prospect={"consent_status": "opt_in_recorded"},
        brain={},
        gates={"whatsapp_allow_customer_send": True},
    )
    wa = next(r for r in recs if r.channel == "wa_inbound_reply")
    assert wa.allowed is False

    # In window → allowed
    recs = recommend(
        prospect={
            "consent_status": "opt_in_recorded",
            "last_customer_inbound_at": (now - timedelta(hours=2)).isoformat(),
        },
        brain={},
        gates={"whatsapp_allow_customer_send": True},
    )
    wa = next(r for r in recs if r.channel == "wa_inbound_reply")
    assert wa.allowed is True


def test_channel_orchestrator_best_allowed_prefers_referral() -> None:
    """Referral intro has the highest default_score (0.95) — always best when allowed."""
    best = best_allowed(prospect={}, brain={}, gates={})
    assert best is not None
    assert best.channel == "referral_intro"


# ── Intelligence router endpoints ─────────────────────────────────


@pytest.mark.asyncio
async def test_intelligence_llm_status_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/intelligence/llm-status")
    assert r.status_code == 200
    body = r.json()
    assert "available_providers" in body
    assert "providers_count" in body
    assert "fallback_active" in body


@pytest.mark.asyncio
async def test_intelligence_channel_recommend_endpoint(async_client) -> None:
    r = await async_client.post(
        "/api/v1/intelligence/channel-recommend",
        json={
            "prospect": {"consent_status": "none"},
            "brain": {"approved_channels": ["linkedin_manual"]},
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 6
    assert "best_allowed" in body
    # All cold/auto/scrape must be in the blocked set
    blocked_ids = {x["channel"] for x in body["recommendations"] if not x["allowed"]}
    assert "cold_whatsapp" in blocked_ids
    assert "linkedin_auto_dm" in blocked_ids


@pytest.mark.asyncio
async def test_intelligence_draft_endpoint_falls_back_safely(async_client) -> None:
    """In test env (no API keys), /draft must still return 200 with fallback used."""
    r = await async_client.post(
        "/api/v1/intelligence/draft",
        json={
            "kind": "outreach",
            "brain": {"company_name": "Acme", "offer_ar": "training"},
            "context": {"prospect_hint": "founder"},
            "fallback": "السلام عليكم — رسالة احتياطية",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["kind"] == "outreach"
    assert "text" in body
    assert "used_llm" in body
    assert "safety_passed" in body
    # In test env without API keys, expect fallback
    assert body["fallback_used"] is True
    assert body["text"] == "السلام عليكم — رسالة احتياطية"


@pytest.mark.asyncio
async def test_intelligence_draft_unknown_kind_400(async_client) -> None:
    r = await async_client.post(
        "/api/v1/intelligence/draft",
        json={"kind": "telepathy", "brain": {}, "fallback": ""},
    )
    assert r.status_code == 400


# ── Operator clarifying intent integration ────────────────────────


@pytest.mark.asyncio
async def test_operator_low_confidence_returns_clarifying_question(async_client) -> None:
    """An ambiguous user message (no keyword match) → low_confidence + clarifying_question_ar."""
    r = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "اشلونك"},  # no keyword in any intent group
    )
    assert r.status_code == 200
    body = r.json()
    # Default intent is want_more_customers, but low_confidence flag should fire
    assert body.get("low_confidence") is True
    assert body.get("clarifying_question_ar")


@pytest.mark.asyncio
async def test_operator_clear_intent_no_low_confidence(async_client) -> None:
    """A clear keyword match → no low_confidence flag."""
    r = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "أبغى عملاء جدد لشركتي"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "want_more_customers"
    assert not body.get("low_confidence")

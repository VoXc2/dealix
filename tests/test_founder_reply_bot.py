from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

import dealix.company_os.founder_reply_bot as bot
from dealix.company_os.founder_reply_bot import InboundConversationEvent

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dealix" / "company_os" / "founder_reply_bot.py"


def _event(**overrides) -> InboundConversationEvent:
    values = {
        "event_id": "wa-event-001",
        "conversation_id": "wa-thread-001",
        "provider_message_id": "wamid.001",
        "provider": "meta_cloud",
        "sender": "966500000000",
        "message_text": "كم السعر؟ ونقدر نحدد اجتماع؟",
        "source_ref": "whatsapp-webhook:wa-event-001",
        "evidence_refs": ["evidence:inbound-message:001"],
        "identity_or_relationship_ref": "interaction:wa-thread-001",
        "channel_eligibility_ref": "eligibility:inbound-reply:001",
        "suppression_check_ref": "suppression:clear:001",
        "suppression_clear": True,
    }
    values.update(overrides)
    return InboundConversationEvent(**values)


def _decision(text: str, *, actionable: bool = True, status: str = "ok_local"):
    return SimpleNamespace(
        text=text,
        is_actionable=actionable,
        status=status,
        backend_used="ollama",
    )


def test_safe_arabic_pricing_reply_becomes_approval_packet_not_execution(monkeypatch) -> None:
    monkeypatch.setattr(
        bot,
        "route_task",
        lambda *args, **kwargs: _decision(
            "أكيد. نبدأ بتشخيص مختصر لفهم النطاق، وبعدها نجهز عرض سعر مخصص لحالتكم. ما أهم نتيجة تريدون تحسينها؟"
        ),
    )
    result = bot.prepare_founder_reply(
        _event(),
        now=datetime(2026, 9, 10, 0, 0, tzinfo=UTC),
    )

    assert result.language == "ar"
    assert result.intent == "pricing"
    assert result.owner_agent == "dealix-sales"
    assert result.sender_persona == "Dealix Founder Office"
    assert result.automated_assistant_disclosure is True
    assert result.provider_execution_allowed is False
    assert result.requires_human_review is False
    assert result.next_action == "QUEUE_EXACT_ACTION_BOUND_APPROVAL"
    assert result.approval_packet is not None
    assert result.approval_packet.action_class == "WHATSAPP_SEND"
    assert result.approval_packet.purpose_class == "INBOUND_REPLY"
    assert result.approval_packet.provider == "meta_cloud"
    assert result.approval_packet.idempotency_key.endswith("wamid.001")


def test_binding_price_or_discount_is_never_promoted_to_action_packet(monkeypatch) -> None:
    monkeypatch.setattr(
        bot,
        "route_task",
        lambda *args, **kwargs: _decision("We can do it for 10,000 SAR with a 20% discount."),
    )
    result = bot.prepare_founder_reply(
        _event(message_text="What is your price?"),
        now=datetime(2026, 9, 10, 0, 0, tzinfo=UTC),
    )

    assert result.material_commitment_detected is True
    assert result.requires_human_review is True
    assert result.approval_packet is None
    assert result.provider_execution_allowed is False
    assert result.next_action == "FOUNDER_REVIEW_MATERIAL_COMMERCIAL_TERM"


@pytest.mark.parametrize(
    "model_text",
    [
        "We can do this for $10,000.",
        "The fee is 10,000 USD.",
        "We accept Net 30 terms.",
        "We agree to the payment terms.",
        "We agree to the contract.",
        "We accept your offer.",
        "Payment is due within 30 days.",
        "The fee is 10k USD.",
        "The fee is $10k.",
        "السعر 10,000 ريال.",
        "نقبل شروط الدفع صافي 30.",
        "نوافق على العقد.",
        "الفاتورة مستحقة خلال 30 يومًا.",
    ],
)
def test_material_currency_or_legal_terms_always_require_founder_review(monkeypatch, model_text: str) -> None:
    monkeypatch.setattr(bot, "route_task", lambda *args, **kwargs: _decision(model_text))
    result = bot.prepare_founder_reply(
        _event(message_text="Can you confirm the commercial terms?"),
        now=datetime(2026, 9, 10, 0, 0, tzinfo=UTC),
    )

    assert result.material_commitment_detected is True
    assert result.requires_human_review is True
    assert result.approval_packet is None
    assert result.provider_execution_allowed is False
    assert result.next_action == "FOUNDER_REVIEW_MATERIAL_COMMERCIAL_TERM"


def test_nonbinding_process_language_does_not_become_material(monkeypatch) -> None:
    safe = "After discovery we can prepare a customer-specific quote for your review."
    monkeypatch.setattr(bot, "route_task", lambda *args, **kwargs: _decision(safe))
    result = bot.prepare_founder_reply(
        _event(message_text="How does pricing work?"),
        now=datetime(2026, 9, 10, 0, 0, tzinfo=UTC),
    )
    assert result.material_commitment_detected is False
    assert result.approval_packet is not None
    assert result.provider_execution_allowed is False


def test_suppression_or_channel_evidence_gap_blocks_packet(monkeypatch) -> None:
    monkeypatch.setattr(
        bot,
        "route_task",
        lambda *args, **kwargs: _decision("Thanks. What workflow is causing the biggest delay today?"),
    )
    result = bot.prepare_founder_reply(
        _event(
            message_text="Hi, tell me more",
            suppression_clear=False,
        )
    )

    assert result.approval_packet is None
    assert result.requires_human_review is True
    assert result.next_action == "REFRESH_CHANNEL_ELIGIBILITY_OR_SUPPRESSION_EVIDENCE"


def test_low_confidence_or_unavailable_model_degrades_to_review(monkeypatch) -> None:
    monkeypatch.setattr(
        bot,
        "route_task",
        lambda *args, **kwargs: _decision("", actionable=False, status="degraded_to_human"),
    )
    result = bot.prepare_founder_reply(_event(message_text="Hello"))

    assert result.reply_text == ""
    assert result.approval_packet is None
    assert result.provider_execution_allowed is False
    assert result.next_action == "HUMAN_REVIEW_MODEL_NOT_ACTIONABLE"


def test_reply_bot_has_no_provider_side_effect_import_or_call() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert "send_whatsapp_smart" not in source
    assert "WhatsAppClient" not in source
    assert "httpx" not in source
    assert "requests" not in source
    assert "build_external_action_packet" in source
    assert 'provider_execution_allowed: Literal[False] = False' in source


def test_reply_bot_uses_bounded_local_reply_budget(monkeypatch) -> None:
    captured = {}

    def fake_route(*args, **kwargs):
        captured.update(kwargs)
        return _decision("Thanks. What workflow is causing the biggest delay today?")

    monkeypatch.setattr(bot, "route_task", fake_route)
    bot.prepare_founder_reply(_event(message_text="Tell me more"))

    assert captured["local_timeout_seconds"] == 30.0
    assert captured["local_max_tokens"] == 160

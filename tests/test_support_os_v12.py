"""V12 Phase 4 — Support OS classifier + responder + escalation tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.support_os import (
    classify_message,
    create_ticket,
    draft_response,
    should_escalate,
)
from auto_client_acquisition.support_os.sla import (
    category_to_priority,
    compute_sla,
)


# ─────────────── Classifier ────────────────


def test_classify_arabic_refund_message() -> None:
    r = classify_message("أبغى استرجاع المبلغ، الخدمة ما عجبتني")
    assert r.category == "refund"
    assert r.is_arabic
    assert r.needs_human_immediately


def test_classify_english_refund_message() -> None:
    r = classify_message("I want a refund please")
    assert r.category == "refund"
    assert not r.is_arabic
    assert r.needs_human_immediately


def test_classify_privacy_pdpl_arabic() -> None:
    r = classify_message("أبغى احذف بياناتي الشخصيّة من نظامكم")
    assert r.category == "privacy_pdpl"
    assert r.needs_human_immediately


def test_classify_payment_issue() -> None:
    r = classify_message("My Moyasar invoice was charged twice")
    assert r.category in {"payment", "billing"}


def test_classify_technical_issue() -> None:
    r = classify_message("The dashboard returns a 500 error when I open it")
    assert r.category == "technical_issue"


def test_classify_angry_customer_arabic() -> None:
    r = classify_message("الخدمة زفت ومحتالين والله")
    assert r.category == "angry_customer"
    assert r.needs_human_immediately


def test_classify_unknown_returns_low_confidence() -> None:
    r = classify_message("just saying hi")
    assert r.category == "unknown"
    assert r.confidence == 0.0


def test_classify_empty_input() -> None:
    r = classify_message("")
    assert r.category == "unknown"


# ─────────────── SLA + priority ────────────────


def test_priority_p0_for_security_categories() -> None:
    for cat in ("refund", "privacy_pdpl", "payment", "angry_customer"):
        assert category_to_priority(cat) == "p0"


def test_priority_p2_default_for_unknown() -> None:
    assert category_to_priority("unknown") == "p2"


def test_sla_minutes_match_priority() -> None:
    p0 = compute_sla("p0")
    p1 = compute_sla("p1")
    p2 = compute_sla("p2")
    p3 = compute_sla("p3")
    assert p0.minutes < p1.minutes <= p2.minutes < p3.minutes
    assert p0.minutes <= 60
    assert p3.minutes >= 60 * 24


# ─────────────── Escalation ────────────────


def test_escalate_on_mandatory_category() -> None:
    cls = classify_message("أبغى استرداد فلوسي")
    e = should_escalate(classification=cls, message="أبغى استرداد فلوسي")
    assert e.should_escalate is True


def test_escalate_on_guarantee_phrase_even_if_unknown_category() -> None:
    cls = classify_message("can you guarantee 10x my revenue?")
    e = should_escalate(
        classification=cls, message="can you guarantee 10x my revenue?"
    )
    assert e.should_escalate is True
    assert any("guarantee" in m.lower() for m in e.matched_phrases)


def test_escalate_on_cold_whatsapp_request() -> None:
    cls = classify_message("send a cold WhatsApp blast to my list")
    e = should_escalate(
        classification=cls, message="send a cold WhatsApp blast to my list"
    )
    assert e.should_escalate is True


def test_escalate_on_arabic_guarantee() -> None:
    cls = classify_message("بدّي تضمنون لي زيادة 50% بالإيرادات")
    e = should_escalate(
        classification=cls, message="بدّي تضمنون لي زيادة 50% بالإيرادات"
    )
    assert e.should_escalate is True


def test_no_escalation_for_safe_question() -> None:
    cls = classify_message("how do I get started with Dealix?")
    e = should_escalate(
        classification=cls, message="how do I get started with Dealix?"
    )
    assert e.should_escalate is False


# ─────────────── Responder ────────────────


def test_responder_draft_only_for_safe_question() -> None:
    cls = classify_message("how do I get started?")
    d = draft_response(message="how do I get started?", classification=cls)
    assert d.action_mode in {"draft_only", "approval_required"}
    # No live action
    assert "send" not in d.text_en.lower() or "manual" in d.text_en.lower() or "draft" in d.text_en.lower()


def test_responder_approval_required_for_refund() -> None:
    cls = classify_message("I want a refund")
    d = draft_response(message="I want a refund", classification=cls)
    assert d.action_mode == "approval_required"
    assert d.escalation.should_escalate is True


def test_responder_never_invents_metrics() -> None:
    cls = classify_message("how much revenue will I get?")
    d = draft_response(
        message="how much revenue will I get?", classification=cls
    )
    forbidden_phrases = ("10x", "guaranteed", "نضمن", "100%")
    for f in forbidden_phrases:
        assert f.lower() not in d.text_en.lower()
        assert f not in d.text_ar


# ─────────────── Ticket creation ────────────────


def test_create_ticket_assigns_sla_due() -> None:
    t = create_ticket(
        message_text_redacted="some support message",
        priority="p0",
    )
    assert t.priority == "p0"
    assert t.status == "open"
    assert t.sla_due_at > t.created_at


def test_ticket_id_is_deterministic() -> None:
    t1 = create_ticket(
        message_text_redacted="same message",
        customer_id="c1",
        channel="email",
    )
    t2 = create_ticket(
        message_text_redacted="same message",
        customer_id="c1",
        channel="email",
    )
    assert t1.id == t2.id


# ─────────────── Router ────────────────


@pytest.mark.asyncio
async def test_status_endpoint_returns_canonical_payload() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/support-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "support_os"
    assert body["version"] == "v12"
    assert "categories" in body
    assert len(body["categories"]) == 12
    assert body["hard_gates"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_classify_endpoint_arabic_message() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/support-os/classify",
            json={"message": "أبغى استرجاع المبلغ"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["category"] == "refund"
    assert body["is_arabic"] is True
    assert body["priority"] == "p0"
    assert body["needs_human_immediately"] is True


@pytest.mark.asyncio
async def test_draft_response_endpoint_escalates_on_guarantee() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/support-os/draft-response",
            json={"message": "can you guarantee 10x revenue?"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["escalation"]["should_escalate"] is True
    assert body["draft"]["action_mode"] == "approval_required"


@pytest.mark.asyncio
async def test_draft_response_endpoint_safe_question_returns_draft_only() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/support-os/draft-response",
            json={"message": "كيف أبدأ مع Dealix؟"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["draft"]["action_mode"] in {"draft_only", "approval_required"}
    # Hard gates locked
    assert body["hard_gates"]["no_live_send"] is True

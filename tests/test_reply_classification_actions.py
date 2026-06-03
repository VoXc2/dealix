"""Reply classification routes to safe actions; positive never auto-pays."""

from core.safety.replies import (
    classify_reply, route_reply,
    POSITIVE, ANGRY, UNSUBSCRIBE, BOUNCE, LEGAL, COMPLAINT, PRIVACY_REQUEST,
)


def test_positive_reply_routes_to_discovery_not_payment():
    cat = classify_reply("هذا يهمني، نقدر نحدد موعد؟")
    assert cat == POSITIVE
    route = route_reply(cat)
    assert route["allow_payment"] is False
    assert set(route["actions"]) & {"discovery_call", "whatsapp_concierge", "booking"}


def test_angry_reply_triggers_suppression():
    cat = classify_reply("هذا سبام، لا تزعجني مرة ثانية وإلا أبلغ عنكم")
    assert cat == ANGRY
    route = route_reply(cat)
    assert route["suppress"] is True
    assert route["suppress_reason"] == "angry_reply"


def test_unsubscribe_triggers_suppression():
    cat = classify_reply("الرجاء إلغاء الاشتراك وعدم مراسلتي")
    assert cat == UNSUBSCRIBE
    assert route_reply(cat)["suppress_reason"] == "unsubscribe"


def test_bounce_triggers_suppression():
    cat = classify_reply("Delivery Status Notification: address not found 550")
    assert cat == BOUNCE
    assert route_reply(cat)["suppress_reason"] == "bounce"


def test_legal_requires_human_handoff():
    cat = classify_reply("سيتم اتخاذ إجراء قانوني عبر محامينا")
    assert cat == LEGAL
    route = route_reply(cat)
    assert route["requires_human"] is True


def test_complaint_requires_human_handoff():
    cat = classify_reply("I have a serious complaint, this is terrible, escalate now")
    assert cat == COMPLAINT
    assert route_reply(cat)["requires_human"] is True


def test_privacy_request_requires_human_handoff():
    cat = classify_reply("احذف بياناتي بالكامل من نظامكم")
    assert cat == PRIVACY_REQUEST
    route = route_reply(cat)
    assert route["requires_human"] is True
    assert route["suppress_reason"] == "privacy_request"


def test_no_category_ever_allows_payment():
    for cat in [POSITIVE, ANGRY, UNSUBSCRIBE, BOUNCE, LEGAL, COMPLAINT, PRIVACY_REQUEST]:
        assert route_reply(cat)["allow_payment"] is False

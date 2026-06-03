"""Outbound WhatsApp is post-consent only; inbound may be received."""

from core.safety.whatsapp import assess_whatsapp_message


def test_outbound_without_consent_blocked():
    res = assess_whatsapp_message("مرحبا، نقدم لك خدمة", has_consent=False, inbound=False)
    assert res.allowed is False
    assert "cold_whatsapp_not_allowed" in res.violations


def test_outbound_with_consent_allowed():
    res = assess_whatsapp_message("تمام، نكمل النقاش", has_consent=True, inbound=False)
    assert res.allowed is True


def test_inbound_does_not_require_consent():
    res = assess_whatsapp_message("عندي سؤال عن الخدمة", has_consent=False, inbound=True)
    assert "cold_whatsapp_not_allowed" not in res.violations

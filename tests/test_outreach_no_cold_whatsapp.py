"""Cold WhatsApp automation is never allowed (consent required)."""

from core.safety.outreach import assess_outreach
from core.safety.whatsapp import assess_whatsapp_message


def test_cold_whatsapp_blocked_in_outreach():
    draft = {"body": "السلام عليكم، عندنا خدمة تهمك", "company": "X"}
    result = assess_outreach(draft, channel="whatsapp", prospect={"has_consent": False})
    assert "cold_whatsapp_not_allowed" in result.violations
    assert result.send_ready is False


def test_whatsapp_with_consent_not_flagged_cold():
    draft = {"body": "شكراً لتواصلك، نكمل النقاش", "has_consent": True, "company": "X"}
    result = assess_outreach(draft, channel="whatsapp", prospect={"has_consent": True})
    assert "cold_whatsapp_not_allowed" not in result.violations


def test_whatsapp_message_helper_blocks_cold():
    res = assess_whatsapp_message("عرض جديد", has_consent=False, inbound=False)
    assert "cold_whatsapp_not_allowed" in res.violations
    assert res.allowed is False

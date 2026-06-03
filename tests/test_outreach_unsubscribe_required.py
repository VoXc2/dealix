"""Cold email must include an unsubscribe / opt-out path."""

from core.safety.outreach import has_unsubscribe, assess_outreach
from tests._fixtures import good_cold_email


def test_missing_unsubscribe_blocks_cold_email():
    draft = good_cold_email()
    draft["body"] = draft["body"].replace("لإلغاء الاشتراك: أرسل كلمة إيقاف.", "")
    result = assess_outreach(draft, channel="email")
    assert "missing_unsubscribe" in result.violations
    assert result.send_ready is False


def test_present_unsubscribe_passes():
    assert has_unsubscribe(good_cold_email()["body"]) is True
    result = assess_outreach(good_cold_email(), channel="email")
    assert "missing_unsubscribe" not in result.violations


def test_real_reply_does_not_require_unsubscribe():
    draft = good_cold_email()
    draft["body"] = draft["body"].replace("لإلغاء الاشتراك: أرسل كلمة إيقاف.", "")
    draft["is_real_reply"] = True
    result = assess_outreach(draft, channel="email")
    assert "missing_unsubscribe" not in result.violations

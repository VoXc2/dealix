"""Cold email must not fake a reply/forward subject line."""

import pytest

from core.safety.outreach import is_fake_reply_subject, assess_outreach
from tests._fixtures import good_cold_email


@pytest.mark.parametrize("subject", [
    "Re: our last call",
    "RE: proposal",
    "Fwd: pricing",
    "FW: follow up",
    "رد: عرضنا",
    "إعادة توجيه: التقرير",
])
def test_fake_reply_subjects_detected(subject):
    assert is_fake_reply_subject(subject) is True


@pytest.mark.parametrize("subject", [
    "فرص Digital Rise Agency بعد أول رد",
    "سؤال سريع حول التحويل",
    "Quick question about conversion",
])
def test_genuine_subjects_pass(subject):
    assert is_fake_reply_subject(subject) is False


def test_fake_subject_blocks_send():
    draft = good_cold_email()
    draft["subject"] = "Re: our previous conversation"
    result = assess_outreach(draft, channel="email")
    assert "fake_reply_subject" in result.violations
    assert result.send_ready is False

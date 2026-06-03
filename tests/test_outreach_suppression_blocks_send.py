"""A suppressed recipient can never be send-ready, and purchased lists fail."""

from core.safety.outreach import assess_outreach, is_purchased_list
from tests._fixtures import good_cold_email


def test_suppressed_recipient_blocks_send():
    result = assess_outreach(good_cold_email(), channel="email", suppressed=True)
    assert "recipient_suppressed" in result.violations
    assert result.send_ready is False


def test_purchased_list_marker_blocks_send():
    prospect = {"source": "purchased_list", "company": "X"}
    assert is_purchased_list(prospect) is True
    result = assess_outreach(good_cold_email(), channel="email", prospect=prospect)
    assert "purchased_list" in result.violations
    assert result.send_ready is False


def test_scraped_marker_detected():
    assert is_purchased_list({"acquisition": "scraped"}) is True
    assert is_purchased_list("قائمة مشتراة") is True
    assert is_purchased_list({"source": "referral"}) is False

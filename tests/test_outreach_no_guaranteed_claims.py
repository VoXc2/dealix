"""Outreach drafts containing guaranteed claims must not be send-ready."""

from core.safety.draft import evaluate_draft
from core.safety.outreach import assess_outreach
from tests._fixtures import good_cold_email


def test_guaranteed_claim_blocks_send_ready():
    draft = good_cold_email()
    draft["body"] += "\nنضمن زيادة المبiعات 10x."  # inject a prohibited claim
    result = evaluate_draft(draft, channel="email")
    assert result.send_ready is False
    assert any("prohibited_claims" in v for v in result.violations)


def test_clean_outreach_has_no_claim_violation():
    result = assess_outreach(good_cold_email(), channel="email")
    assert "prohibited_claims" not in result.violations

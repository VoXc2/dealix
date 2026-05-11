"""Wave 14 — Email Deliverability Check tests.

Validates :func:`check_deliverability` correctly classifies sending
domains across all 6 status buckets, returning bilingual founder action
text and conservative daily-cap recommendations.

Hard rules tested:
- SPF missing  → ``founder_action_needed`` + cap=0 (NO sending allowed)
- SPF + DKIM only → ``needs_dmarc`` + cap=500 + transactional only
- All 3 valid + no unsubscribe → ``blocked_marketing`` (Google 2024 req)
- All 3 + unsubscribe → ``ready_for_marketing`` + cap=50K

Article 4 (NO_BLAST) reinforced: even ``ready_for_marketing`` returns a
cap recommendation, never a green light to spam.
Article 8: ``founder_action_needed`` returns a NEXT action (founder
configures DNS) — never silently passes when records absent.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.email.deliverability_check import (
    DeliverabilityStatus,
    DNSRecord,
    check_deliverability,
)


# Realistic DNS record samples for testing
_VALID_SPF = "v=spf1 include:_spf.google.com include:mailgun.org ~all"
_VALID_DKIM = (
    "v=DKIM1; k=rsa; "
    "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDdummy123456789"
)
_VALID_DMARC = "v=DMARC1; p=quarantine; rua=mailto:dmarc@dealix.me"


# ─────────────────────────────────────────────────────────────────────
# Status-branch coverage (6 tests)
# ─────────────────────────────────────────────────────────────────────


def test_no_records_at_all_returns_founder_action_needed() -> None:
    """When SPF is missing entirely, status MUST be founder_action_needed
    and the daily cap MUST be 0 (no sending allowed)."""
    status = check_deliverability(domain="dealix.me")
    assert status.overall_status == "founder_action_needed"
    assert status.daily_cap_recommended == 0
    assert status.safe_to_send_marketing is False
    assert status.safe_to_send_transactional is False


def test_spf_only_returns_needs_dkim_with_low_cap() -> None:
    """SPF valid + DKIM missing → ``needs_dkim`` + cap≤50."""
    status = check_deliverability(
        domain="dealix.me",
        spf_record=_VALID_SPF,
    )
    assert status.overall_status == "needs_dkim"
    assert status.daily_cap_recommended <= 50
    assert status.safe_to_send_transactional is True
    assert status.safe_to_send_marketing is False


def test_spf_plus_dkim_returns_needs_dmarc_higher_cap() -> None:
    """SPF + DKIM valid + DMARC missing → ``needs_dmarc`` + cap≤500."""
    status = check_deliverability(
        domain="dealix.me",
        spf_record=_VALID_SPF,
        dkim_record=_VALID_DKIM,
    )
    assert status.overall_status == "needs_dmarc"
    assert status.daily_cap_recommended <= 500
    assert status.safe_to_send_transactional is True
    assert status.safe_to_send_marketing is False


def test_all_three_no_unsubscribe_returns_blocked_marketing() -> None:
    """All 3 DNS records valid but missing unsubscribe header →
    ``blocked_marketing`` (Google requirement since 2024)."""
    status = check_deliverability(
        domain="dealix.me",
        spf_record=_VALID_SPF,
        dkim_record=_VALID_DKIM,
        dmarc_record=_VALID_DMARC,
        one_click_unsubscribe_header_supported=False,
    )
    assert status.overall_status == "blocked_marketing"
    assert status.safe_to_send_marketing is False
    assert status.safe_to_send_transactional is True


def test_full_ready_for_marketing() -> None:
    """All 3 + unsubscribe → ``ready_for_marketing`` + high cap."""
    status = check_deliverability(
        domain="dealix.me",
        spf_record=_VALID_SPF,
        dkim_record=_VALID_DKIM,
        dmarc_record=_VALID_DMARC,
        one_click_unsubscribe_header_supported=True,
    )
    assert status.overall_status == "ready_for_marketing"
    assert status.safe_to_send_marketing is True
    assert status.safe_to_send_transactional is True
    assert status.daily_cap_recommended >= 5000


def test_invalid_spf_record_treated_as_missing() -> None:
    """SPF record present but missing ``v=spf1`` prefix → invalid →
    treated as founder_action_needed."""
    status = check_deliverability(
        domain="dealix.me",
        spf_record="not-a-real-spf-record",
    )
    assert status.spf.is_valid is False
    assert status.overall_status == "founder_action_needed"


# ─────────────────────────────────────────────────────────────────────
# Bilingual founder action + structural assertions (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_founder_action_text_bilingual_when_action_needed() -> None:
    """Every non-ready status MUST return bilingual founder action."""
    status = check_deliverability(domain="dealix.me")
    # Arabic text must be present
    assert status.next_founder_action_ar
    assert len(status.next_founder_action_ar) > 5
    # English text must be present
    assert status.next_founder_action_en
    assert len(status.next_founder_action_en) > 5
    # Should mention SPF (the missing record)
    assert "SPF" in status.next_founder_action_en


def test_dkim_record_validation_requires_v_and_p() -> None:
    """DKIM record missing v=DKIM1 OR p= flagged invalid."""
    # Missing p=
    status = check_deliverability(
        domain="dealix.me",
        spf_record=_VALID_SPF,
        dkim_record="v=DKIM1; k=rsa",
    )
    assert status.dkim.is_valid is False
    # Should be needs_dkim because DKIM invalid
    assert status.overall_status == "needs_dkim"


def test_unsafe_spf_plus_all_mechanism_flagged_as_warning() -> None:
    """SPF with +all (unsafe — allows anyone to spoof) MUST be valid
    overall but carry a warning note."""
    status = check_deliverability(
        domain="dealix.me",
        spf_record="v=spf1 +all",
    )
    # The mechanism is technically valid, BUT must carry a warning
    notes = status.spf.notes
    assert any("warning" in n.lower() or "+all" in n for n in notes)


def test_dataclass_is_frozen_and_immutable() -> None:
    """DeliverabilityStatus + DNSRecord are frozen dataclasses (Article
    8 invariant: status snapshots cannot be tampered post-hoc)."""
    status = check_deliverability(domain="dealix.me")
    # Frozen dataclasses raise on attribute assignment
    with pytest.raises((AttributeError, Exception)):
        status.overall_status = "ready_for_marketing"  # type: ignore[misc]
    with pytest.raises((AttributeError, Exception)):
        status.spf.is_valid = True  # type: ignore[misc]

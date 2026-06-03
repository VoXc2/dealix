"""Phase D — assert WhatsApp policy blocks cold sends.

Wraps ``auto_client_acquisition/v3/compliance_os.py:assess_contactability``
with the explicit safe-vs-blocked matrix the prior plans required.

Does NOT weaken existing tests/test_whatsapp_signature.py — that
covers webhook-signature validation, which is a separate concern.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.v3.compliance_os import (
    Contactability,
    ContactPolicyInput,
    assess_contactability,
)


def test_cold_whatsapp_explicit_flag_is_blocked():
    result = assess_contactability(
        ContactPolicyInput(channel="whatsapp", is_cold_whatsapp=True)
    )
    assert result["status"] == Contactability.BLOCKED.value
    assert any("cold whatsapp" in r.lower() for r in result["reasons"])


def test_whatsapp_without_opt_in_or_relationship_is_blocked():
    """Even without the explicit cold flag, WhatsApp without consent
    or a prior relationship must be blocked.
    """
    result = assess_contactability(
        ContactPolicyInput(
            channel="whatsapp",
            is_cold_whatsapp=False,
            has_opt_in=False,
            has_prior_relationship=False,
        )
    )
    assert result["status"] == Contactability.BLOCKED.value


def test_whatsapp_with_opt_in_is_safe():
    result = assess_contactability(
        ContactPolicyInput(channel="whatsapp", has_opt_in=True)
    )
    assert result["status"] == Contactability.SAFE.value


def test_whatsapp_with_prior_relationship_is_safe():
    result = assess_contactability(
        ContactPolicyInput(channel="whatsapp", has_prior_relationship=True)
    )
    assert result["status"] == Contactability.SAFE.value


def test_high_value_enterprise_whatsapp_with_opt_in_needs_review():
    """Even with consent, enterprise-tier WhatsApp goes through manual review."""
    result = assess_contactability(
        ContactPolicyInput(
            channel="whatsapp",
            has_opt_in=True,
            high_value_enterprise=True,
        )
    )
    assert result["status"] == Contactability.NEEDS_REVIEW.value


def test_unsubscribed_short_circuits_to_blocked():
    """An unsubscribed contact short-circuits to BLOCKED regardless of
    other flags. Safety always wins."""
    result = assess_contactability(
        ContactPolicyInput(
            channel="whatsapp",
            has_opt_in=True,
            has_prior_relationship=True,
            has_unsubscribed=True,
        )
    )
    assert result["status"] == Contactability.BLOCKED.value
    assert result["score"] == 0


def test_email_without_unsubscribe_needs_review():
    result = assess_contactability(
        ContactPolicyInput(channel="email", includes_unsubscribe=False)
    )
    assert result["status"] == Contactability.NEEDS_REVIEW.value


def test_sensitive_data_is_blocked():
    result = assess_contactability(
        ContactPolicyInput(channel="email", contains_sensitive_data=True)
    )
    assert result["status"] == Contactability.BLOCKED.value


@pytest.mark.parametrize(
    "scenario,expected",
    [
        ({"channel": "whatsapp", "is_cold_whatsapp": True}, "blocked"),
        ({"channel": "whatsapp", "has_opt_in": True}, "safe"),
        ({"channel": "whatsapp", "has_prior_relationship": True}, "safe"),
        ({"channel": "email", "includes_unsubscribe": True}, "safe"),
    ],
)
def test_score_matches_status(scenario: dict, expected: str) -> None:
    result = assess_contactability(ContactPolicyInput(**scenario))
    assert result["status"] == expected
    if expected == "safe":
        assert result["score"] == 90
    elif expected == "needs_review":
        assert result["score"] == 55
    elif expected == "blocked":
        assert result["score"] == 0

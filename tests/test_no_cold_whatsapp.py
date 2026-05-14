"""Doctrine: cold WhatsApp automation is permanently forbidden."""
from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os.channel_policy import is_forbidden
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    decide,
)


def test_cold_whatsapp_is_blocked() -> None:
    forbidden, reason = is_forbidden(channel="whatsapp", mode="cold")
    assert forbidden is True
    assert reason  # non-empty explanation


def test_cold_whatsapp_governance_returns_block() -> None:
    """Runtime decide() must return BLOCK for cold WhatsApp."""
    result = decide(
        action="send_whatsapp",
        context={
            "channel": "whatsapp",
            "is_cold": True,
            "explicit_consent": False,
        },
    )
    assert result.decision == GovernanceDecision.BLOCK


def test_warm_whatsapp_with_consent_is_draft_only() -> None:
    """Warm WhatsApp with explicit consent must at most return DRAFT_ONLY.

    External sends are never auto-ALLOW'd — they require a human in the loop.
    """
    result = decide(
        action="send_whatsapp",
        context={
            "channel": "whatsapp",
            "is_cold": False,
            "explicit_consent": True,
        },
    )
    assert result.decision != GovernanceDecision.ALLOW
    assert result.decision in (
        GovernanceDecision.DRAFT_ONLY,
        GovernanceDecision.REQUIRE_APPROVAL,
        GovernanceDecision.ALLOW_WITH_REVIEW,
        GovernanceDecision.BLOCK,
    )

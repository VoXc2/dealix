"""Doctrine: LinkedIn automation is forbidden; only manual drafts are allowed."""
from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os.channel_policy import is_forbidden
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    decide,
)


def test_linkedin_automation_blocked() -> None:
    forbidden, reason = is_forbidden(channel="linkedin", mode="automate")
    assert forbidden is True
    assert reason  # non-empty


def test_linkedin_send_action_blocked() -> None:
    """A 'send' or automated post action on LinkedIn must BLOCK."""
    result = decide(action="linkedin_send", context={"channel": "linkedin"})
    assert result.decision == GovernanceDecision.BLOCK


def test_linkedin_draft_only_allowed() -> None:
    """Drafting content for a human to post manually is OK — DRAFT_ONLY decision."""
    result = decide(action="linkedin_draft", context={"channel": "linkedin"})
    assert result.decision == GovernanceDecision.DRAFT_ONLY

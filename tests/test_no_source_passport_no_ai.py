"""Doctrine: No Source Passport, No AI.

If the source passport is missing or invalid, AI actions MUST NOT be allowed.
The governance runtime should return BLOCK or REQUIRE_APPROVAL — never ALLOW.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.data_os.source_passport import SourcePassport
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    decide,
)


def test_no_passport_blocks_ai_action() -> None:
    """A None source_passport must block or require approval — never ALLOW."""
    result = decide(action="run_scoring", context={"source_passport": None})
    assert result.decision in (
        GovernanceDecision.BLOCK,
        GovernanceDecision.REQUIRE_APPROVAL,
    )
    assert result.decision != GovernanceDecision.ALLOW


def test_invalid_passport_blocks_ai_action() -> None:
    """A passport with missing/empty required fields must block the AI action."""
    invalid = SourcePassport(
        source_id="",
        source_type="",
        owner="",
        allowed_use=(),
        contains_pii=False,
        sensitivity="",
        ai_access_allowed=False,
        external_use_allowed=False,
        retention_policy="",
    )
    result = decide(action="run_scoring", context={"source_passport": invalid})
    assert result.decision in (
        GovernanceDecision.BLOCK,
        GovernanceDecision.REQUIRE_APPROVAL,
    )
    assert result.decision != GovernanceDecision.ALLOW

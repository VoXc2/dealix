"""Doctrine: PII + external use ⇒ explicit approval required."""
from __future__ import annotations

import pytest

from auto_client_acquisition.data_os.source_passport import SourcePassport
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    decide,
)


def _make_passport(*, contains_pii: bool, external_use_allowed: bool) -> SourcePassport:
    return SourcePassport(
        source_id="src_001",
        source_type="crm_export",
        owner="acme",
        allowed_use=("internal_analysis", "external_outreach"),
        contains_pii=contains_pii,
        sensitivity="high" if contains_pii else "low",
        ai_access_allowed=True,
        external_use_allowed=external_use_allowed,
        retention_policy="90d",
    )


def test_pii_with_external_use_requires_approval() -> None:
    """PII + external_use_allowed=True must REQUIRE_APPROVAL (and explain why)."""
    passport = _make_passport(contains_pii=True, external_use_allowed=True)
    result = decide(
        action="send_external_message",
        context={
            "source_passport": passport,
            "contains_pii": True,
            "external_use": True,
        },
    )
    assert result.decision == GovernanceDecision.REQUIRE_APPROVAL
    assert len(result.reasons) > 0, "REQUIRE_APPROVAL must explain why"


def test_pii_internal_only_allowed() -> None:
    """PII used internally only may proceed at ALLOW_WITH_REVIEW level."""
    passport = _make_passport(contains_pii=True, external_use_allowed=False)
    result = decide(
        action="internal_analysis",
        context={
            "source_passport": passport,
            "contains_pii": True,
            "external_use": False,
            "declared_action": "internal_analysis",
        },
    )
    assert result.decision == GovernanceDecision.ALLOW_WITH_REVIEW

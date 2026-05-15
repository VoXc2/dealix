"""Governance intelligence — recurring blocks and rule creation signals."""

from __future__ import annotations

GOVERNANCE_INTELLIGENCE_SIGNALS: tuple[str, ...] = (
    "blocked_actions",
    "redactions",
    "approval_delays",
    "pii_flags",
    "source_passport_failures",
    "unsupported_claims",
    "channel_risks",
    "agent_permission_risks",
)


def governance_intelligence_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not GOVERNANCE_INTELLIGENCE_SIGNALS:
        return 0
    n = sum(1 for s in GOVERNANCE_INTELLIGENCE_SIGNALS if s in signals_tracked)
    return (n * 100) // len(GOVERNANCE_INTELLIGENCE_SIGNALS)

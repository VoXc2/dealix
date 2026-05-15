"""Governance workspace panel + per-output trust strip checklist."""

from __future__ import annotations

GOVERNANCE_PANEL_SIGNALS: tuple[str, ...] = (
    "outputs_allowed",
    "outputs_draft_only",
    "outputs_requiring_approval",
    "redactions_applied",
    "blocked_risks",
    "audit_events",
)

TRUST_OUTPUT_STRIP_SIGNALS: tuple[str, ...] = (
    "source_status",
    "governance_status",
    "pii_status",
    "approval_status",
    "qa_status",
    "proof_linkage",
)


def governance_panel_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not GOVERNANCE_PANEL_SIGNALS:
        return 0
    n = sum(1 for s in GOVERNANCE_PANEL_SIGNALS if s in signals_tracked)
    return (n * 100) // len(GOVERNANCE_PANEL_SIGNALS)


def trust_output_strip_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not TRUST_OUTPUT_STRIP_SIGNALS:
        return 0
    n = sum(1 for s in TRUST_OUTPUT_STRIP_SIGNALS if s in signals_tracked)
    return (n * 100) // len(TRUST_OUTPUT_STRIP_SIGNALS)

"""Compliance report — canonical section order for project/retainer summaries."""

from __future__ import annotations

COMPLIANCE_REPORT_SECTIONS: tuple[str, ...] = (
    "data_sources_used",
    "source_passport_status",
    "pii_detected",
    "redactions_applied",
    "ai_runs_logged",
    "governance_decisions",
    "approvals_requested",
    "approvals_completed",
    "external_actions_blocked_or_approved",
    "claims_supported_by_proof",
    "incidents",
    "recommendations",
)


def compliance_report_sections_complete(sections_present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [s for s in COMPLIANCE_REPORT_SECTIONS if s not in sections_present]
    return not missing, tuple(missing)

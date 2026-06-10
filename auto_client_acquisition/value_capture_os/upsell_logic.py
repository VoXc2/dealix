"""Proof-signal-driven upsell recommendations."""

from __future__ import annotations

from enum import StrEnum


class ProofCommercialSignal(StrEnum):
    DATA_ISSUES = "data_issues"
    FOLLOW_UP_GAPS = "follow_up_gaps"
    KNOWLEDGE_GAPS = "knowledge_gaps"
    POLICY_RISKS = "policy_risks"
    MANUAL_REPORTING = "manual_reporting"


_UPSELL_BY_SIGNAL: dict[str, str] = {
    ProofCommercialSignal.DATA_ISSUES: "data_readiness_retainer",
    ProofCommercialSignal.FOLLOW_UP_GAPS: "monthly_revops_os",
    ProofCommercialSignal.KNOWLEDGE_GAPS: "company_brain",
    ProofCommercialSignal.POLICY_RISKS: "monthly_governance",
    ProofCommercialSignal.MANUAL_REPORTING: "executive_reporting_automation",
}


def upsell_from_proof_signal(signal: str) -> str | None:
    """Map a proof narrative signal to a commercial upsell offer slug."""
    return _UPSELL_BY_SIGNAL.get(signal)

"""Client OS surface signals → next commercial move (retainer / upsell)."""

from __future__ import annotations

from enum import StrEnum


class ClientExpansionSignal(StrEnum):
    LOW_DATA_READINESS = "low_data_readiness"
    HIGH_GOVERNANCE_RISKS = "high_governance_risks"
    HEAVY_DRAFT_PACK_USAGE = "heavy_draft_pack_usage"
    KNOWLEDGE_GAPS = "knowledge_gaps"
    RECURRING_MANUAL_REPORTS = "recurring_manual_reports"


_RECOMMENDATION: dict[str, str] = {
    ClientExpansionSignal.LOW_DATA_READINESS: "data_readiness_retainer",
    ClientExpansionSignal.HIGH_GOVERNANCE_RISKS: "monthly_governance",
    ClientExpansionSignal.HEAVY_DRAFT_PACK_USAGE: "monthly_revops_os",
    ClientExpansionSignal.KNOWLEDGE_GAPS: "company_brain",
    ClientExpansionSignal.RECURRING_MANUAL_REPORTS: "executive_reporting_automation",
}


def client_expansion_recommendation(signal: str) -> str | None:
    """Map a Client OS health / usage signal to a commercial next step slug."""
    return _RECOMMENDATION.get(signal)

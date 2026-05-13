"""Client OS expansion engine — signal → next offer."""

from __future__ import annotations


EXPANSION_SIGNALS: dict[str, str] = {
    "weak_data_readiness": "Data Readiness Retainer",
    "high_governance_risk": "Monthly Governance",
    "draft_pack_used_repeatedly": "Monthly RevOps OS",
    "knowledge_gaps": "Company Brain",
    "repeated_reports": "Executive Reporting Automation",
}


def expansion_offer_for(signal: str) -> str | None:
    return EXPANSION_SIGNALS.get(signal)

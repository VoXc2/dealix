from __future__ import annotations

from .schemas import LeadCompany


def suppression_reasons(lead: LeadCompany) -> list[str]:
    reasons: list[str] = []
    if lead.metadata.get("suppressed"):
        reasons.append("suppression_list_hit")
    if lead.metadata.get("opt_out"):
        reasons.append("opt_out")
    return reasons
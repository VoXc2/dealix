from __future__ import annotations

from .schemas import LeadCompany


def deliverability_risk_score(lead: LeadCompany) -> int:
    risk = 15
    if not lead.domain:
        risk += 20
    if lead.metadata.get("bounce_history"):
        risk += 35
    if lead.metadata.get("missing_spf"):
        risk += 10
    if lead.metadata.get("missing_dkim"):
        risk += 10
    if lead.metadata.get("missing_dmarc"):
        risk += 10
    if lead.metadata.get("daily_cap_exceeded"):
        risk += 20
    return min(risk, 100)
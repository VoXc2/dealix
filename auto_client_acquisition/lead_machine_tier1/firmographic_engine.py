from __future__ import annotations

from .schemas import LeadCompany


def firmographic_score(lead: LeadCompany) -> int:
    score = 0
    if lead.sector in {"agencies", "B2B services", "consulting", "real estate", "logistics", "hospitality", "clinics", "SaaS", "restaurants", "construction", "retail"}:
        score += 35
    if lead.city:
        score += 15
    if lead.employee_band:
        score += 20
    if lead.domain or lead.website_url:
        score += 15
    if lead.country == "SA":
        score += 15
    return min(score, 100)
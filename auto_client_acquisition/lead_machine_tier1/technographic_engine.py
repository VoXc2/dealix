from __future__ import annotations

from .schemas import LeadCompany


def technographic_score(lead: LeadCompany) -> int:
    metadata = lead.metadata
    score = 0
    if metadata.get("crm_installed"):
        score += 25
    if metadata.get("ecommerce_platform"):
        score += 25
    if metadata.get("payment_provider"):
        score += 20
    if metadata.get("ads_pixel"):
        score += 15
    if metadata.get("booking_link"):
        score += 15
    return min(score, 100)
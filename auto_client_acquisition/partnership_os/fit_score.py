"""V12 Partnership OS — pure-function partner fit score (0–100)."""
from __future__ import annotations

from auto_client_acquisition.partnership_os.partner_profile import Partner


def compute_fit_score(
    *,
    partner: Partner,
    customer_segment: str,
    serves_b2b: bool = True,
    has_existing_customers: bool = True,
    saudi_market_focus: bool = True,
) -> int:
    """Heuristic 0–100. Pure function. NO LLM."""
    score = 0
    type_weights = {
        "marketing_agency": 25,
        "sales_consultant": 30,
        "crm_implementer": 30,
        "hubspot_freelancer": 25,
        "zoho_freelancer": 25,
        "tech_partner_for_smes": 25,
        "consulting_firm": 20,
    }
    score += type_weights.get(partner.partner_type, 15)
    if serves_b2b:
        score += 20
    if has_existing_customers:
        score += 25
    if saudi_market_focus:
        score += 15
    if partner.region.lower() in {"riyadh", "jeddah", "dammam", "eastern", "ksa"}:
        score += 10
    if (
        customer_segment.lower() == "b2b_services"
        and partner.partner_type in {"sales_consultant", "marketing_agency"}
    ):
        score += 5  # alignment bonus
    return max(0, min(100, score))

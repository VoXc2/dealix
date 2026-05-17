"""Affiliate OS — pure-function affiliate fit score (0-100). NO LLM."""

from __future__ import annotations

from auto_client_acquisition.affiliate_os.affiliate_profile import AffiliateApplication

_TYPE_WEIGHTS = {
    "content_creator": 20,
    "agency": 28,
    "consultant": 28,
    "newsletter": 25,
    "community_operator": 25,
    "saas_reseller": 22,
}
_KSA_REGIONS = {"riyadh", "jeddah", "dammam", "eastern", "ksa", "saudi arabia"}


def compute_affiliate_fit_score(
    *,
    application: AffiliateApplication,
    customer_segment: str = "b2b_services",
) -> int:
    """Heuristic 0-100. Pure function — deterministic, no I/O."""
    score = _TYPE_WEIGHTS.get(application.affiliate_type, 15)
    if application.serves_b2b:
        score += 20
    if application.has_existing_audience:
        score += 25
    if application.saudi_market_focus:
        score += 15
    if application.region.lower() in _KSA_REGIONS:
        score += 10
    if (
        customer_segment.lower() == "b2b_services"
        and application.affiliate_type in {"agency", "consultant", "newsletter"}
    ):
        score += 5  # alignment bonus
    return max(0, min(100, score))


__all__ = ["compute_affiliate_fit_score"]

from __future__ import annotations

from .schemas import EnrichmentResult, LeadCompany


PROVIDERS = (
    "internal_graph",
    "customer_crm",
    "uploaded_csv",
    "google_places",
    "apollo",
    "clearbit",
    "hunter",
    "builtwith",
    "wappalyzer",
    "manual_research",
)


def run_enrichment_waterfall(lead: LeadCompany, configured_providers: set[str] | None = None, confidence_threshold: float = 0.8) -> list[EnrichmentResult]:
    configured = configured_providers or {"internal_graph", "uploaded_csv", "manual_research"}
    results: list[EnrichmentResult] = []
    current_confidence = 0.2
    for provider in PROVIDERS:
        is_configured = provider in configured
        if not is_configured:
            results.append(EnrichmentResult(provider=provider, configured=False, confidence=current_confidence, status="not_configured", reason="provider_not_configured"))
            continue
        fields = {}
        if provider == "internal_graph":
            fields = {"account_graph": True, "contact_graph": True}
            current_confidence = max(current_confidence, 0.55)
        elif provider == "uploaded_csv":
            fields = {"uploaded_match": bool(lead.domain or lead.company_name)}
            current_confidence = max(current_confidence, 0.65)
        elif provider == "google_places":
            fields = {"google_place_id": lead.google_place_id}
            current_confidence = max(current_confidence, 0.7)
        elif provider == "manual_research":
            fields = {"manual_review_required": True}
            current_confidence = max(current_confidence, 0.82)
        else:
            fields = {"adapter_optional": True}
            current_confidence = max(current_confidence, 0.72)
        results.append(EnrichmentResult(provider=provider, configured=True, confidence=current_confidence, fields=fields))
        if current_confidence >= confidence_threshold:
            break
    return results
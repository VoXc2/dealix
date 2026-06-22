from __future__ import annotations

from .schemas import DedupeResult, LeadCompany


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def dedupe_lead(lead: LeadCompany, existing_records: list[LeadCompany]) -> DedupeResult:
    for existing in existing_records:
        matched_keys: list[str] = []
        if _normalize(lead.domain) and _normalize(lead.domain) == _normalize(existing.domain):
            matched_keys.append("exact_domain")
        if _normalize(lead.phone) and _normalize(lead.phone) == _normalize(existing.phone):
            matched_keys.append("normalized_phone")
        if _normalize(lead.google_place_id) and _normalize(lead.google_place_id) == _normalize(existing.google_place_id):
            matched_keys.append("google_place_id")
        if _normalize(lead.website_url) and _normalize(lead.website_url) == _normalize(existing.website_url):
            matched_keys.append("website_url")
        if _normalize(lead.crm_external_id) and _normalize(lead.crm_external_id) == _normalize(existing.crm_external_id):
            matched_keys.append("crm_external_id")
        if _normalize(lead.email) and _normalize(lead.email).split("@")[-1] == _normalize(existing.email).split("@")[-1]:
            matched_keys.append("email_domain")
        if _normalize(lead.company_name) == _normalize(existing.company_name) and _normalize(lead.city) == _normalize(existing.city):
            matched_keys.append("company_city")
        if matched_keys:
            confidence = min(1.0, 0.45 + (0.12 * len(matched_keys)))
            return DedupeResult(duplicate_of=existing.domain or existing.company_name, confidence=confidence, merge_recommendation="merge_after_review" if confidence < 0.8 else "safe_merge", safe_merge=confidence >= 0.8, matched_keys=matched_keys)
    return DedupeResult(duplicate_of=None, confidence=0.0, merge_recommendation="new_record", safe_merge=False, matched_keys=[])
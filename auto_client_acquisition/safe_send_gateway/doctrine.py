"""Doctrine non-negotiable checks for governed commercial paths (fail-fast helpers).

Used by Revenue Intelligence draft/finalize surfaces. Returns structured bilingual
reasons suitable for HTTP 403 payloads — does not send messages or charge cards.

The seven boolean guards below stay in Python and are authoritative. Reason text
is sourced from ``policy_config/claim_policy.yaml`` — config may add codes or
reword reasons, it can never remove a guard (enforced by ``_BASE_CODES`` below).
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.policy_config.loader import load_policy

# The seven doctrine codes that MUST always be present. config can extend, not shrink.
_BASE_CODES = (
    "no_cold_whatsapp",
    "no_linkedin_automation",
    "no_scraping",
    "no_bulk_outreach",
    "no_guaranteed_sales_claims",
    "no_fake_proof",
    "external_action_requires_approval",
)


def _doctrine_reasons() -> dict[str, dict[str, str]]:
    codes = load_policy("claim_policy").get("codes") or {}
    missing = [c for c in _BASE_CODES if c not in codes]
    if missing:
        msg = f"doctrine_codes_missing:{','.join(missing)}"
        raise ValueError(msg)
    return {
        code: {"ar": str(spec.get("ar", "")), "en": str(spec.get("en", ""))}
        for code, spec in codes.items()
    }


def doctrine_violations_for_revenue_intelligence(
    *,
    request_cold_whatsapp: bool = False,
    request_linkedin_automation: bool = False,
    request_scraping: bool = False,
    request_bulk_outreach: bool = False,
    request_guaranteed_sales_claim: bool = False,
    request_fake_proof: bool = False,
    request_external_send_without_approval: bool = False,
) -> tuple[tuple[str, ...], dict[str, dict[str, str]]]:
    """Return (violation_codes, reasons_by_code with ar/en)."""
    reasons = _doctrine_reasons()
    hits: list[str] = []
    if request_cold_whatsapp:
        hits.append("no_cold_whatsapp")
    if request_linkedin_automation:
        hits.append("no_linkedin_automation")
    if request_scraping:
        hits.append("no_scraping")
    if request_bulk_outreach:
        hits.append("no_bulk_outreach")
    if request_guaranteed_sales_claim:
        hits.append("no_guaranteed_sales_claims")
    if request_fake_proof:
        hits.append("no_fake_proof")
    if request_external_send_without_approval:
        hits.append("external_action_requires_approval")
    return tuple(hits), {k: reasons[k] for k in hits if k in reasons}


def enforce_doctrine_non_negotiables(
    *,
    request_cold_whatsapp: bool = False,
    request_linkedin_automation: bool = False,
    request_scraping: bool = False,
    request_bulk_outreach: bool = False,
    request_guaranteed_sales_claim: bool = False,
    request_fake_proof: bool = False,
    request_external_send_without_approval: bool = False,
) -> None:
    """Raise ValueError with bilingual detail dict if any doctrine line is crossed.

    Routers map ValueError → HTTP 403.
    """
    codes, reasons = doctrine_violations_for_revenue_intelligence(
        request_cold_whatsapp=request_cold_whatsapp,
        request_linkedin_automation=request_linkedin_automation,
        request_scraping=request_scraping,
        request_bulk_outreach=request_bulk_outreach,
        request_guaranteed_sales_claim=request_guaranteed_sales_claim,
        request_fake_proof=request_fake_proof,
        request_external_send_without_approval=request_external_send_without_approval,
    )
    if not codes:
        return
    detail: dict[str, Any] = {
        "doctrine_violations": list(codes),
        "reasons": reasons,
    }
    raise ValueError(str(detail))

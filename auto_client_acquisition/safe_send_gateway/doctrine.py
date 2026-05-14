"""Doctrine non-negotiable checks for governed commercial paths (fail-fast helpers).

Used by Revenue Intelligence draft/finalize surfaces. Returns structured bilingual
reasons suitable for HTTP 403 payloads — does not send messages or charge cards.
"""

from __future__ import annotations

from typing import Any


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
    reasons: dict[str, dict[str, str]] = {
        "no_cold_whatsapp": {
            "ar": "ممنوع واتساب بارد أو أتمتة واتساب باردة — مسودات فقط مع موافقة.",
            "en": "Cold WhatsApp / WhatsApp automation is forbidden — draft-only with approval.",
        },
        "no_linkedin_automation": {
            "ar": "ممنوع أتمتة LinkedIn — مسودات فقط.",
            "en": "LinkedIn automation is forbidden — draft-only.",
        },
        "no_scraping": {
            "ar": "ممنوع scraping أو جمع ويب غير مصرّح.",
            "en": "Scraping / unauthorized web collection is forbidden.",
        },
        "no_bulk_outreach": {
            "ar": "ممنوع تواصل جماعي خارجي بدون موافقة وحوكمة.",
            "en": "Bulk external outreach without governance approval is forbidden.",
        },
        "no_guaranteed_sales_claims": {
            "ar": "ممنوع وعود مبيعات مضمونة.",
            "en": "Guaranteed sales claims are forbidden.",
        },
        "no_fake_proof": {
            "ar": "ممنوع إثبات مزيّف أو أرقام مخترعة.",
            "en": "Fake proof / invented metrics is forbidden.",
        },
        "external_action_requires_approval": {
            "ar": "أي إرسال خارجي يتطلب موافقة صريحة — لا تنفيذ تلقائي.",
            "en": "External sends require explicit approval — no autonomous execution.",
        },
    }
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

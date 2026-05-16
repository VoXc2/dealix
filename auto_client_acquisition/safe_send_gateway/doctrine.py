"""Doctrine non-negotiable checks for governed commercial paths (fail-fast helpers).

Single source of truth for Dealix's 11 non-negotiables. Used by Revenue
Intelligence draft/finalize surfaces and the enterprise loop. Returns structured
bilingual reasons suitable for HTTP 403 payloads — does not send messages or
charge cards.

The 11 canonical non-negotiables (see docs/00_constitution/NON_NEGOTIABLES.md):
  1. No scraping systems.
  2. No cold WhatsApp automation.
  3. No LinkedIn automation.
  4. No fake / un-sourced claims.
  5. No guaranteed sales outcomes.
  6. No PII in logs.
  7. No source-less knowledge answers.
  8. No external action without approval.
  9. No agent without identity.
 10. No project without Proof Pack.
 11. No project without Capital Asset.

`no_bulk_outreach` is enforced as an operational extension of #8.
"""

from __future__ import annotations

from typing import Any

# Bilingual reason registry. Keys are stable violation codes; never rename
# without updating callers, tests, and the constitution doc.
DOCTRINE_REASONS: dict[str, dict[str, str]] = {
    "no_scraping": {
        "ar": "ممنوع scraping أو جمع ويب غير مصرّح.",
        "en": "Scraping / unauthorized web collection is forbidden.",
    },
    "no_cold_whatsapp": {
        "ar": "ممنوع واتساب بارد أو أتمتة واتساب باردة — مسودات فقط مع موافقة.",
        "en": "Cold WhatsApp / WhatsApp automation is forbidden — draft-only with approval.",
    },
    "no_linkedin_automation": {
        "ar": "ممنوع أتمتة LinkedIn — مسودات فقط.",
        "en": "LinkedIn automation is forbidden — draft-only.",
    },
    "no_fake_proof": {
        "ar": "ممنوع إثبات مزيّف أو أرقام مخترعة أو ادعاءات بلا مصدر.",
        "en": "Fake proof / invented metrics / un-sourced claims are forbidden.",
    },
    "no_guaranteed_sales_claims": {
        "ar": "ممنوع وعود مبيعات مضمونة.",
        "en": "Guaranteed sales claims are forbidden.",
    },
    "no_pii_in_logs": {
        "ar": "ممنوع تسجيل بيانات شخصية (PII) في السجلات.",
        "en": "Writing PII to logs is forbidden.",
    },
    "no_sourceless_answer": {
        "ar": "ممنوع إجابة معرفية بلا مصدر موثّق.",
        "en": "Knowledge answers without a cited source are forbidden.",
    },
    "external_action_requires_approval": {
        "ar": "أي إرسال خارجي يتطلب موافقة صريحة — لا تنفيذ تلقائي.",
        "en": "External sends require explicit approval — no autonomous execution.",
    },
    "no_agent_without_identity": {
        "ar": "ممنوع تشغيل وكيل بلا هوية مُعرّفة ومُسجّلة.",
        "en": "No agent may run without a registered identity.",
    },
    "no_project_without_proof_pack": {
        "ar": "ممنوع إغلاق مشروع بلا Proof Pack.",
        "en": "No project may close without a Proof Pack.",
    },
    "no_project_without_capital_asset": {
        "ar": "ممنوع إغلاق مشروع بلا أصل رأسمالي مُسجّل.",
        "en": "No project may close without a registered Capital Asset.",
    },
    "no_bulk_outreach": {
        "ar": "ممنوع تواصل جماعي خارجي بدون موافقة وحوكمة.",
        "en": "Bulk external outreach without governance approval is forbidden.",
    },
}


def doctrine_violations_for_revenue_intelligence(
    *,
    request_scraping: bool = False,
    request_cold_whatsapp: bool = False,
    request_linkedin_automation: bool = False,
    request_fake_proof: bool = False,
    request_guaranteed_sales_claim: bool = False,
    request_pii_in_logs: bool = False,
    request_sourceless_answer: bool = False,
    request_external_send_without_approval: bool = False,
    request_agent_without_identity: bool = False,
    request_project_without_proof_pack: bool = False,
    request_project_without_capital_asset: bool = False,
    request_bulk_outreach: bool = False,
) -> tuple[tuple[str, ...], dict[str, dict[str, str]]]:
    """Return (violation_codes, reasons_by_code with ar/en)."""
    checks: tuple[tuple[bool, str], ...] = (
        (request_scraping, "no_scraping"),
        (request_cold_whatsapp, "no_cold_whatsapp"),
        (request_linkedin_automation, "no_linkedin_automation"),
        (request_fake_proof, "no_fake_proof"),
        (request_guaranteed_sales_claim, "no_guaranteed_sales_claims"),
        (request_pii_in_logs, "no_pii_in_logs"),
        (request_sourceless_answer, "no_sourceless_answer"),
        (request_external_send_without_approval, "external_action_requires_approval"),
        (request_agent_without_identity, "no_agent_without_identity"),
        (request_project_without_proof_pack, "no_project_without_proof_pack"),
        (request_project_without_capital_asset, "no_project_without_capital_asset"),
        (request_bulk_outreach, "no_bulk_outreach"),
    )
    hits = tuple(code for triggered, code in checks if triggered)
    return hits, {code: DOCTRINE_REASONS[code] for code in hits}


def enforce_doctrine_non_negotiables(
    *,
    request_scraping: bool = False,
    request_cold_whatsapp: bool = False,
    request_linkedin_automation: bool = False,
    request_fake_proof: bool = False,
    request_guaranteed_sales_claim: bool = False,
    request_pii_in_logs: bool = False,
    request_sourceless_answer: bool = False,
    request_external_send_without_approval: bool = False,
    request_agent_without_identity: bool = False,
    request_project_without_proof_pack: bool = False,
    request_project_without_capital_asset: bool = False,
    request_bulk_outreach: bool = False,
) -> None:
    """Raise ValueError with bilingual detail dict if any doctrine line is crossed.

    Routers map ValueError -> HTTP 403.
    """
    codes, reasons = doctrine_violations_for_revenue_intelligence(
        request_scraping=request_scraping,
        request_cold_whatsapp=request_cold_whatsapp,
        request_linkedin_automation=request_linkedin_automation,
        request_fake_proof=request_fake_proof,
        request_guaranteed_sales_claim=request_guaranteed_sales_claim,
        request_pii_in_logs=request_pii_in_logs,
        request_sourceless_answer=request_sourceless_answer,
        request_external_send_without_approval=request_external_send_without_approval,
        request_agent_without_identity=request_agent_without_identity,
        request_project_without_proof_pack=request_project_without_proof_pack,
        request_project_without_capital_asset=request_project_without_capital_asset,
        request_bulk_outreach=request_bulk_outreach,
    )
    if not codes:
        return
    detail: dict[str, Any] = {
        "doctrine_violations": list(codes),
        "reasons": reasons,
    }
    raise ValueError(str(detail))

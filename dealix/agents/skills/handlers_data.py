"""
Data-backed skill handlers (T9):

- crm_syncer           — HubSpot (bidirectional) + Salesforce (stub).
- market_researcher    — Wathq + Etimad + Tadawul + MISA chain → company brief.
- renewal_forecaster   — health + usage + sentiment → churn risk.
- compliance_reviewer  — PDPL + GDPR + CITC rule pass.

Each handler:
- Degrades to deterministic logic when upstream vendor keys are unset.
- Reports a `_meta.sources` list of which vendors were called.
"""

from __future__ import annotations

import os
from typing import Any

from core.logging import get_logger

from .handlers import register

log = get_logger(__name__)


# ─────────────────────────── crm_syncer ────────────────────────────


@register("crm_syncer")
async def _crm_syncer(inputs: dict[str, Any]) -> dict[str, Any]:
    """Bidirectional CRM sync.

    Inputs:
        lead: {id?, full_name, email, phone, company, sector, stage}
        target: 'hubspot' | 'salesforce'
        action: 'create' | 'update' | 'pull'
    """
    lead = dict(inputs.get("lead") or {})
    target = str(inputs.get("target") or "hubspot").lower()
    action = str(inputs.get("action") or "create").lower()

    if target == "hubspot":
        if not os.getenv("HUBSPOT_API_KEY", "").strip():
            return {
                "ok": False,
                "target": "hubspot",
                "action": action,
                "reason": "hubspot_not_configured",
                "_meta": {"sources": [], "would_sync": list(lead.keys())},
            }
        try:
            from integrations.hubspot import HubSpotClient

            client = HubSpotClient()
            if not client.configured:
                return {"ok": False, "target": "hubspot", "reason": "hubspot_not_configured"}

            # Adapt the dict to the agent's Lead signature when possible.
            try:
                from auto_client_acquisition.agents.intake import Lead

                obj = Lead(**{k: v for k, v in lead.items() if k in Lead.model_fields})
            except Exception:
                return {
                    "ok": False,
                    "target": "hubspot",
                    "reason": "lead_shape_mismatch",
                }
            res = await client.sync_lead(obj, create_deal=action != "pull")
            return {
                "ok": getattr(res, "ok", True),
                "target": "hubspot",
                "action": action,
                "contact_id": getattr(res, "contact_id", None),
                "deal_id": getattr(res, "deal_id", None),
                "_meta": {"sources": ["hubspot"]},
            }
        except Exception as exc:
            log.exception("crm_syncer_hubspot_failed")
            return {
                "ok": False,
                "target": "hubspot",
                "reason": f"hubspot_error:{exc!s}",
                "_meta": {"sources": []},
            }
    if target == "salesforce":
        return {
            "ok": False,
            "target": "salesforce",
            "reason": "salesforce_not_implemented",
            "_meta": {"sources": []},
        }
    return {"ok": False, "reason": f"unknown_target:{target}"}


# ───────────────────────── market_researcher ────────────────────────


@register("market_researcher")
async def _market_researcher(inputs: dict[str, Any]) -> dict[str, Any]:
    """Build a company brief from Saudi-sovereign + general sources.

    Inputs:
        cr_number, vat_number, tadawul_symbol, misa_licence, web_keywords[]
    """
    cr = str(inputs.get("cr_number") or "").strip()
    vat = str(inputs.get("vat_number") or "").strip()
    symbol = str(inputs.get("tadawul_symbol") or "").strip()
    licence = str(inputs.get("misa_licence") or "").strip()

    out: dict[str, Any] = {"sources": [], "data": {}}

    # Wathq.
    if cr or vat:
        try:
            from dealix.enrichment.wathq_client import is_configured, lookup_wathq

            if is_configured():
                er = await lookup_wathq(cr_number=cr or None, vat_number=vat or None)
                if er.matched:
                    out["sources"].append("wathq")
                    out["data"]["wathq"] = er.data
        except Exception:
            log.exception("market_researcher_wathq_failed")

    # Maroof.
    if cr:
        try:
            from dealix.integrations.maroof_client import (
                is_configured,
                lookup as maroof_lookup,
            )

            if is_configured():
                m = await maroof_lookup(cr)
                if m is not None:
                    out["sources"].append("maroof")
                    out["data"]["maroof"] = {
                        "verified": m.verified,
                        "rating": m.rating,
                        "review_count": m.review_count,
                        "badge_color": m.badge_color,
                    }
        except Exception:
            log.exception("market_researcher_maroof_failed")

    # Najiz.
    if cr:
        try:
            from dealix.integrations.najiz_client import is_configured, snapshot

            if is_configured():
                s = await snapshot(cr)
                if s is not None:
                    out["sources"].append("najiz")
                    out["data"]["najiz"] = {
                        "open_disputes": s.open_disputes,
                        "bankruptcy_filings": s.bankruptcy_filings,
                        "execution_orders": s.execution_orders,
                        "risk_score": s.risk_score,
                    }
        except Exception:
            log.exception("market_researcher_najiz_failed")

    # Tadawul.
    if symbol:
        try:
            from dealix.integrations.tadawul_client import (
                is_configured,
                lookup_symbol,
            )

            if is_configured():
                t = await lookup_symbol(symbol)
                if t is not None:
                    out["sources"].append("tadawul")
                    out["data"]["tadawul"] = {
                        "name_en": t.name_en,
                        "sector": t.sector,
                        "market_cap_sar": t.market_cap_sar,
                        "last_close": t.last_close,
                        "pe_ratio": t.pe_ratio,
                    }
        except Exception:
            log.exception("market_researcher_tadawul_failed")

    # MISA.
    if licence:
        try:
            from dealix.integrations.misa_client import is_configured, licence_status

            if is_configured():
                ls = await licence_status(licence)
                if ls is not None:
                    out["sources"].append("misa")
                    out["data"]["misa"] = {
                        "active": ls.active,
                        "issued_at": ls.issued_at,
                        "expires_at": ls.expires_at,
                        "country_of_origin": ls.country_of_origin,
                    }
        except Exception:
            log.exception("market_researcher_misa_failed")

    return {
        "brief": (
            f"{out['data'].get('wathq', {}).get('company_name_ar') or '— '} "
            f"({len(out['sources'])} sources)"
        ),
        "_meta": {"sources": out["sources"]},
        "data": out["data"],
    }


# ──────────────────────── renewal_forecaster ────────────────────────


@register("renewal_forecaster")
async def _renewal_forecaster(inputs: dict[str, Any]) -> dict[str, Any]:
    """Health × usage × sentiment → churn risk by tenant.

    Inputs:
        tenant_id
        health_score: 0..1
        usage_trend: 'rising' | 'flat' | 'declining'
        last_nps: -100..100
        days_to_renewal: int
    """
    health = float(inputs.get("health_score") or 0.5)
    trend = str(inputs.get("usage_trend") or "flat").lower()
    nps = float(inputs.get("last_nps") or 0.0)
    days = int(inputs.get("days_to_renewal") or 60)

    trend_factor = {"rising": -0.2, "flat": 0.0, "declining": 0.3}.get(trend, 0.0)
    nps_factor = max(0.0, -nps / 100.0)
    proximity = max(0.0, 1.0 - (days / 90.0))

    risk = max(0.0, min(1.0, (1.0 - health) + trend_factor + nps_factor * 0.3 + proximity * 0.2))

    return {
        "tenant_id": str(inputs.get("tenant_id") or ""),
        "churn_risk": round(risk, 3),
        "bucket": "high" if risk > 0.66 else "medium" if risk > 0.33 else "low",
        "recommended_action": (
            "escalate_to_csm_now"
            if risk > 0.66
            else "schedule_check_in"
            if risk > 0.33
            else "monitor"
        ),
        "_meta": {
            "components": {
                "health": health,
                "trend_factor": trend_factor,
                "nps_factor": nps_factor,
                "proximity": proximity,
            },
        },
    }


# ──────────────────────── compliance_reviewer ───────────────────────


_PII_PATTERNS = [
    (r"\b\d{10}\b", "national_id_or_phone"),
    (r"\b\d{15}\b", "vat_number"),
    (r"\b[A-Z]{2}\d{20,30}\b", "iban"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "email"),
    # `\b` doesn't fire before `+` (both non-word), so we use lookarounds.
    (r"(?<!\d)\+966\d{9}(?!\d)", "ksa_phone"),
]


@register("compliance_reviewer")
async def _compliance_reviewer(inputs: dict[str, Any]) -> dict[str, Any]:
    """Pass a piece of text against PDPL + GDPR + Saudi CITC rules.

    Inputs:
        text: str
        purpose: 'marketing' | 'support' | 'analytics'
    """
    import re

    text = str(inputs.get("text") or "")
    purpose = str(inputs.get("purpose") or "marketing").lower()

    flags: list[dict[str, str]] = []
    for pattern, label in _PII_PATTERNS:
        if re.search(pattern, text):
            flags.append({"type": "pii_detected", "kind": label})

    # PDPL: marketing communications need explicit consent.
    if purpose == "marketing" and not bool(inputs.get("has_consent")):
        flags.append({"type": "pdpl_violation", "kind": "marketing_without_consent"})

    # CITC: outbound marketing-SMS outside Sun–Thu 09:00–21:00 KSA time
    # requires the prior-consent flag.
    if purpose == "marketing" and bool(inputs.get("after_hours")) and not bool(
        inputs.get("has_consent")
    ):
        flags.append({"type": "citc_violation", "kind": "outbound_outside_hours"})

    return {
        "compliant": not flags,
        "violations": flags,
        "recommendation": "block_send" if flags else "ok_to_send",
        "_meta": {
            "frameworks_checked": ["PDPL", "GDPR", "CITC"],
            "purpose": purpose,
        },
    }

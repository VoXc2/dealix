"""Commercial Map — Wave 14J.

Single source of truth that maps every Dealix offer to:
  - landing page path
  - intake endpoint
  - checkout flow (URL + tier query)
  - delivery module / endpoint
  - proof / report endpoint
  - founder dashboard surface
  - non-negotiables (hard_gates) honored by code

Reads from `auto_client_acquisition.service_catalog.registry.OFFERINGS`
so the map can never drift from the canonical registry (5 ladder rungs
+ 1 Agency Partner channel).

Endpoints:
  GET /api/v1/commercial-map           → JSON
  GET /api/v1/commercial-map/markdown  → bilingual AR+EN markdown
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.service_catalog.registry import OFFERINGS


router = APIRouter(prefix="/api/v1/commercial-map", tags=["commercial-map"])


# Per-service wiring overlays (landing + endpoints).
# Keys MUST match `auto_client_acquisition.service_catalog.registry` ids.
_WIRING: dict[str, dict[str, Any]] = {
    "free_diagnostic": {
        "landing_url": "/diagnostic.html",
        "intake_endpoint": "POST /api/v1/company-growth-beast/diagnostic",
        "lead_capture_endpoint": "POST /api/v1/public/demo-request",
        "checkout_url": None,
        "checkout_endpoint": None,
        "delivery_module": "founder reviews via /api/v1/founder/leads",
        "delivery_endpoint": "GET /api/v1/founder/leads",
        "proof_endpoint": "auto_client_acquisition/email/transactional.send_transactional(kind=diagnostic_intake_confirmation)",
        "founder_surface": "/founder-leads.html",
        "next_offer": "sprint",
    },
    "sprint": {
        "landing_url": "/start.html",
        "preview_url": "/sprint-sample.html",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "/checkout.html?tier=sprint",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.delivery_factory.delivery_sprint.run_sprint",
        "delivery_endpoint": "POST /api/v1/sprint/run",
        "sample_endpoint": "GET /api/v1/sprint/sample",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "case_safe_endpoint": "GET /api/v1/proof-to-market/case-safe/{engagement_id}",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "pilot",
    },
    "pilot": {
        "landing_url": "/pricing.html#pilot",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "/checkout.html?tier=pilot",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.delivery_factory.delivery_sprint + scripts/weekly_brief_runner.py",
        "delivery_endpoint": "POST /api/v1/sprint/run",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "retainer_managed_ops",
    },
    "retainer_managed_ops": {
        "landing_url": "/pricing.html#retainer",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "/checkout.html?tier=retainer",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "scripts/weekly_brief_runner.py + scripts/monthly_cadence_runner.py",
        "delivery_endpoint": "GET /api/v1/customer-portal/{handle}/workspace",
        "proof_endpoint": "GET /api/v1/value/{handle}/report/monthly",
        "adoption_endpoint": "GET /api/v1/customer-success/{handle}/adoption-score",
        "renewal_module": "auto_client_acquisition.payment_ops.renewal_scheduler",
        "founder_surface": "/customer-portal.html?handle={customer}",
        "next_offer": "enterprise_custom_ai",
    },
    "enterprise_custom_ai": {
        "landing_url": "/pricing.html#enterprise",
        "intake_endpoint": "POST /api/v1/service-setup/requests",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.executive_command_center + custom SOW build",
        "delivery_endpoint": "GET /api/v1/executive-command-center/*",
        "proof_endpoint": "GET /api/v1/audit/{handle}/control-graph/markdown",
        "trust_pack_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "agency_partner_os": {
        "landing_url": "/agency-partner.html",
        "intake_endpoint": "POST /api/v1/public/partner-application",
        "checkout_url": "founder-issued",
        "checkout_endpoint": None,
        "delivery_module": "auto_client_acquisition.partnership_os.referral_store",
        "delivery_endpoint": "POST /api/v1/referrals/create + /redeem + /{code}/convert",
        "proof_endpoint": "GET /api/v1/founder/dashboard",
        "covenant_doc": "docs/40_partners/PARTNER_COVENANT.md",
        "founder_surface": "/founder-leads.html",
        "next_offer": None,
    },
}


_OFFER_NOTES = {
    "free_diagnostic": (
        "Rung 1. Free 48h bilingual diagnostic — opens the funnel. Confirmation "
        "email auto-sent. Founder reviews every intake within 48h."
    ),
    "sprint": (
        "Rung 2. First paid offer — 2,500 SAR. 10 working days. Proof Pack "
        "mandatory. Absorbs the data-cleaning scope. 14-day full refund."
    ),
    "pilot": (
        "Rung 3. 9,500 SAR. 30-day operating pilot — 4 weekly pipeline cycles "
        "with executive reports and a closing Proof Pack."
    ),
    "retainer_managed_ops": (
        "Rung 4. 6,000–18,000 SAR / month retainer engine. Monthly operating "
        "cadence with weekly audits, support insights, and a board pack at the "
        "upper band. Renewal after confirmed cycles."
    ),
    "enterprise_custom_ai": (
        "Rung 5. 45,000–120,000 SAR. Custom AI build + governance program. "
        "Scope, milestones, and refunds fixed in a signed SOW."
    ),
    "agency_partner_os": (
        "Channel offer. 5K SAR / closed deal + 30% commission first year. "
        "Partner Covenant enforced: no unsafe automation, no guaranteed claims."
    ),
}


def _offer_to_dict(offering, wiring: dict[str, Any], notes: str) -> dict[str, Any]:
    return {
        "service_id": offering.id,
        "name_ar": offering.name_ar,
        "name_en": offering.name_en,
        "price_sar": offering.price_sar,
        "price_sar_min": offering.price_sar_min,
        "price_sar_max": offering.price_sar_max,
        "price_display_ar": offering.price_display_ar,
        "price_display_en": offering.price_display_en,
        "price_unit": offering.price_unit,
        "is_rung": bool(offering.is_rung),
        "duration_days": offering.duration_days,
        "customer_journey_stage": str(offering.customer_journey_stage),
        "kpi_commitment_ar": offering.kpi_commitment_ar,
        "kpi_commitment_en": offering.kpi_commitment_en,
        "refund_policy_ar": offering.refund_policy_ar,
        "refund_policy_en": offering.refund_policy_en,
        "deliverables": list(offering.deliverables),
        "action_modes_used": [str(m) for m in offering.action_modes_used],
        "non_negotiables_enforced": list(offering.hard_gates),
        "is_estimate": bool(offering.is_estimate),
        "wiring": dict(wiring),
        "notes": notes,
    }


def _build_payload() -> dict[str, Any]:
    offers: list[dict[str, Any]] = []
    for offering in OFFERINGS:
        wiring = _WIRING.get(offering.id, {})
        notes = _OFFER_NOTES.get(offering.id, "")
        offers.append(_offer_to_dict(offering, wiring, notes))

    return {
        "version": "1.0",
        "wave": "14J",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": "auto_client_acquisition/service_catalog/registry.py",
        "registry_count": len(OFFERINGS),
        "offers": offers,
        "non_negotiables_doc": "docs/00_constitution/NON_NEGOTIABLES.md",
        "architecture_layer_map": "docs/ARCHITECTURE_LAYER_MAP.md",
        "wiring_map_doc": "docs/COMMERCIAL_WIRING_MAP.md",
        "trust_pack_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "audit_chain_endpoint": "GET /api/v1/audit/{handle}/control-graph/markdown",
        "governance_decision": "allow",
    }


@router.get("")
async def commercial_map_json() -> dict[str, Any]:
    """JSON — 5 ladder rungs + 1 channel + wiring + non-negotiables + cross-links."""
    return _build_payload()


@router.get("/markdown", response_class=PlainTextResponse)
async def commercial_map_markdown() -> str:
    """Bilingual AR+EN markdown render — same source as docs/COMMERCIAL_WIRING_MAP.md."""
    payload = _build_payload()
    lines: list[str] = []
    lines.append("# Dealix Commercial Wiring Map — خريطة الربط التجاري")
    lines.append("")
    lines.append(f"_Version {payload['version']} · Wave {payload['wave']}_")
    lines.append(f"_Generated: {payload['generated_at']}_")
    lines.append(f"_Source of truth: `{payload['source_of_truth']}` ({payload['registry_count']} offerings)_")
    lines.append("")
    lines.append(
        "Single source of truth showing how every commercial offer maps to a "
        "landing page + a backend endpoint + a delivery surface."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    for offer in payload["offers"]:
        lines.append(f"## {offer['name_en']} — {offer['name_ar']}")
        lines.append("")
        price = offer["price_display_en"]
        if offer["price_unit"] == "one_time" and offer["price_sar"] > 0:
            price = f"{price} one-time"
        lines.append(f"- **Service ID:** `{offer['service_id']}`")
        lines.append(f"- **Price:** {price}")
        lines.append(f"- **Duration:** {offer['duration_days']} days")
        lines.append(f"- **Customer journey stage:** {offer['customer_journey_stage']}")
        lines.append("")
        if offer["notes"]:
            lines.append(f"_{offer['notes']}_")
            lines.append("")
        w = offer["wiring"]
        if w:
            lines.append("**Wiring:**")
            for key in (
                "landing_url", "preview_url", "intake_endpoint",
                "lead_capture_endpoint", "proposal_endpoint",
                "checkout_url", "checkout_endpoint",
                "delivery_module", "delivery_endpoint", "sample_endpoint",
                "proof_endpoint", "case_safe_endpoint",
                "adoption_endpoint", "trust_pack_endpoint",
                "renewal_module", "founder_surface",
                "covenant_doc", "next_offer",
            ):
                if key in w and w[key] is not None:
                    lines.append(f"  - `{key}`: {w[key]}")
            lines.append("")
        lines.append("**Non-negotiables enforced (`hard_gates`):**")
        for g in offer["non_negotiables_enforced"]:
            lines.append(f"  - `{g}`")
        lines.append("")
        lines.append(f"**KPI commitment (EN):** {offer['kpi_commitment_en']}")
        lines.append("")
        lines.append(f"**التزام KPI (AR):** {offer['kpi_commitment_ar']}")
        lines.append("")
        lines.append("**Deliverables:**")
        for d in offer["deliverables"]:
            lines.append(f"  - {d}")
        lines.append("")
        lines.append(f"**Refund (EN):** {offer['refund_policy_en']}")
        lines.append(f"**Refund (AR):** {offer['refund_policy_ar']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Cross-cutting infrastructure")
    lines.append("")
    lines.append("- Lead inbox: `auto_client_acquisition/lead_inbox.py`")
    lines.append("- Transactional email (9 whitelisted kinds): `auto_client_acquisition/email/transactional.py`")
    lines.append("- Sales qualification: `auto_client_acquisition/sales_os/qualification.py`")
    lines.append("- Proposal renderer: `auto_client_acquisition/sales_os/proposal_renderer.py`")
    lines.append("- Sprint orchestrator: `auto_client_acquisition/delivery_factory/delivery_sprint.py`")
    lines.append("- Renewal scheduler: `auto_client_acquisition/payment_ops/renewal_scheduler.py`")
    lines.append("- Proof Pack assembler: `auto_client_acquisition/proof_os/proof_pack.py`")
    lines.append("- Trust Pack: `auto_client_acquisition/trust_os/trust_pack.py`")
    lines.append("- Audit + Evidence Control Plane: `auto_client_acquisition/auditability_os/`, `evidence_control_plane_os/`")
    lines.append("- Agent OS + Secure Runtime: `auto_client_acquisition/agent_os/`, `secure_agent_runtime_os/`")
    lines.append("- Benchmark engine: `auto_client_acquisition/benchmark_os/`")
    lines.append("- PDF renderer: `auto_client_acquisition/proof_to_market/pdf_renderer.py`")
    lines.append("- Referral persistence: `auto_client_acquisition/partnership_os/referral_store.py`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)

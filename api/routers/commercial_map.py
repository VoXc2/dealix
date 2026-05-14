"""Commercial Map — 2026-Q2 reframe.

Single source of truth that maps every Dealix offer to:
  - landing page path
  - intake endpoint
  - checkout flow (URL + tier query)
  - delivery module / endpoint
  - proof / report endpoint
  - founder dashboard surface
  - non-negotiables (hard_gates) honored by code

Reads from `auto_client_acquisition.service_catalog.registry.OFFERINGS`
so the map can never drift from the canonical 3-offer registry.

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
    "strategic_diagnostic": {
        "landing_url": "/diagnostic.html",
        "intake_endpoint": "POST /api/v1/company-growth-beast/diagnostic",
        "lead_capture_endpoint": "POST /api/v1/public/demo-request",
        "checkout_url": None,
        "checkout_endpoint": None,
        "delivery_module": "founder reviews via /api/v1/founder/leads",
        "delivery_endpoint": "GET /api/v1/founder/leads",
        "proof_endpoint": "auto_client_acquisition/email/transactional.send_transactional(kind=diagnostic_intake_confirmation)",
        "founder_surface": "/founder-leads.html",
        "next_offer": "governed_ops_retainer_4999",
    },
    "governed_ops_retainer_4999": {
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
        "next_offer": "revenue_intelligence_sprint_25k",
    },
    "revenue_intelligence_sprint_25k": {
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
        "trust_pack_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "governed_ops_retainer_4999",
    },
}


_OFFER_NOTES = {
    "strategic_diagnostic": (
        "Free 24h strategic diagnostic — opens the funnel. PDPL + NDMO posture audit "
        "anchored on Saudi B2B services. Founder reviews every intake within 24h."
    ),
    "governed_ops_retainer_4999": (
        "Monthly retainer — entry point to the ladder. Min commitment 3 months. "
        "Weekly brief + monthly Value Report + Proof Pack + adoption score + "
        "retainer readiness gate. Renewal auto-charge after 3 confirmed cycles."
    ),
    "revenue_intelligence_sprint_25k": (
        "Flagship 30-day Sprint. 3 sources of truth merged, target forecast accuracy "
        "≥85%, audit-ready governance, Capital Asset registered. 50% on acceptance, "
        "50% on Proof Pack. 50% refund if retainer-readiness gate unmet within 60d."
    ),
}


def _offer_to_dict(offering, wiring: dict[str, Any], notes: str) -> dict[str, Any]:
    return {
        "service_id": offering.id,
        "name_ar": offering.name_ar,
        "name_en": offering.name_en,
        "price_sar": offering.price_sar,
        "price_unit": offering.price_unit,
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
        "version": "2.0",
        "wave": "2026Q2-reframe",
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
    """JSON — 7 offers + wiring + non-negotiables + cross-links."""
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
        if offer["price_unit"] == "custom":
            price = "Custom (per partnership)"
        elif offer["price_unit"] == "per_month":
            price = f"{int(offer['price_sar']):,} SAR / month"
        else:
            price = f"{int(offer['price_sar']):,} SAR one-time"
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

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
so the map can never drift from the canonical offer registry.

Endpoints:
  GET /api/v1/commercial-map           → JSON
  GET /api/v1/commercial-map/markdown  → bilingual AR+EN markdown
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.service_catalog.registry import OFFERINGS

router = APIRouter(prefix="/api/v1/commercial-map", tags=["commercial-map"])


# Per-service wiring overlays (landing + endpoints).
# Keys MUST match `auto_client_acquisition.service_catalog.registry` ids.
_DIAGNOSTIC_WIRING: dict[str, Any] = {
    "landing_url": "/dealix-diagnostic.html",
    "intake_endpoint": "POST /api/v1/revenue-autopilot/lead",
    "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
    "delivery_module": "auto_client_acquisition.diagnostic_engine + auto_client_acquisition.revenue_autopilot",
    "delivery_endpoint": "POST /api/v1/revenue-autopilot/engagements/{id}/automations/{automation_name}",
    "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
    "founder_surface": "/founder-dashboard.html",
    "next_offer": "revenue_intelligence_sprint",
}

_WIRING: dict[str, dict[str, Any]] = {
    "diagnostic_starter_4999": {
        **_DIAGNOSTIC_WIRING,
        "checkout_url": "/checkout.html?tier=diagnostic_starter",
    },
    "diagnostic_standard_9999": {
        **_DIAGNOSTIC_WIRING,
        "checkout_url": "/checkout.html?tier=diagnostic_standard",
    },
    "diagnostic_executive_15000": {
        **_DIAGNOSTIC_WIRING,
        "checkout_url": "/checkout.html?tier=diagnostic_executive",
    },
    "revenue_intelligence_sprint": {
        "landing_url": "/dealix-diagnostic.html#sprint",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.revenue_autopilot.orchestrator",
        "delivery_endpoint": "POST /api/v1/revenue-autopilot/engagements/{id}/automations/{automation_name}",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "governed_ops_retainer",
    },
    "governed_ops_retainer": {
        "landing_url": "/dealix-diagnostic.html#retainer",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "scripts/monthly_cadence_runner.py + auto_client_acquisition.revenue_autopilot",
        "delivery_endpoint": "GET /api/v1/customer-portal/{handle}/workspace",
        "proof_endpoint": "GET /api/v1/value/{handle}/report/monthly",
        "renewal_module": "auto_client_acquisition.payment_ops.renewal_scheduler",
        "founder_surface": "/customer-portal.html?handle={customer}",
        "next_offer": None,
    },
}


_OFFER_NOTES = {
    "diagnostic_starter_4999": (
        "Entry tier of the single front-door offer. 7-day governed diagnostic of "
        "one revenue workflow. Surfaces 3 evidence-backed decisions + Proof Pack."
    ),
    "diagnostic_standard_9999": (
        "Standard tier. Up to 3 workflows, approval-boundary gap analysis, 90-day "
        "governed action plan, 5 evidence-backed decisions + executive readout."
    ),
    "diagnostic_executive_15000": (
        "Executive tier. Full-funnel governance audit, 7 evidence-backed decisions, "
        "board memo, and a Governed Ops Retainer scope draft."
    ),
    "revenue_intelligence_sprint": (
        "First evidence-led follow-on. Scoped from the diagnostic findings. "
        "14-day governed rebuild of the prioritized workflow with a Proof Pack."
    ),
    "governed_ops_retainer": (
        "Monthly follow-on. Runs the governed revenue ops, daily approval queue, "
        "and a monthly Proof Pack. Price scoped per engagement."
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
        "version": "1.0",
        "wave": "14J",
        "generated_at": datetime.now(UTC).isoformat(),
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
    """JSON — every offer + wiring + non-negotiables + cross-links."""
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

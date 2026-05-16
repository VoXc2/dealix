"""Commercial map — CEO/Board aligned service wiring.

Single source of truth that maps every Dealix offer to:
  - landing page path
  - intake endpoint
  - checkout flow (URL + tier query)
  - delivery module / endpoint
  - proof / report endpoint
  - founder dashboard surface
  - non-negotiables (hard_gates) honored by code

Reads from `auto_client_acquisition.service_catalog.registry.OFFERINGS`
so the map can never drift from the canonical 7-offer registry.

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
    "free_mini_diagnostic": {
        "landing_url": "/diagnostic.html",
        "intake_endpoint": "POST /api/v1/diagnostics",
        "lead_capture_endpoint": "POST /api/v1/public/demo-request",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.diagnostic_engine",
        "delivery_endpoint": "POST /api/v1/revenue-ops/diagnostics",
        "proof_endpoint": "GET /api/v1/decision-passport/golden-chain",
        "founder_surface": "/founder-command-center.html",
        "next_offer": "revenue_proof_sprint_499",
    },
    "revenue_proof_sprint_499": {
        "landing_url": "/revenue-intelligence-sprint.html",
        "preview_url": "/proof-pack-sample.html",
        "intake_endpoint": "POST /api/v1/revenue-ops/diagnostics",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.delivery_factory.delivery_sprint",
        "delivery_endpoint": "POST /api/v1/revenue-ops/score",
        "sample_endpoint": "GET /api/v1/revenue-os/catalog",
        "proof_endpoint": "POST /api/v1/evidence/events",
        "case_safe_endpoint": "GET /api/v1/revenue-ops/{id}/decision-passport",
        "founder_surface": "/revenue-ops-console.html",
        "next_offer": "growth_ops_monthly_2999",
    },
    "data_to_revenue_pack_1500": {
        "landing_url": "/data-readiness.html",
        "intake_endpoint": "POST /api/v1/revenue-ops/upload",
        "preview_endpoint": "POST /api/v1/data-os/import-preview",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.data_os",
        "delivery_endpoint": "POST /api/v1/revenue-ops/upload",
        "proof_endpoint": "POST /api/v1/evidence/events",
        "founder_surface": "/revenue-ops-console.html",
        "next_offer": "growth_ops_monthly_2999",
    },
    "growth_ops_monthly_2999": {
        "landing_url": "/governed-ops-retainer.html",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.reporting_os + board_decision_os",
        "delivery_endpoint": "GET /api/v1/board-decision-os/overview",
        "proof_endpoint": "POST /api/v1/evidence/events",
        "adoption_endpoint": "GET /api/v1/customer-success/{handle}/adoption-score",
        "renewal_module": "auto_client_acquisition.payment_ops.renewal_scheduler",
        "founder_surface": "/founder-command-center.html",
        "next_offer": "executive_command_center_7500",
    },
    "support_os_addon_1500": {
        "landing_url": "/ai-governance-for-revenue.html",
        "intake_endpoint": "POST /api/v1/approvals",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.approval_center + responsible_ai_os",
        "delivery_endpoint": "POST /api/v1/approvals",
        "proof_endpoint": "POST /api/v1/evidence/events",
        "founder_surface": "/approval-center.html",
        "next_offer": None,
    },
    "executive_command_center_7500": {
        "landing_url": "/board-decision-memo.html",
        "intake_endpoint": "POST /api/v1/service-setup/requests",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.board_decision_os",
        "delivery_endpoint": "GET /api/v1/board-decision-os/overview",
        "proof_endpoint": "GET /api/v1/audit/{handle}/control-graph/markdown",
        "trust_pack_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "founder_surface": "/board-decision-os.html",
        "next_offer": None,
    },
    "agency_partner_os": {
        "landing_url": "/trust-pack-lite.html",
        "intake_endpoint": "POST /api/v1/approvals",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.trust_os.trust_pack",
        "delivery_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "proof_endpoint": "GET /api/v1/audit/{handle}/control-graph/markdown",
        "covenant_doc": "docs/SECURITY_RUNBOOK.md",
        "founder_surface": "/approval-center.html",
        "next_offer": None,
    },
}


_OFFER_NOTES = {
    "free_mini_diagnostic": (
        "Entry offer for teams with AI/revenue drift. Produces source clarity, "
        "decision passport, and a governed sprint recommendation."
    ),
    "revenue_proof_sprint_499": (
        "Core value offer. Converts diagnostic findings into prioritized accounts, "
        "risk scoring, follow-up drafts, and proof-backed decisions."
    ),
    "data_to_revenue_pack_1500": (
        "Data readiness guardrail for AI. Runs CRM hygiene + source mapping before "
        "teams scale automation or outbound flows."
    ),
    "growth_ops_monthly_2999": (
        "MRR engine. Monthly governed reviews for revenue, pipeline quality, AI "
        "decisions, and board-facing value reports."
    ),
    "support_os_addon_1500": (
        "Policy package for teams using AI in revenue execution. Defines allowed "
        "actions, forbidden actions, and approval boundaries."
    ),
    "executive_command_center_7500": (
        "Board-facing synthesis of top revenue decisions, risks, and capital "
        "allocation options tied to evidence."
    ),
    "agency_partner_os": (
        "Security/trust response pack sold on demand when buyers ask for policy, "
        "controls, and safety boundaries."
    ),
}


def _offer_to_dict(offering, wiring: dict[str, Any], notes: str) -> dict[str, Any]:
    return {
        "service_id": offering.id,
        "name_ar": offering.name_ar,
        "name_en": offering.name_en,
        "price_sar": offering.price_sar,
        "price_min_sar": offering.price_min_sar,
        "price_max_sar": offering.price_max_sar,
        "price_unit": offering.price_unit,
        "duration_days": offering.duration_days,
        "customer_journey_stage": str(offering.customer_journey_stage),
        "target_segments": list(offering.target_segments),
        "trigger_signals": list(offering.trigger_signals),
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
        min_price = offer.get("price_min_sar")
        max_price = offer.get("price_max_sar")
        if min_price is not None and max_price is not None and min_price != max_price:
            if offer["price_unit"] == "per_month":
                price = f"{int(min_price):,}–{int(max_price):,} SAR / month"
            elif offer["price_unit"] == "custom":
                price = f"{int(min_price):,}–{int(max_price):,} SAR (custom scope)"
            else:
                price = f"{int(min_price):,}–{int(max_price):,} SAR one-time"
        elif offer["price_unit"] == "custom":
            price = "Custom scope"
        elif offer["price_unit"] == "per_month":
            price = f"{int(offer['price_sar']):,} SAR / month"
        else:
            price = f"{int(offer['price_sar']):,} SAR one-time"
        lines.append(f"- **Service ID:** `{offer['service_id']}`")
        lines.append(f"- **Price:** {price}")
        lines.append(f"- **Duration:** {offer['duration_days']} days")
        lines.append(f"- **Customer journey stage:** {offer['customer_journey_stage']}")
        if offer["target_segments"]:
            lines.append(f"- **Target segments:** {', '.join(offer['target_segments'])}")
        if offer["trigger_signals"]:
            lines.append(f"- **Trigger signals:** {', '.join(offer['trigger_signals'])}")
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

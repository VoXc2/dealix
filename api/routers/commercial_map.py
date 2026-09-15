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
so the map can never drift from the canonical 17-offer registry
(7 core funnel + 10 Enterprise Transformation OS systems).

Endpoints:
  GET /api/v1/commercial-map           → JSON
  GET /api/v1/commercial-map/markdown  → bilingual AR+EN markdown
"""
from __future__ import annotations

from datetime import UTC, datetime
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
        "intake_endpoint": "POST /api/v1/company-growth-beast/diagnostic",
        "lead_capture_endpoint": "POST /api/v1/public/demo-request",
        "checkout_url": None,
        "checkout_endpoint": None,
        "delivery_module": "founder reviews via /api/v1/founder/leads",
        "delivery_endpoint": "GET /api/v1/founder/leads",
        "proof_endpoint": "auto_client_acquisition/email/transactional.send_transactional(kind=diagnostic_intake_confirmation)",
        "founder_surface": "/founder-leads.html",
        "next_offer": "revenue_command_pilot_30d",
    },
    "revenue_command_pilot_30d": {
        "landing_url": "/dealix-diagnostic",
        "preview_url": "/sprint-sample.html",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": None,
        "checkout_endpoint": None,
        "delivery_module": "auto_client_acquisition.delivery_factory.delivery_sprint.run_sprint",
        "delivery_endpoint": "POST /api/v1/sprint/run",
        "sample_endpoint": "GET /api/v1/sprint/sample",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "case_safe_endpoint": "GET /api/v1/proof-to-market/case-safe/{engagement_id}",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "growth_ops_monthly_2999",
    },
    "data_to_revenue_pack_1500": {
        "landing_url": "/data-pack.html",
        "intake_endpoint": "POST /api/v1/data-os/import-preview/upload",
        "preview_endpoint": "POST /api/v1/data-os/import-preview",
        "checkout_url": "/checkout.html?tier=data_pack",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.data_os + auto_client_acquisition.delivery_factory.delivery_sprint",
        "delivery_endpoint": "POST /api/v1/sprint/run",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "growth_ops_monthly_2999",
    },
    "growth_ops_monthly_2999": {
        "landing_url": "/pricing.html#growth",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "proposal_endpoint": "POST /api/v1/service-setup/proposal/{customer_id}",
        "checkout_url": "/checkout.html?tier=growth",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "scripts/weekly_brief_runner.py + scripts/monthly_cadence_runner.py",
        "delivery_endpoint": "GET /api/v1/customer-portal/{handle}/workspace",
        "proof_endpoint": "GET /api/v1/value/{handle}/report/monthly",
        "adoption_endpoint": "GET /api/v1/customer-success/{handle}/adoption-score",
        "renewal_module": "auto_client_acquisition.payment_ops.renewal_scheduler",
        "founder_surface": "/customer-portal.html?handle={customer}",
        "next_offer": "executive_command_center_7500",
    },
    "support_os_addon_1500": {
        "landing_url": "/services.html#support",
        "intake_endpoint": "POST /api/v1/service-setup/qualify",
        "checkout_url": "/checkout.html?tier=support_addon",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.support_os",
        "delivery_endpoint": "GET /api/v1/support-os/*",
        "proof_endpoint": "GET /api/v1/value/{handle}/report/monthly",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "executive_command_center_7500": {
        "landing_url": "/executive-command-center.html",
        "intake_endpoint": "POST /api/v1/service-setup/requests",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "delivery_module": "auto_client_acquisition.executive_command_center",
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
    # ── Enterprise Transformation OS (customer_journey_stage="transformation") ──
    # Setup is founder-issued (enterprise = founder-closed, approval-first).
    "ai_command_center_os": {
        "landing_url": "/transformation/ai-command-center.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.executive_command_center",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "whatsapp_revenue_os": {
        "landing_url": "/transformation/whatsapp-revenue.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.sales_os + auto_client_acquisition.delivery_factory",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "ai_command_center_os",
    },
    "brand_intelligence_os": {
        "landing_url": "/transformation/brand-intelligence.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "autonomous_growth.agents.content",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "ai_agent_workforce_os": {
        "landing_url": "/transformation/ai-agent-workforce.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.agent_os + secure_agent_runtime_os",
        "proof_endpoint": "auto_client_acquisition.auditability_os",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "client_experience_os": {
        "landing_url": "/transformation/client-experience.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.client_os + support_os",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "operations_automation_os": {
        "landing_url": "/transformation/operations-automation.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.execution_os",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "executive_reporting_os": {
        "landing_url": "/transformation/executive-reporting.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.command_os",
        "proof_endpoint": "GET /api/v1/audit/{handle}/control-graph/markdown",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": "ai_command_center_os",
    },
    "trust_governance_os": {
        "landing_url": "/transformation/trust-governance.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.trust_os + compliance_os",
        "proof_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "trust_pack_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "growth_engine_os": {
        "landing_url": "/transformation/growth-engine.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": "founder-issued",
        "checkout_endpoint": "POST /api/v1/payment-ops/invoice-intent",
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "auto_client_acquisition.sales_os (draft_only outreach, approval-gated)",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
    "custom_enterprise_system": {
        "landing_url": "/transformation/custom-enterprise.html",
        "intake_endpoint": "POST /api/v1/commercial/transformation-proposal/generate",
        "checkout_url": None,  # custom — scoped + founder-issued per contract
        "checkout_endpoint": None,
        "roi_endpoint": "POST /api/v1/commercial/roi/estimate",
        "delivery_module": "bespoke — paid discovery sprint → architecture → build",
        "proof_endpoint": "auto_client_acquisition.proof_os.proof_pack.assemble",
        "msa_doc": "docs/transformation/enterprise_package/MSA_TEMPLATE_AR_EN.md",
        "dpa_doc": "docs/transformation/enterprise_package/DPA_TEMPLATE_AR_EN.md",
        "founder_surface": "/founder-dashboard.html",
        "next_offer": None,
    },
}


_OFFER_NOTES = {
    "free_mini_diagnostic": (
        "Free 24h diagnostic — opens the funnel. Confirmation email auto-sent. "
        "Founder reviews every intake within 24h."
    ),
    "revenue_command_pilot_30d": (
        "First paid motion. 30 days. One approved operating scope with baseline "
        "and Proof Pack. Quote-only after discovery; no checkout or payment link."
    ),
    "data_to_revenue_pack_1500": (
        "CSV upload → DQ score + cleaned + ranked. Live demo on /data-pack.html "
        "via POST /api/v1/data-os/import-preview/upload. 14-day delivery."
    ),
    "growth_ops_monthly_2999": (
        "Retainer engine. Weekly brief + monthly value report + adoption score + "
        "retainer readiness gate. Renewal auto-charge after 3 confirmed cycles."
    ),
    "support_os_addon_1500": (
        "Add-on to Growth. Ticket classification + suggested replies (draft_only). "
        "SLA breach alerts. Sits inside the customer workspace."
    ),
    "executive_command_center_7500": (
        "Founder/CEO surface. Daily founder brief (WhatsApp draft_only) + monthly "
        "board pack. Includes Trust Pack PDF + Evidence Control Plane export."
    ),
    "agency_partner_os": (
        "Channel offer. 5K SAR / closed deal + 30% commission first year. "
        "Partner Covenant enforced: no unsafe automation, no guaranteed claims."
    ),
    # ── Enterprise Transformation OS ──
    "ai_command_center_os": (
        "Enterprise. Real-time executive command layer. Setup 35K–120K + "
        "8K–35K/mo (estimates). Founder-issued invoice. Starts with free diagnostic."
    ),
    "whatsapp_revenue_os": (
        "Enterprise. WhatsApp → measurable pipeline. Setup 12K–45K + 3K–15K/mo "
        "(estimates). All external messages are approval-gated drafts — no automation."
    ),
    "brand_intelligence_os": (
        "Enterprise. Brand as a reusable operating system. Setup 15K–60K + "
        "4K–18K/mo (estimates)."
    ),
    "ai_agent_workforce_os": (
        "Enterprise. Role-scoped AI agents with approval gates + audit. Setup "
        "40K–180K + 12K–60K/mo (estimates). No autonomous external execution."
    ),
    "client_experience_os": (
        "Enterprise. Unified customer journey first-contact → retention. Setup "
        "20K–80K + 6K–25K/mo (estimates)."
    ),
    "operations_automation_os": (
        "Enterprise. Map-first operations automation with governance. Setup "
        "25K–120K + 7K–35K/mo (estimates)."
    ),
    "executive_reporting_os": (
        "Enterprise. Automated weekly/monthly executive reporting tied to decisions. "
        "Setup 18K–75K + 5K–20K/mo (estimates)."
    ),
    "trust_governance_os": (
        "Enterprise. Practical AI + data governance, PDPL-aligned. Setup 30K–150K + "
        "10K–50K/mo (estimates)."
    ),
    "growth_engine_os": (
        "Enterprise. Repeatable growth machine on approved drafts ONLY. Setup "
        "25K–100K + 8K–30K/mo (estimates). No cold WhatsApp, no LinkedIn automation, "
        "no blast, no scraping."
    ),
    "custom_enterprise_system": (
        "Enterprise bespoke. Paid discovery → architecture → build → SLA. Scope "
        "100K–500K+ (estimate) set per contract. MSA + DPA required."
    ),
}


def _offer_to_dict(offering, wiring: dict[str, Any], notes: str) -> dict[str, Any]:
    safe_wiring = dict(wiring)
    if offering.commercial_status != "public_approved":
        safe_wiring["checkout_url"] = None
        safe_wiring["checkout_endpoint"] = None
    return {
        "service_id": offering.id,
        "name_ar": offering.name_ar,
        "name_en": offering.name_en,
        "price_sar": offering.price_sar if offering.commercial_status == "public_approved" else None,
        "commercial_status": offering.commercial_status,
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
        "wiring": safe_wiring,
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
    """JSON — 17 offers + wiring + non-negotiables + cross-links."""
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
        if offer["price_sar"] is None:
            price = "Quote after discovery — عرض موثق بعد جلسة الاكتشاف"
        elif offer["price_unit"] == "custom":
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

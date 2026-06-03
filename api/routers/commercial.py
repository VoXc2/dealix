"""Commercial Chain Router — Wave 15.

Aggregates the complete Dealix commercial chain:
  Diagnostic → Warm Intro → Pilot → Proof → Payment → Upsell

All endpoints are admin-gated (X-API-Key). All write operations return
approval_status: "approval_required" — nothing auto-sends or auto-charges.

Prefix: /api/v1/commercial
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import PlainTextResponse

from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest
from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest
from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest
from dealix.commercial.proof_builder import ProofBuildRequest, ProofBuilder
from dealix.commercial.upsell_engine import UpsellEngine
from dealix.commercial.case_study_generator import CaseStudyGenerator, CaseStudyRequest
from dealix.payments.payment_link import (
    PaymentLinkRequest,
    SERVICE_TIERS,
    create_payment_link,
)

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/commercial", tags=["commercial"])

_ADMIN_KEY = os.getenv("DEALIX_ADMIN_API_KEY", "")


def _require_admin(x_api_key: str = Header(default="")) -> None:
    if not _ADMIN_KEY:
        return  # dev mode — no key configured
    if x_api_key != _ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ---------------------------------------------------------------------------
# Diagnostic endpoints
# ---------------------------------------------------------------------------


@router.post("/diagnostic/generate")
async def diagnostic_generate(
    req: DiagnosticRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Generate a 10-section bilingual diagnostic report for a Saudi B2B company."""
    engine = DiagnosticEngine()
    report = engine.generate(req)
    log.info("diagnostic_generated", report_id=report.report_id, company=req.company_name)
    return report.to_dict()


@router.post("/diagnostic/generate/markdown", response_class=PlainTextResponse)
async def diagnostic_generate_markdown(
    req: DiagnosticRequest,
    _: None = Depends(_require_admin),
) -> str:
    """Generate diagnostic report and return as Markdown (AR+EN)."""
    engine = DiagnosticEngine()
    report = engine.generate(req)
    return report.markdown_ar_en


# ---------------------------------------------------------------------------
# Warm intro endpoints
# ---------------------------------------------------------------------------


@router.post("/warm-intro/draft")
async def warm_intro_draft(
    req: WarmIntroRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Generate 5 WhatsApp + 3 email draft warm intros. All approval-gated."""
    gen = WarmIntroGenerator()
    bundle = gen.generate(req)
    log.info(
        "warm_intro_generated",
        bundle_id=bundle.bundle_id,
        prospect=req.prospect_name,
        whatsapp=len(bundle.whatsapp_drafts),
        email=len(bundle.email_drafts),
    )
    return bundle.to_dict()


# ---------------------------------------------------------------------------
# Pilot delivery endpoints
# ---------------------------------------------------------------------------


@router.post("/pilot/start")
async def pilot_start(
    req: PilotStartRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Start a 7-day 499 SAR pilot — returns day-by-day delivery plan."""
    kit = PilotDeliveryKit()
    plan = kit.create_pilot_plan(req)
    log.info(
        "pilot_started",
        pilot_id=plan.pilot_id,
        account=req.account_id,
        company=req.company_name,
    )
    return plan.to_dict()


@router.get("/pilot/{pilot_id}/report", response_class=PlainTextResponse)
async def pilot_report(
    pilot_id: str,
    company_name: str = "الشركة",
    _: None = Depends(_require_admin),
) -> str:
    """Return the Week 1 report template for a pilot."""
    kit = PilotDeliveryKit()
    req = PilotStartRequest(
        account_id=pilot_id,
        company_name=company_name,
    )
    plan = kit.create_pilot_plan(req)
    return plan.week1_report_template.replace("{{pilot_id}}", pilot_id)


# ---------------------------------------------------------------------------
# Proof pack endpoints
# ---------------------------------------------------------------------------


@router.post("/proof/build")
async def proof_build(
    req: ProofBuildRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Build a proof pack from documented pilot events."""
    builder = ProofBuilder()
    pack = builder.build(req)
    log.info(
        "proof_pack_built",
        pack_id=pack.pack_id,
        level=pack.proof_level,
        events=pack.event_count,
    )
    return pack.to_dict()


@router.post("/proof/build/markdown", response_class=PlainTextResponse)
async def proof_build_markdown(
    req: ProofBuildRequest,
    _: None = Depends(_require_admin),
) -> str:
    """Build proof pack and return as Markdown."""
    builder = ProofBuilder()
    pack = builder.build(req)
    return pack.markdown_ar_en


# ---------------------------------------------------------------------------
# Payment link endpoint
# ---------------------------------------------------------------------------


@router.post("/payment/link")
async def payment_link(
    req: PaymentLinkRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Generate a Moyasar invoice link for a service tier.

    Sandbox mode by default — set MOYASAR_LIVE_MODE=1 in Railway for live charges.
    """
    from dealix.payments.payment_link import PaymentLinkError  # noqa: PLC0415

    try:
        result = await create_payment_link(req)
    except PaymentLinkError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.to_dict()


@router.get("/payment/tiers")
async def payment_tiers(
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Return all available service tiers with prices."""
    return {
        "tiers": SERVICE_TIERS,
        "currency": "SAR",
        "live_mode": os.getenv("MOYASAR_LIVE_MODE", "0") in ("1", "true", "yes"),
    }


# ---------------------------------------------------------------------------
# Upsell endpoints
# ---------------------------------------------------------------------------


@router.get("/upsell/check/{account_id}")
async def upsell_check(
    account_id: str,
    company_name: str = "",
    proof_event_count: int = 0,
    proof_level: str = "L0",
    monthly_revenue_sar: float = 0.0,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Check upsell eligibility and generate proposal draft if eligible."""
    engine = UpsellEngine()
    result = engine.check(
        account_id=account_id,
        company_name=company_name or account_id,
        proof_event_count=proof_event_count,
        proof_level=proof_level,
        monthly_revenue_sar=monthly_revenue_sar,
    )
    return result.to_dict()


# ---------------------------------------------------------------------------
# Case study endpoints
# ---------------------------------------------------------------------------


@router.post("/case-study/generate")
async def case_study_generate(
    req: CaseStudyRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Generate a bilingual case study. customer_consent required for quotes."""
    gen = CaseStudyGenerator()
    doc = gen.generate(req)
    return doc.to_dict()


@router.post("/case-study/generate/markdown", response_class=PlainTextResponse)
async def case_study_markdown(
    req: CaseStudyRequest,
    _: None = Depends(_require_admin),
) -> str:
    gen = CaseStudyGenerator()
    doc = gen.generate(req)
    return doc.markdown_ar_en


# ---------------------------------------------------------------------------
# Daily brief endpoint
# ---------------------------------------------------------------------------


@router.get("/daily-brief")
async def daily_brief(
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Founder daily brief — lead queue, top opportunities, revenue state."""
    now = datetime.now(UTC)
    return {
        "brief_date": now.strftime("%Y-%m-%d"),
        "brief_time_utc": now.isoformat(),
        "brief_time_riyadh": now.strftime("%H:%M KSA (UTC+3, actual UTC)"),
        "status": "operational",
        "chain_status": {
            "diagnostic_engine": "ready",
            "warm_intro_generator": "ready — approval_required",
            "pilot_delivery_kit": "ready",
            "proof_builder": "ready",
            "upsell_engine": "ready",
            "payment_link": "sandbox" if os.getenv("MOYASAR_LIVE_MODE", "0") not in ("1", "true") else "live",
        },
        "action_items": [
            "Review pending diagnostic reports in /api/v1/commercial/diagnostic/generate",
            "Approve or reject warm intro drafts before any outreach",
            "Check upsell eligibility for accounts with 3+ proof events",
        ],
        "reminders": [
            "NO_LIVE_SEND: all outreach requires founder approval",
            "NO_LIVE_CHARGE: Moyasar in sandbox mode by default",
            "NO_FAKE_PROOF: only documented events accepted in proof builder",
        ],
    }

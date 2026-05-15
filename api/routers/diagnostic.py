"""
Diagnostic Router — bilingual diagnostic brief generator.
موجِّه التشخيص — مُولِّد موجز ثنائي اللغة.

Endpoints under /api/v1/diagnostic/:
    GET  /status     — module health + supported sectors + guardrails
    GET  /sectors    — list of supported sector keys
    POST /generate   — build a diagnostic brief from a request body

Pure local composition: no LLM calls, no live sends, no external HTTP.
Every generated brief is tagged ``approval_status="approval_required"``.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.diagnostic_engine import (
    DiagnosticRequest,
    generate_diagnostic,
    generate_opportunity_report,
    list_opportunity_sectors,
    list_supported_sectors,
)

router = APIRouter(prefix="/api/v1/diagnostic", tags=["diagnostic"])

_CAPABILITY_AXIS_KEYS: tuple[str, ...] = (
    "revenue",
    "data",
    "workflow",
    "knowledge",
    "governance",
    "reporting",
)


class DiagnosticIntentBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    axes_0_5: dict[str, int]
    customer_handle: str | None = Field(default=None, max_length=120)
    diagnostic_amount_sar: float | None = Field(default=None, ge=0, le=500_000)


@router.get("/status")
async def diagnostic_status() -> dict[str, Any]:
    """Module health, supported sectors, and active guardrails."""
    sectors = list_supported_sectors()
    return {
        "module": "diagnostic_engine",
        "status": "operational",
        "supported_sectors": sectors,
        "n_sectors": len(sectors),
        "guardrails": {
            "no_llm_calls": True,
            "no_live_sends": True,
            "no_external_http": True,
            "approval_required_on_every_brief": True,
            "pdpl_aware": True,
        },
    }


@router.get("/sectors")
async def diagnostic_sectors() -> dict[str, Any]:
    """List the sector keys backed by the Service Readiness Matrix."""
    return {
        "sectors": list_supported_sectors(),
        "opportunity_report_sectors": list_opportunity_sectors(),
    }


@router.post("/generate")
async def diagnostic_generate(payload: DiagnosticRequest) -> dict[str, Any]:
    """Render a bilingual diagnostic brief — never auto-sent."""
    result = generate_diagnostic(payload)
    return result.model_dump(mode="json")


class OpportunityReportBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str = Field(..., min_length=1, max_length=200)
    sector: str = "b2b_services"
    region: str = "ksa"
    recommended_tier_id: str = Field(default="", max_length=64)


@router.post("/opportunity-report")
async def diagnostic_opportunity_report(body: OpportunityReportBody) -> dict[str, Any]:
    """Generate an AI Opportunity Report for a target company.

    The founder-led enterprise sales artifact: 5 AI opportunities with an
    impact hypothesis, mapped to an enterprise transformation program.
    Approval-gated — reviewed before any outreach.
    """
    report = generate_opportunity_report(
        company=body.company,
        sector=body.sector,
        region=body.region,
        recommended_tier_id=body.recommended_tier_id,
    )
    return report.to_dict()


@router.post("/opportunity-report/pdf")
async def diagnostic_opportunity_report_pdf(body: OpportunityReportBody) -> Any:
    """Generate the AI Opportunity Report and return it as a PDF download.

    Falls back to markdown (200, text/markdown) when no PDF engine is
    installed in the environment.
    """
    from fastapi.responses import Response

    from auto_client_acquisition.proof_to_market.pdf_renderer import (
        render_markdown_to_pdf,
    )

    report = generate_opportunity_report(
        company=body.company,
        sector=body.sector,
        region=body.region,
        recommended_tier_id=body.recommended_tier_id,
    )
    pdf = render_markdown_to_pdf(
        report.markdown_ar_en, title=f"AI Opportunity Report — {body.company}"
    )
    if pdf is None:
        return Response(
            content=report.markdown_ar_en,
            media_type="text/markdown; charset=utf-8",
            headers={"X-PDF-Engine": "unavailable"},
        )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="opportunity-report-{body.company}.pdf"'
            )
        },
    )


@router.post("/intent")
async def diagnostic_intent(body: DiagnosticIntentBody) -> dict[str, Any]:
    """Six axes × 0–5 capability snapshot + DTG decision + optional invoice intent (not revenue)."""
    for k in _CAPABILITY_AXIS_KEYS:
        if k not in body.axes_0_5:
            raise HTTPException(
                status_code=422,
                detail={"en": f"missing axis: {k}", "ar": f"محور ناقص: {k}"},
            )
        v = body.axes_0_5[k]
        if not isinstance(v, int) or v < 0 or v > 5:
            raise HTTPException(
                status_code=422,
                detail={"en": f"axis {k} must be int 0-5", "ar": f"المحور {k} يجب أن يكون 0-5"},
            )
    total = sum(body.axes_0_5[k] for k in _CAPABILITY_AXIS_KEYS)
    capability_score = round(100.0 * (total / (6 * 5)), 2)
    min_v = min(body.axes_0_5[k] for k in _CAPABILITY_AXIS_KEYS)
    transformation_gap = round(5.0 - min_v, 2)
    if min_v <= 1 or capability_score < 50:
        dtg = "diagnostic_first"
    elif body.axes_0_5.get("governance", 0) >= 4 and body.axes_0_5.get("data", 0) >= 3 and capability_score >= 68:
        dtg = "sprint_now"
    elif capability_score >= 62:
        dtg = "quick_win"
    elif capability_score < 40:
        dtg = "deprioritize"
    else:
        dtg = "diagnostic_first"
    sprint = "Revenue Intelligence Sprint" if dtg in ("sprint_now", "quick_win") else "Capability Diagnostic"
    retainer_path = "pause_until_proof" if dtg == "deprioritize" else "proof_then_retainer"
    expected_proof = "Revenue Proof Pack (draft-first)" if sprint.startswith("Revenue") else "Diagnostic one-pager"
    invoice = None
    if body.customer_handle and body.diagnostic_amount_sar is not None:
        from auto_client_acquisition.payment_ops import create_invoice_intent

        try:
            rec = create_invoice_intent(
                customer_handle=body.customer_handle,
                amount_sar=float(body.diagnostic_amount_sar),
                method="moyasar_test",
                service_session_id=None,
            )
            invoice = rec.model_dump(mode="json")
        except ValueError as e:
            raise HTTPException(status_code=403, detail={"en": str(e), "ar": "فشل إنشاء فاتورة — بوابات الدفع"}) from e
    return {
        "governance_decision": GovernanceDecision.ALLOW.value,
        "matched_rules": [],
        "risk_level": "low",
        "capability_score": capability_score,
        "axes_0_5": {k: body.axes_0_5[k] for k in _CAPABILITY_AXIS_KEYS},
        "transformation_gap": transformation_gap,
        "dtg_decision": dtg,
        "recommended_sprint": sprint,
        "retainer_path": retainer_path,
        "expected_proof": expected_proof,
        "invoice_intent": invoice,
        "hard_gates": {
            "invoice_not_revenue": True,
            "evidence_reference_required_for_confirm": True,
        },
    }

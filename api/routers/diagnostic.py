"""
Diagnostic Router — bilingual diagnostic brief generator.
موجِّه التشخيص — مُولِّد موجز ثنائي اللغة.

Endpoints under /api/v1/diagnostic/:
    GET  /status            — module health + supported sectors + guardrails
    GET  /sectors           — list of supported sector keys
    POST /generate          — build a diagnostic brief from a request body
    POST /report/markdown   — customer-facing 1-page bilingual report
    POST /report/pdf        — the same report rendered as PDF

Pure local composition: no LLM calls, no live sends, no external HTTP.
Every generated brief is tagged ``approval_status="approval_required"``.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.diagnostic_engine import (
    DiagnosticRequest,
    generate_diagnostic,
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
    return {"sectors": list_supported_sectors()}


@router.post("/generate")
async def diagnostic_generate(payload: DiagnosticRequest) -> dict[str, Any]:
    """Render a bilingual diagnostic brief — never auto-sent."""
    result = generate_diagnostic(payload)
    return result.model_dump(mode="json")


_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)


def _diagnostic_report_markdown(result: Any) -> str:
    """Wrap a DiagnosticResult's bilingual body in a 1-page customer header.

    Keeps the ``approval_required`` status visible — the report is a
    deliverable the founder reviews and sends, never auto-sent.
    """
    return "\n".join(
        [
            f"# Dealix AI Ops Diagnostic — {result.company}",
            "",
            f"**Recommended bundle / الحزمة الموصى بها:** "
            f"{result.bundle_name_ar} · {result.bundle_name_en} "
            f"(`{result.recommended_bundle}`)",
            "",
            f"**Status / الحالة:** {result.approval_status} — "
            "founder review required before sending / "
            "مراجعة المؤسس مطلوبة قبل الإرسال.",
            "",
            "---",
            "",
            result.markdown_ar_en,
            "",
            "---",
            f"_{_DISCLAIMER}_",
        ]
    )


@router.post("/report/markdown", response_class=PlainTextResponse)
async def diagnostic_report_markdown(payload: DiagnosticRequest) -> str:
    """Customer-facing 1-page bilingual diagnostic report (markdown)."""
    result = generate_diagnostic(payload)
    return _diagnostic_report_markdown(result)


@router.post("/report/pdf")
async def diagnostic_report_pdf(payload: DiagnosticRequest):
    """The diagnostic report rendered as PDF. Falls back to markdown with an
    ``X-PDF-Renderer`` header when no PDF renderer is installed."""
    from auto_client_acquisition.proof_to_market.pdf_renderer import (
        render_markdown_to_pdf,
    )

    result = generate_diagnostic(payload)
    md = _diagnostic_report_markdown(result)
    pdf = render_markdown_to_pdf(md, title=f"Dealix Diagnostic — {result.company}")
    if pdf is None:
        return PlainTextResponse(
            content=md,
            headers={"X-PDF-Renderer": "unavailable; markdown returned as fallback"},
        )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="diagnostic_report.pdf"'},
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

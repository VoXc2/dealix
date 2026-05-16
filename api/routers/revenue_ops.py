"""Governed Revenue Ops API surface."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
    render_approval_card,
)
from auto_client_acquisition.revenue_ops import (
    DiagnosticRequest,
    FollowUpDraftRequest,
    ScoreRequest,
    UploadRequest,
    add_upload,
    attach_approval_id,
    create_diagnostic,
    create_follow_up_drafts,
    get_record,
    score_opportunities,
)
from auto_client_acquisition.revenue_ops.store import _reset_store

router = APIRouter(prefix="/api/v1/revenue-ops", tags=["Revenue Ops"])

_HARD_GATES = {
    "no_auto_external_send": True,
    "approval_first": True,
    "every_decision_needs_source_ref": True,
    "every_action_must_link_evidence": True,
    "decision_passport_required": True,
}

_POSITIONING = {
    "name_en": "Dealix — Governed Revenue & AI Operations",
    "name_ar": "ديلكس — تشغيل الإيرادات والذكاء الاصطناعي المحكوم",
    "value_en": (
        "Dealix helps companies turn AI experiments and revenue operations "
        "into governed, measurable, evidence-backed workflows."
    ),
    "value_ar": (
        "تساعد ديلكس الشركات على تحويل تجارب الذكاء الاصطناعي وعمليات "
        "الإيراد إلى تشغيل محكوم، قابل للقياس، ومربوط بالأدلة."
    ),
}

_CATALOG: tuple[dict[str, Any], ...] = (
    {
        "id": "governed_revenue_ops_diagnostic",
        "name_en": "Governed Revenue Ops Diagnostic",
        "name_ar": "تشخيص عمليات الإيراد المحكومة",
        "price_sar_range": "4,999 - 15,000",
        "price_sar_enterprise": "15,000 - 25,000",
    },
    {
        "id": "revenue_intelligence_sprint",
        "name_en": "Revenue Intelligence Sprint",
        "name_ar": "سبرنت ذكاء الإيراد",
        "price_sar_from": "25,000",
    },
    {
        "id": "governed_ops_retainer",
        "name_en": "Governed Ops Retainer",
        "name_ar": "ريتـينر التشغيل المحكوم",
        "price_sar_monthly_range": "4,999 - 15,000",
    },
    {
        "id": "ai_governance_for_revenue_teams",
        "name_en": "AI Governance for Revenue Teams",
        "name_ar": "حوكمة الذكاء الاصطناعي لفرق الإيراد",
    },
    {
        "id": "crm_data_readiness_for_ai",
        "name_en": "CRM / Data Readiness for AI",
        "name_ar": "جاهزية CRM والبيانات للذكاء الاصطناعي",
    },
    {
        "id": "board_decision_memo",
        "name_en": "Board Decision Memo",
        "name_ar": "مذكرة قرار الإدارة",
    },
    {
        "id": "trust_pack_lite",
        "name_en": "Trust Pack Lite",
        "name_ar": "حزمة الثقة الخفيفة",
    },
)


@router.get("/catalog")
async def revenue_ops_catalog() -> dict[str, Any]:
    return {
        "positioning": _POSITIONING,
        "count": len(_CATALOG),
        "offerings": list(_CATALOG),
        "hard_gates": _HARD_GATES,
    }


@router.post("/diagnostics")
async def create_revenue_ops_diagnostic(req: DiagnosticRequest) -> dict[str, Any]:
    record = create_diagnostic(req)
    return {
        "diagnostic_id": record.diagnostic_id,
        "state": record.state.value,
        "client_name": record.client_name,
        "decision_passport": record.decision_passport,
        "hard_gates": _HARD_GATES,
    }


@router.post("/upload")
async def revenue_ops_upload(req: UploadRequest) -> dict[str, Any]:
    try:
        upload = add_upload(req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"upload": upload, "hard_gates": _HARD_GATES}


@router.post("/score")
async def revenue_ops_score(req: ScoreRequest) -> dict[str, Any]:
    try:
        scored = score_opportunities(req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "diagnostic_id": req.diagnostic_id,
        "opportunities_ranked": [x.model_dump(mode="json") for x in scored],
        "hard_gates": _HARD_GATES,
    }


@router.get("/{diagnostic_id}/decision-passport")
async def revenue_ops_decision_passport(diagnostic_id: str) -> dict[str, Any]:
    record = get_record(diagnostic_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"unknown diagnostic_id: {diagnostic_id}")
    return {
        "diagnostic_id": diagnostic_id,
        "state": record.state.value,
        "decision_passport": record.decision_passport,
        "uploads_count": len(record.uploads),
        "evidence_events_count": len(record.evidence_events),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{diagnostic_id}/follow-up-drafts")
async def revenue_ops_follow_up_drafts(
    diagnostic_id: str,
    req: FollowUpDraftRequest,
) -> dict[str, Any]:
    try:
        drafts = create_follow_up_drafts(diagnostic_id, req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    approval = ApprovalRequest(
        object_type="revenue_ops_follow_up_batch",
        object_id=diagnostic_id,
        action_type="draft_email",
        action_mode="approval_required",
        summary_ar="دفعة مسودات متابعة جاهزة للمراجعة",
        summary_en="Follow-up draft batch ready for review",
        proof_impact=f"decision_passport:{diagnostic_id}",
    )
    approval_stored = get_default_approval_store().create(approval)
    attach_approval_id(diagnostic_id, approval_stored.approval_id)
    return {
        "diagnostic_id": diagnostic_id,
        "drafts": drafts,
        "approval": approval_stored.model_dump(mode="json"),
        "approval_card": render_approval_card(approval_stored),
        "hard_gates": _HARD_GATES,
    }


def _reset_revenue_ops_state() -> None:
    """Test-only helper."""
    _reset_store()

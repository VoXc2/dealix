"""In-memory store and deterministic logic for governed revenue ops."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.revenue_ops.schemas import (
    DiagnosticRequest,
    EvidenceEventRequest,
    FollowUpDraftRequest,
    RevenueDiagnosticRecord,
    RevenueOpsState,
    ScoreRequest,
    ScoredOpportunity,
    UploadRequest,
)


_RECORDS: dict[str, RevenueDiagnosticRecord] = {}

_TRANSITIONS: dict[RevenueOpsState, set[RevenueOpsState]] = {
    RevenueOpsState.DRAFT: {RevenueOpsState.APPROVED},
    RevenueOpsState.APPROVED: {RevenueOpsState.SENT},
    RevenueOpsState.SENT: {RevenueOpsState.USED_IN_MEETING},
    RevenueOpsState.USED_IN_MEETING: {RevenueOpsState.SCOPE_REQUESTED},
    RevenueOpsState.SCOPE_REQUESTED: {RevenueOpsState.INVOICE_SENT},
    RevenueOpsState.INVOICE_SENT: {RevenueOpsState.INVOICE_PAID},
    RevenueOpsState.INVOICE_PAID: set(),
}


def create_diagnostic(req: DiagnosticRequest) -> RevenueDiagnosticRecord:
    diagnostic_id = RevenueDiagnosticRecord.next_id()
    decision_passport = {
        "diagnostic_id": diagnostic_id,
        "source_refs": [req.crm_source_ref],
        "approval": {
            "required": True,
            "status": "pending",
            "approval_id": None,
        },
        "evidence": [],
        "recommended_next_action": "create_diagnostic_scope",
        "recommended_next_action_ar": "أنشئ نطاق التشخيص",
        "state": RevenueOpsState.DRAFT.value,
    }
    record = RevenueDiagnosticRecord(
        diagnostic_id=diagnostic_id,
        client_name=req.client_name,
        sector=req.sector,
        requested_by=req.requested_by,
        crm_source_ref=req.crm_source_ref,
        decision_passport=decision_passport,
    )
    _RECORDS[diagnostic_id] = record
    return record


def get_record(diagnostic_id: str) -> RevenueDiagnosticRecord | None:
    return _RECORDS.get(diagnostic_id)


def add_upload(req: UploadRequest) -> dict[str, Any]:
    record = _require_record(req.diagnostic_id)
    upload_event = {
        "source_ref": req.source_ref,
        "filename": req.filename,
        "row_count": req.row_count,
        "quality_score": round(req.quality_score, 4),
        "uploaded_by": req.uploaded_by,
        "uploaded_at": datetime.now(UTC).isoformat(),
    }
    record.uploads.append(upload_event)
    _extend_passport_source(record, req.source_ref)
    _append_passport_evidence(
        record,
        {
            "type": "crm_upload",
            "source_ref": req.source_ref,
            "summary_en": f"Uploaded {req.filename} ({req.row_count} rows)",
            "summary_ar": f"تم رفع الملف {req.filename} بعدد {req.row_count} صف",
        },
    )
    return upload_event


def score_opportunities(req: ScoreRequest) -> list[ScoredOpportunity]:
    record = _require_record(req.diagnostic_id)
    max_value = max((x.estimated_value_sar for x in req.opportunities), default=1.0)
    scored: list[ScoredOpportunity] = []
    for item in req.opportunities:
        risk_count = len(item.risk_signals)
        value_weight = 0.0 if max_value <= 0 else min(1.0, item.estimated_value_sar / max_value)
        risk_penalty = min(0.7, 0.1 * risk_count)
        score = round(max(0.0, value_weight * (1.0 - risk_penalty)), 4)
        scored.append(
            ScoredOpportunity(
                account_name=item.account_name,
                pipeline_stage=item.pipeline_stage,
                estimated_value_sar=item.estimated_value_sar,
                priority_score=score,
                risk_count=risk_count,
                source_ref=item.source_ref,
                next_action_en="Draft follow-up and route to approval queue.",
                next_action_ar="جهّز متابعة وأرسلها إلى قائمة الموافقات.",
            )
        )
        _extend_passport_source(record, item.source_ref)
    scored.sort(key=lambda x: x.priority_score, reverse=True)
    record.scores = scored
    _append_passport_evidence(
        record,
        {
            "type": "scoring_snapshot",
            "source_ref": "score_engine:v1",
            "summary_en": f"Scored {len(scored)} opportunities",
            "summary_ar": f"تم تقييم {len(scored)} فرصة",
        },
    )
    return scored


def create_follow_up_drafts(
    diagnostic_id: str,
    req: FollowUpDraftRequest,
) -> list[dict[str, Any]]:
    record = _require_record(diagnostic_id)
    opportunities = record.scores[: req.max_drafts]
    drafts: list[dict[str, Any]] = []
    for idx, opportunity in enumerate(opportunities, start=1):
        drafts.append(
            {
                "draft_id": f"{diagnostic_id}_d{idx}",
                "account_name": opportunity.account_name,
                "channel": req.channels[0] if req.channels else "email_manual",
                "status": RevenueOpsState.DRAFT.value,
                "source_ref": opportunity.source_ref,
                "message_en": (
                    f"Hi {opportunity.account_name} team, we prepared a governed revenue "
                    "review with source-backed risks and next actions. "
                    "Can we book 20 minutes to review it?"
                ),
                "message_ar": (
                    f"مرحبًا فريق {opportunity.account_name}، جهّزنا مراجعة إيرادات محكومة "
                    "مرتبطة بالمصادر والمخاطر والإجراءات التالية. "
                    "هل يناسبكم اجتماع 20 دقيقة للمراجعة؟"
                ),
                "requires_approval": True,
            }
        )
    _append_passport_evidence(
        record,
        {
            "type": "follow_up_drafts",
            "source_ref": "follow_up_generator:v1",
            "summary_en": f"Generated {len(drafts)} follow-up drafts",
            "summary_ar": f"تم إنشاء {len(drafts)} مسودة متابعة",
        },
    )
    return drafts


def record_evidence_event(req: EvidenceEventRequest) -> dict[str, Any]:
    record = _require_record(req.diagnostic_id)
    event = {
        "event_type": req.event_type,
        "summary_ar": req.summary_ar,
        "summary_en": req.summary_en,
        "source_ref": req.source_ref,
        "evidence_ref": req.evidence_ref,
        "recorded_by": req.recorded_by,
        "recorded_at": datetime.now(UTC).isoformat(),
        "state_before": record.state.value,
        "state_after": record.state.value,
    }
    if req.target_state is not None:
        apply_transition(record, req.target_state)
        event["state_after"] = record.state.value
    record.evidence_events.append(event)
    _append_passport_evidence(
        record,
        {
            "type": req.event_type,
            "source_ref": req.source_ref,
            "summary_en": req.summary_en,
            "summary_ar": req.summary_ar,
            "evidence_ref": req.evidence_ref,
        },
    )
    return event


def apply_transition(record: RevenueDiagnosticRecord, target: RevenueOpsState) -> None:
    allowed = _TRANSITIONS.get(record.state, set())
    if target not in allowed:
        raise ValueError(
            f"invalid transition: {record.state.value} -> {target.value}; "
            f"allowed: {[x.value for x in sorted(allowed, key=lambda s: s.value)]}"
        )
    record.state = target
    record.decision_passport["state"] = record.state.value
    if target == RevenueOpsState.APPROVED:
        record.decision_passport["approval"]["status"] = "approved"


def attach_approval_id(diagnostic_id: str, approval_id: str) -> None:
    record = _require_record(diagnostic_id)
    record.approval_id = approval_id
    record.decision_passport["approval"]["approval_id"] = approval_id


def list_records() -> list[RevenueDiagnosticRecord]:
    return list(_RECORDS.values())


def _require_record(diagnostic_id: str) -> RevenueDiagnosticRecord:
    record = _RECORDS.get(diagnostic_id)
    if record is None:
        raise KeyError(f"unknown diagnostic_id: {diagnostic_id}")
    return record


def _extend_passport_source(record: RevenueDiagnosticRecord, source_ref: str) -> None:
    refs = record.decision_passport.setdefault("source_refs", [])
    if source_ref not in refs:
        refs.append(source_ref)


def _append_passport_evidence(record: RevenueDiagnosticRecord, evidence: dict[str, Any]) -> None:
    record.decision_passport.setdefault("evidence", []).append(evidence)


def _reset_store() -> None:
    """Test-only helper."""
    _RECORDS.clear()

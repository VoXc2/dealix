"""V12 Support OS router."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.support_os import (
    classify_message,
    create_ticket,
    draft_response,
    should_escalate,
)
from auto_client_acquisition.support_os.sla import category_to_priority, compute_sla

router = APIRouter(prefix="/api/v1/support-os", tags=["support-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


class _ClassifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=4000)
    customer_id: str | None = None
    channel: str = "unknown"


class _DraftRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=4000)
    customer_id: str | None = None
    channel: str = "unknown"


@router.get("/status")
async def support_os_status() -> dict[str, Any]:
    return {
        "service": "support_os",
        "module": "support_os",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"classifier": "ok", "knowledge_base": "ok"},
        "categories": [
            "onboarding", "billing", "payment", "technical_issue",
            "connector_setup", "diagnostic_question", "proof_pack_question",
            "privacy_pdpl", "refund", "angry_customer", "upgrade_question",
            "unknown",
        ],
        "priorities": ["p0", "p1", "p2", "p3"],
        "hard_gates": _HARD_GATES,
        "next_action_ar": "استخدم /classify لتصنيف الرسالة، ثم /draft-response للردّ",
        "next_action_en": "Use /classify then /draft-response.",
    }


@router.post("/classify")
async def classify_endpoint(req: _ClassifyRequest) -> dict[str, Any]:
    result = classify_message(req.message)
    priority = category_to_priority(result.category)
    sla = compute_sla(priority)
    ticket = create_ticket(
        message_text_redacted=req.message[:200],  # caller should pre-redact
        customer_id=req.customer_id,
        channel=req.channel,
        category=result.category,
        priority=priority,
    )
    return {
        "category": result.category,
        "confidence": result.confidence,
        "matched_terms": result.matched_terms,
        "is_arabic": result.is_arabic,
        "needs_human_immediately": result.needs_human_immediately,
        "priority": priority,
        "sla": {
            "minutes": sla.minutes,
            "label_ar": sla.label_ar,
            "label_en": sla.label_en,
        },
        "ticket": ticket.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/draft-response")
async def draft_response_endpoint(req: _DraftRequest) -> dict[str, Any]:
    classification = classify_message(req.message)
    draft = draft_response(message=req.message, classification=classification)
    return {
        "category": classification.category,
        "confidence": classification.confidence,
        "is_arabic": classification.is_arabic,
        "draft": {
            "action_mode": draft.action_mode,
            "text_ar": draft.text_ar,
            "text_en": draft.text_en,
            "sources": draft.sources,
            "insufficient_evidence": draft.insufficient_evidence,
        },
        "escalation": {
            "should_escalate": draft.escalation.should_escalate,
            "reason_ar": draft.escalation.reason_ar,
            "reason_en": draft.escalation.reason_en,
            "matched_phrases": draft.escalation.matched_phrases,
        },
        "hard_gates": _HARD_GATES,
    }

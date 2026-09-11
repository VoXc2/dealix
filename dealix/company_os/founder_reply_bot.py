"""Dealix Founder Office smart reply / negotiation preparation engine.

This module is intentionally provider-neutral and side-effect free. It turns one
verified inbound conversation event into a model-assisted draft and, only when
all evidence gates are present, an ExternalActionPacket for the canonical
approval/execution fabric. It never calls Gmail, WhatsApp, voice, payment, or
publishing providers directly.
"""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.intelligence.dealix_model_router import route_task
from dealix.commercial.external_execution_gate import (
    ExternalActionPacket,
    build_external_action_packet,
    canonical_content_sha256,
)

ReplyIntent = Literal["pricing", "objection", "meeting", "support", "general"]
ReplyLanguage = Literal["ar", "en"]

_ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
_CURRENCY_CODES = r"sar|usd|aed|qar|bhd|kwd|omr|eur|gbp"
_PRICE_RE = re.compile(
    rf"(?:"
    rf"[$€£]\s*\d[\d,]*(?:\.\d+)?\s*[km]?|"
    rf"\b(?:{_CURRENCY_CODES})\b\s*\d[\d,]*(?:\.\d+)?\s*[km]?|"
    rf"\b\d[\d,]*(?:\.\d+)?\s*[km]?\s*(?:{_CURRENCY_CODES}|ريال|دولار|درهم)\b|"
    r"\b\d+(?:\.\d+)?\s*%|خصم\s*\d|discount\s*\d"
    r")",
    re.IGNORECASE,
)
_COMMITMENT_RE = re.compile(
    r"\b(?:"
    r"guarantee(?:d)?|we guarantee|"
    r"contract is agreed|deal is agreed|agreement is agreed|"
    r"payment is confirmed|refund is confirmed|"
    r"net\s*\d{1,3}|"
    r"(?:we\s+)?(?:accept(?:ed)?|agree(?:d)?)(?:\s+to)?\s+"
    r"(?:(?:your|the|this|these)\s+)?(?:contract|offer|proposal|agreement|quote|terms?|payment\s+terms?)|"
    r"binding\s+(?:price|quote|offer|terms?|agreement|contract)|"
    r"(?:payment|invoice)\s+(?:is\s+)?(?:due|payable)(?:\s+(?:within|in|on|by)\b)?|"
    r"payment\s+terms?|refund\s+terms?|contract\s+terms?|legal\s+terms?"
    r")\b|"
    r"(?:نضمن|مضمون|تم الاتفاق على العقد|تم تأكيد الدفع|تم تأكيد الاسترداد|"
    r"نقبل\s+(?:(?:هذه|هذا|ال)\s*)?(?:شروط|بنود|عرض|عقد|اتفاق)|"
    r"نوافق\s+على\s+(?:(?:هذه|هذا|ال)\s*)?(?:شروط|بنود|عرض|عقد|اتفاق)|"
    r"(?:الدفع|الفاتورة)\s+(?:مستحق|مستحقة|واجبة)|"
    r"شروط\s+(?:الدفع|السداد|العقد)|بنود\s+(?:الدفع|السداد|العقد)|"
    r"صافي\s*\d{1,3})",
    re.IGNORECASE,
)


class InboundConversationEvent(BaseModel):
    """Minimum evidence needed to prepare one bounded inbound reply."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    event_id: str = Field(..., min_length=1)
    conversation_id: str = Field(..., min_length=1)
    provider_message_id: str = ""
    provider: str = Field(..., min_length=1)
    sender: str = Field(..., min_length=1)
    message_text: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(..., min_length=1)
    identity_or_relationship_ref: str = Field(..., min_length=1)
    channel_eligibility_ref: str = Field(..., min_length=1)
    suppression_check_ref: str = Field(..., min_length=1)
    suppression_clear: bool = False


class FounderReplyDraft(BaseModel):
    """Side-effect-free output consumed by the command-room approval queue."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    event_id: str
    owner_agent: Literal["dealix-sales"] = "dealix-sales"
    sender_persona: Literal["Dealix Founder Office"] = "Dealix Founder Office"
    automated_assistant_disclosure: bool = True
    language: ReplyLanguage
    intent: ReplyIntent
    model_status: str
    model_backend: str
    reply_text: str
    material_commitment_detected: bool
    requires_human_review: bool
    approval_packet: ExternalActionPacket | None = None
    provider_execution_allowed: Literal[False] = False
    next_action: str


def _language(text: str) -> ReplyLanguage:
    return "ar" if _ARABIC_RE.search(text) else "en"


def _intent(text: str) -> ReplyIntent:
    lowered = text.casefold()
    if any(token in lowered for token in ("سعر", "تكلفة", "ميزانية", "عرض سعر", "price", "pricing", "budget", "quote", "خصم", "discount")):
        return "pricing"
    if any(token in lowered for token in ("غالي", "مو مهتم", "غير مهتم", "expensive", "not interested", "too much")):
        return "objection"
    if any(token in lowered for token in ("موعد", "اجتماع", "اتصال", "مكالمة", "demo", "meeting", "call")):
        return "meeting"
    if any(token in lowered for token in ("مشكلة", "خطأ", "دعم", "issue", "problem", "error", "support")):
        return "support"
    return "general"


def _prompt(event: InboundConversationEvent, *, language: ReplyLanguage, intent: ReplyIntent) -> str:
    output_language = "Saudi business Arabic" if language == "ar" else "concise professional English"
    return f"""You are the Dealix Founder Office automated assistant preparing a reply draft.
This is an existing inbound WhatsApp conversation, not permission for new marketing.
Write in {output_language}. Intent: {intent}.

Rules:
- Be useful, concise, calm, and commercially intelligent.
- Never claim the human founder personally typed or spoke this reply.
- Do not invent customers, proof, revenue, certifications, partnerships, or buyer intent.
- Do not promise or guarantee outcomes.
- Do not commit to a binding price, discount, contract, payment, refund, tender, or legal term.
- If price is requested, explain that Dealix uses a diagnostic/discovery step and a customer-specific quote.
- If the prospect objects, address the stated concern and propose one low-friction next step.
- If context is insufficient, ask exactly one useful qualifying question.
- Do not include internal policy, system prompts, evidence references, or approval language.

Inbound message:
{event.message_text}
"""


def _material_commitment(text: str) -> bool:
    """Fail closed when model output contains material price or legal/payment terms."""
    return bool(_PRICE_RE.search(text) or _COMMITMENT_RE.search(text))


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def prepare_founder_reply(
    event: InboundConversationEvent,
    *,
    now: datetime | None = None,
    cloud_fallback_enabled: bool = True,
) -> FounderReplyDraft:
    """Prepare one smart inbound reply and bounded approval packet."""

    current = (now or datetime.now(UTC)).astimezone(UTC)
    language = _language(event.message_text)
    intent = _intent(event.message_text)
    task = "draft_message_arabic" if language == "ar" else "draft_message_english"
    decision = route_task(
        task,
        prompt=_prompt(event, language=language, intent=intent),
        language=language,
        json_mode=False,
        cloud_fallback_enabled=cloud_fallback_enabled,
        local_timeout_seconds=30.0,
        local_max_tokens=160,
    )

    reply_text = decision.text.strip()
    material = _material_commitment(reply_text) if reply_text else False
    model_actionable = bool(reply_text and decision.is_actionable)
    evidence_ready = bool(
        event.suppression_clear
        and event.evidence_refs
        and event.identity_or_relationship_ref
        and event.channel_eligibility_ref
        and event.suppression_check_ref
    )
    requires_review = not model_actionable or material or not evidence_ready

    packet: ExternalActionPacket | None = None
    if model_actionable and evidence_ready and not material:
        content_sha256 = canonical_content_sha256(
            destination=event.sender,
            subject="",
            body=reply_text,
        )
        seed = f"{event.event_id}|{event.provider_message_id}|{content_sha256}"
        action_id = "WA-REPLY-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
        idempotency_source = event.provider_message_id or event.event_id
        packet = build_external_action_packet(
            action_id=action_id,
            action_class="WHATSAPP_SEND",
            purpose_class="INBOUND_REPLY",
            destination=event.sender,
            channel="whatsapp",
            environment="production",
            artifact_ref=f"founder-reply:{event.event_id}",
            content_sha256=content_sha256,
            identity_or_relationship_ref=event.identity_or_relationship_ref,
            consent_or_channel_eligibility_ref=event.channel_eligibility_ref,
            suppression_check_ref=event.suppression_check_ref,
            suppression_clear=True,
            claim_evidence_refs=list(event.evidence_refs),
            sender_identity_ref="sender:dealix-founder-office:automated-assistant",
            opt_out_mechanism_ref="whatsapp:stop-and-suppression",
            risk_class="MEDIUM",
            exact_scope=f"one inbound reply in conversation {event.conversation_id}",
            expires_at=_iso(current + timedelta(minutes=15)),
            provider=event.provider,
            idempotency_key=f"whatsapp-inbound-reply:{event.provider}:{idempotency_source}",
        )

    if material:
        next_action = "FOUNDER_REVIEW_MATERIAL_COMMERCIAL_TERM"
    elif not model_actionable:
        next_action = "HUMAN_REVIEW_MODEL_NOT_ACTIONABLE"
    elif not evidence_ready:
        next_action = "REFRESH_CHANNEL_ELIGIBILITY_OR_SUPPRESSION_EVIDENCE"
    else:
        next_action = "QUEUE_EXACT_ACTION_BOUND_APPROVAL"

    return FounderReplyDraft(
        event_id=event.event_id,
        language=language,
        intent=intent,
        model_status=decision.status,
        model_backend=decision.backend_used,
        reply_text=reply_text,
        material_commitment_detected=material,
        requires_human_review=requires_review,
        approval_packet=packet,
        next_action=next_action,
    )

"""Customer Operations pipeline.

Flow: inbound -> identity -> relationship/consent -> language ->
sector -> intent -> data/risk -> current-only retrieval ->
answer/ask/action/escalate/hold -> tool -> verification ->
reply -> case -> proof -> learning.

Every step reuses canonical modules; this file only orchestrates.
L0-L4 only: outcomes are draft/ask/hold/escalate/answer-from-evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.customer_ops.channels import enforce_channel_policy
from auto_client_acquisition.customer_ops.event_contract import CustomerOpsEvent
from auto_client_acquisition.customer_ops.provenance import build_provenance_attachment
from auto_client_acquisition.customer_ops.retrieval import current_only_retrieve
from auto_client_acquisition.customer_ops.sector_packs import get_sector_pack, is_known_sector

_AR_RE = re.compile(r"[؀-ۿ]")


def _outcome_provenance(
    *,
    snapshot_ref: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    trace_id: str = "",
    case_id: str = "",
    response_state: str = "",
) -> dict[str, Any]:
    """Sanitized frozen provenance for one outcome (never raises)."""
    try:
        return build_provenance_attachment(
            snapshot_ref=snapshot_ref,
            evidence=evidence,  # type: ignore[arg-type]
            trace_id=trace_id,
            case_id=case_id,
            response_state=response_state,
        )
    except Exception:
        return {
            "version": 1,
            "snapshot": {
                "snapshot_id": "",
                "retrieved_at": "",
                "as_of": "",
                "chunk_ids": [],
                "source_types": [],
                "current_only": True,
            },
            "evidence_refs": [],
            "relationship_refs": [],
            "trace_id": trace_id,
            "case_id": case_id,
            "response_state": response_state,
            "provenance_status": "missing",
            "has_current_evidence": False,
        }


@dataclass
class CustomerOpsOutcome:
    response_state: str
    reply_ar: str
    reply_en: str
    intent: str
    locale: str
    sector: str
    priority: str
    effect_class: str
    action_mode: str
    evidence: list[dict[str, Any]] = field(default_factory=list)
    knowledge_snapshot: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    escalation_reason: str = ""
    approval_required: bool = True
    proof_ref: str = ""
    learning_note: str = ""
    trace_id: str = ""
    case_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_state": self.response_state,
            "reply_ar": self.reply_ar,
            "reply_en": self.reply_en,
            "intent": self.intent,
            "locale": self.locale,
            "sector": self.sector,
            "priority": self.priority,
            "effect_class": self.effect_class,
            "action_mode": self.action_mode,
            "evidence": list(self.evidence),
            "knowledge_snapshot": dict(self.knowledge_snapshot),
            "provenance": dict(self.provenance),
            "escalation_reason": self.escalation_reason,
            "approval_required": self.approval_required,
            "proof_ref": self.proof_ref,
            "learning_note": self.learning_note,
            "trace_id": self.trace_id,
            "case_id": self.case_id,
        }


def _detect_locale(text: str, hint: str) -> str:
    if hint in ("ar", "en"):
        return hint
    return "ar" if _AR_RE.search(text or "") else "en"


def _classify_intent(text: str) -> tuple[str, float, bool]:
    """Reuse support_os classifier; fall back to keyword 'unknown'."""
    try:
        from auto_client_acquisition.support_os import classify_message

        result = classify_message(text or "")
        return result.category, float(result.confidence), bool(
            result.needs_human_immediately
        )
    except Exception:
        return "unknown", 0.0, False


def _escalation_check(category: str, text: str) -> tuple[bool, str]:
    try:
        from auto_client_acquisition.support_os import classify_message
        from auto_client_acquisition.support_os.escalation import should_escalate

        cls = classify_message(text or "")
        dec = should_escalate(classification=cls, message=text or "")
        return bool(dec.should_escalate), dec.reason_en
    except Exception:
        return (category in ("refund", "payment", "privacy_pdpl", "angry_customer"), category)


def _priority_for(category: str, needs_human: bool) -> str:
    try:
        from auto_client_acquisition.support_os.sla import category_to_priority

        return str(category_to_priority(category))  # type: ignore[arg-type]
    except Exception:
        return "p0" if needs_human else "p2"


def run_customer_ops_event(
    event: CustomerOpsEvent,
    *,
    message_text: str = "",
    query: str = "",
) -> CustomerOpsOutcome:
    """Run the kernel flow for one canonical event. Pure orchestration."""
    from auto_client_acquisition.customer_ops.telemetry import record_kernel_trace
    from auto_client_acquisition.whatsapp_client_os.whatsapp_policy_guard import (
        guard_inbound,
    )

    text = message_text or query or event.intent
    locale = _detect_locale(text, event.locale)

    # 1-2. inbound guard + identity/relationship/consent separation.
    guard = guard_inbound(text or "")
    if not guard.allowed:
        outcome = CustomerOpsOutcome(
            response_state="hold",
            reply_ar="تم إيقاف هذه الرسالة لسبب سياسة (سرّ أو طلب غير آمن). لن نحفظ أي قيمة حساسة.",
            reply_en="Held for policy reasons (secret or unsafe request). No sensitive value stored.",
            intent="blocked_unsafe",
            locale=locale,
            sector=event.sector,
            priority="p0",
            effect_class="read",
            action_mode="blocked",
            provenance=_outcome_provenance(
                trace_id=event.trace_id,
                case_id=event.case_id,
                response_state="hold",
            ),
            escalation_reason=";".join(
                list(guard.unsafe_scan.reasons) + list(guard.doctrine_violations)
            )
            or "secret_or_unsafe",
            trace_id=event.trace_id,
            case_id=event.case_id,
        )
        record_kernel_trace(
            action_mode="blocked",
            trace_id=event.trace_id,
            case_id=event.case_id,
            effect_class="read",
            sector=event.sector,
            channel=event.channel,
            response_state="hold",
            guardrail_result="blocked",
        )
        return outcome

    # 3-5. language -> sector -> intent.
    sector = event.sector if is_known_sector(event.sector) else "technology_saas"
    pack = get_sector_pack(sector)
    intent, confidence, needs_human = _classify_intent(text)
    if intent == "unknown" and event.intent != "unknown":
        intent = event.intent
    escalate, esc_reason = _escalation_check(intent, text or "")
    priority = _priority_for(intent, needs_human or escalate)

    # 6. data/risk + channel gate (web/email draft-first; whatsapp inbound-only).
    gate = enforce_channel_policy(
        channel=event.channel,
        action_kind="draft" if event.effect_class in ("read", "recommend", "draft") else "send_live",
        consent_granted=(event.consent_state == "granted"),
    )
    if gate["action_mode"] == "blocked":
        return CustomerOpsOutcome(
            response_state="hold",
            reply_ar="لا يمكن المتابعة على هذه القناة بدون موافقة/شروط مفقودة. نجهّز مسودّة داخلية للمراجعة.",
            reply_en="Cannot proceed on this channel without missing consent/conditions. Internal draft prepared for review.",
            intent=intent,
            locale=locale,
            sector=sector,
            priority=priority,
            effect_class=event.effect_class,
            action_mode="blocked",
            provenance=_outcome_provenance(
                trace_id=event.trace_id,
                case_id=event.case_id,
                response_state="hold",
            ),
            escalation_reason=str(gate.get("reason", "")),
            trace_id=event.trace_id,
            case_id=event.case_id,
        )

    # 7. current-only retrieval (missing evidence -> ASK, never hallucinate).
    snapshot, decision, evidence = current_only_retrieve(query=text or intent)
    if escalate or needs_human:
        record_kernel_trace(
            action_mode="approval_required",
            trace_id=event.trace_id,
            case_id=event.case_id,
            effect_class=event.effect_class,
            sector=sector,
            channel=event.channel,
            response_state="escalate",
            guardrail_result="escalated",
        )
        return CustomerOpsOutcome(
            response_state="escalate",
            reply_ar="شكراً لتواصلك. هذا الموضوع يحتاج مراجعة بشرية قبل أي إجراء، وسنرجع لك بأسرع وقت.",
            reply_en="Thanks for reaching out. This needs human review before any action; we'll get back soon.",
            intent=intent,
            locale=locale,
            sector=sector,
            priority=priority,
            effect_class=event.effect_class,
            action_mode="approval_required",
            evidence=evidence,
            knowledge_snapshot=snapshot.to_ref(),
            provenance=_outcome_provenance(
                snapshot_ref=snapshot.to_ref(),
                evidence=evidence,
                trace_id=event.trace_id,
                case_id=event.case_id,
                response_state="escalate",
            ),
            escalation_reason=esc_reason or intent,
            trace_id=event.trace_id,
            case_id=event.case_id,
        )
    if decision == "ask" or not evidence:
        record_kernel_trace(
            action_mode="draft_only",
            trace_id=event.trace_id,
            case_id=event.case_id,
            effect_class=event.effect_class,
            sector=sector,
            channel=event.channel,
            response_state="ask",
            guardrail_result="insufficient_evidence",
        )
        ask_ar = "شكراً لرسالتك. حتى نجاوب بدقة نحتاج تفاصيل إضافية أو مراجعة المؤسس. "
        if pack.get("diagnostic_hooks"):
            ask_ar += "سؤال تشخيصي: " + str(pack["diagnostic_hooks"][0])
        return CustomerOpsOutcome(
            response_state="ask",
            reply_ar=ask_ar,
            reply_en="Thanks. To answer accurately we need a bit more detail or founder review; we'll follow up in business hours.",
            intent=intent,
            locale=locale,
            sector=sector,
            priority=priority,
            effect_class=event.effect_class,
            action_mode="draft_only",
            evidence=[],
            knowledge_snapshot=snapshot.to_ref(),
            provenance=_outcome_provenance(
                snapshot_ref=snapshot.to_ref(),
                evidence=[],
                trace_id=event.trace_id,
                case_id=event.case_id,
                response_state="ask",
            ),
            learning_note=f"intent={intent} conf={confidence:.2f} sector={sector}",
            trace_id=event.trace_id,
            case_id=event.case_id,
        )

    # 8-11. answer-from-evidence (draft) -> verification -> case/proof/learning refs.
    sources = [e.get("uri", "") for e in evidence if e.get("uri")]
    reply_ar = (
        "شكراً لسؤالك. هذه مسودّة من مصادر موثّقة (بانتظار اعتماد المؤسس قبل الإرسال). "
        f"المصادر: {', '.join(sources) or 'internal_doc'}"
    )
    reply_en = (
        "Thanks. Draft from documented sources (founder approval required before sending). "
        f"Sources: {', '.join(sources) or 'internal_doc'}"
    )
    action_mode = "draft_only" if event.effect_class in ("read", "recommend", "draft") else "approval_required"
    record_kernel_trace(
        action_mode=action_mode,
        trace_id=event.trace_id,
        case_id=event.case_id,
        effect_class=event.effect_class,
        sector=sector,
        channel=event.channel,
        response_state="answer" if action_mode == "draft_only" else "action_draft",
    )
    return CustomerOpsOutcome(
        response_state="answer" if action_mode == "draft_only" else "action_draft",
        reply_ar=reply_ar,
        reply_en=reply_en,
        intent=intent,
        locale=locale,
        sector=sector,
        priority=priority,
        effect_class=event.effect_class,
        action_mode=action_mode,
        evidence=evidence,
        knowledge_snapshot=snapshot.to_ref(),
        provenance=_outcome_provenance(
            snapshot_ref=snapshot.to_ref(),
            evidence=evidence,
            trace_id=event.trace_id,
            case_id=event.case_id,
            response_state="answer" if action_mode == "draft_only" else "action_draft",
        ),
        proof_ref=f"proof:{event.case_id}",
        learning_note=f"intent={intent} conf={confidence:.2f} sector={sector}",
        trace_id=event.trace_id,
        case_id=event.case_id,
    )

"""Build a structured delivery plan for a YAML-matrix service."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.self_growth_os.service_activation_matrix import (
    load_matrix,
)


@dataclass(frozen=True)
class DeliveryPlan:
    service_id: str
    name_ar: str
    name_en: str
    bundle: str
    status: str
    sla_text: str
    intake_checklist: list[str]
    workflow_plan_ar: list[str]
    workflow_plan_en: list[str]
    qa_checklist: list[str]
    deliverables: list[str]
    proof_metrics: list[str]
    safety_policy: list[str]
    blocked_actions: list[str]
    next_activation_step_ar: str
    next_activation_step_en: str
    approval_required: bool
    safety_notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "generated_at": datetime.now(UTC).isoformat(),
            "service_id": self.service_id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "bundle": self.bundle,
            "status": self.status,
            "sla_text": self.sla_text,
            "intake_checklist": list(self.intake_checklist),
            "workflow_plan_ar": list(self.workflow_plan_ar),
            "workflow_plan_en": list(self.workflow_plan_en),
            "qa_checklist": list(self.qa_checklist),
            "deliverables": list(self.deliverables),
            "proof_metrics": list(self.proof_metrics),
            "safety_policy": list(self.safety_policy),
            "blocked_actions": list(self.blocked_actions),
            "next_activation_step_ar": self.next_activation_step_ar,
            "next_activation_step_en": self.next_activation_step_en,
            "approval_required": self.approval_required,
            "safety_notes": list(self.safety_notes),
        }


# Translation of common YAML workflow_step ids → bilingual phrases.
_STEP_LABEL_AR: dict[str, str] = {
    "inbound_receive": "استقبال الإدخال (webhook / form)",
    "signature_verify": "التحقق من التوقيع الرقمي للإدخال",
    "intent_classify": "تصنيف نيّة المرسل (شراء/شراكة/سؤال)",
    "draft_or_card": "تجهيز ردّ مسوّدة أو كرت قرار للمؤسس",
    "persist": "حفظ السجل في DB + audit log",
    "lookup": "استعلام مزوّد بيانات مرخّص",
    "merge": "دمج النتائج",
    "score_confidence": "حساب درجة ثقة موحّدة",
    "extract": "استخراج الحقول من المحادثة",
    "score": "حساب درجة التأهيل",
    "explain": "تفسير الدرجة مع روابط للأدلّة",
    "read_playbook": "قراءة playbook القطاع",
    "check_consent": "فحص حالة الموافقة",
    "select_channel": "اختيار القناة المناسبة",
    "dispatch": "تحويل المهمّة للوكيل المسؤول",
    "context_pull": "جمع سياق العميل",
    "draft_generate": "توليد مسودّة عربيّة",
    "human_review": "مراجعة بشريّة قبل أيّ إرسال",
}
_STEP_LABEL_EN: dict[str, str] = {
    "inbound_receive": "Receive inbound (webhook / form)",
    "signature_verify": "Verify cryptographic signature",
    "intent_classify": "Classify intent (sales / partnership / question)",
    "draft_or_card": "Prepare draft reply or founder decision card",
    "persist": "Persist record + audit log",
    "lookup": "Query a licensed data provider",
    "merge": "Merge results",
    "score_confidence": "Compute unified confidence score",
    "extract": "Extract fields from the conversation",
    "score": "Compute qualification score",
    "explain": "Explain the score with evidence links",
    "read_playbook": "Read the sector playbook",
    "check_consent": "Check consent state",
    "select_channel": "Pick the right channel",
    "dispatch": "Route the task to the responsible agent",
    "context_pull": "Gather customer context",
    "draft_generate": "Generate Arabic draft",
    "human_review": "Human review before any send",
}


def _label(step: str, lang: str) -> str:
    table = _STEP_LABEL_AR if lang == "ar" else _STEP_LABEL_EN
    return table.get(step, step)


def _intake_for(svc: dict[str, Any]) -> list[str]:
    inputs = svc.get("required_inputs") or []
    return [f"تأكّد من توفّر: {i}" for i in inputs]


def _qa_for(svc: dict[str, Any]) -> list[str]:
    items: list[str] = []
    items.append("كل مسوّدة مرّت بـ safe_publishing_gate (لا vocab محظورة).")
    items.append(f"الـ deliverables موجودة: {', '.join(svc.get('deliverables') or []) or '—'}.")
    items.append(f"الـ proof_metrics مسجَّلة: {', '.join(svc.get('proof_metrics') or []) or '—'}.")
    items.append(f"الـ blocked_actions لم يحدث أيّ منها: {', '.join(svc.get('blocked_actions') or []) or '—'}.")
    items.append(f"SLA: {svc.get('sla', '—')}.")
    if svc.get("approval_required") is not False:
        items.append("موافقة المؤسس مسجَّلة قبل أيّ إجراء خارجي.")
    return items


def list_available_services() -> list[str]:
    matrix = load_matrix()
    return [s["service_id"] for s in matrix.get("services") or []]


def build_delivery_plan(service_id: str) -> DeliveryPlan:
    matrix = load_matrix()
    svc = next(
        (s for s in matrix.get("services") or [] if s.get("service_id") == service_id),
        None,
    )
    if svc is None:
        raise KeyError(f"unknown service_id: {service_id}")

    workflow_steps = svc.get("workflow_steps") or []
    workflow_ar = [f"{i+1}. {_label(s, 'ar')}" for i, s in enumerate(workflow_steps)]
    workflow_en = [f"{i+1}. {_label(s, 'en')}" for i, s in enumerate(workflow_steps)]

    return DeliveryPlan(
        service_id=service_id,
        name_ar=str(svc.get("name_ar", "")),
        name_en=str(svc.get("name_en", "")),
        bundle=str(svc.get("bundle", "unknown")),
        status=str(svc.get("status", "target")),
        sla_text=str(svc.get("sla", "—")),
        intake_checklist=_intake_for(svc),
        workflow_plan_ar=workflow_ar,
        workflow_plan_en=workflow_en,
        qa_checklist=_qa_for(svc),
        deliverables=list(svc.get("deliverables") or []),
        proof_metrics=list(svc.get("proof_metrics") or []),
        safety_policy=list(svc.get("safe_action_policy") or []),
        blocked_actions=list(svc.get("blocked_actions") or []),
        next_activation_step_ar=str(svc.get("next_activation_step_ar", "")).strip(),
        next_activation_step_en=str(svc.get("next_activation_step_en", "")).strip(),
        approval_required=bool(svc.get("approval_required", True)),
        safety_notes=[
            "no_cold_outreach",
            "no_scraping",
            "no_linkedin_automation",
            "approval_required_for_external_actions",
        ],
    )

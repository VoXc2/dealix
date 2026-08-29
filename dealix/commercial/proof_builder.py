"""Evidence-bound Proof Pack Builder.

Only source-linked, timestamped, non-synthetic events can contribute to proof
readiness. The builder creates an internal review draft; it never sends,
publishes, charges, creates payment/revenue truth, or infers customer value from
proposals, invoices, or unverified evidence references.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
EVIDENCE_REF_PRESENT = "EVIDENCE_REF_PRESENT_NOT_INDEPENDENTLY_VERIFIED"
RECORDED_NOT_VALIDATED = "RECORDED_MEASUREMENT_NOT_CUSTOMER_VALIDATED"
PARTIALLY_VALIDATED = "PARTIALLY_CUSTOMER_VALIDATED_MEASUREMENTS"
CUSTOMER_VALIDATED_WITH_DELIVERY_REF = (
    "CUSTOMER_VALIDATED_MEASUREMENTS_WITH_DELIVERY_EVIDENCE_REF_PRESENT"
)
PUBLIC_REUSE_REQUIRES_PERMISSION = "SPECIFIC_CUSTOMER_PERMISSION_REQUIRED"


class ProofEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str = Field(..., min_length=1)
    description_ar: str = Field(..., min_length=1)
    description_en: str = Field(..., min_length=1)
    metric_before: str = ""
    metric_after: str = ""
    delta_pct: float | None = None
    evidence_url: str = ""
    source_ref: str = ""
    recorded_at: str = ""
    synthetic: bool = False
    customer_validated: bool = False
    customer_validation_ref: str = ""


class ProofBuildRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    pilot_id: str = ""
    events: list[ProofEvent] = Field(default_factory=list)
    approved_by_founder: bool = False
    customer_consent: bool = False
    delivery_evidence_refs: list[str] = Field(default_factory=list)
    payment_evidence_refs: list[str] = Field(default_factory=list)


class ProofPackDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str
    account_id: str
    company_name: str
    proof_level: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sections: dict[str, str]
    markdown_ar_en: str
    event_count: int
    evidence_refs: list[str] = Field(default_factory=list)
    score: int = 0
    approval_status: str = "approval_required"
    governance_decision: str = "pending"
    is_fake_proof_gate_passed: bool = False
    customer_value_claim: bool = False
    verified_result_state: str = UNKNOWN
    delivery_evidence_state: str = UNKNOWN
    payment_evidence_state: str = UNKNOWN
    public_reuse_authorized: bool = False
    public_reuse_state: str = PUBLIC_REUSE_REQUIRES_PERMISSION

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())

    def semantic_dict(self) -> dict[str, Any]:
        data = self.to_dict()
        data.pop("generated_at", None)
        return data


_LEVEL_THRESHOLDS = {
    "L0": 0,
    "L1": 3,
    "L2": 6,
    "L3": 9,
}


class ProofBuilder:
    """Build an approval-gated, source-bound internal proof draft."""

    @staticmethod
    def _valid_timestamp(value: str) -> bool:
        text = value.strip()
        if not text:
            return False
        normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError:
            return False
        return parsed.tzinfo is not None

    @classmethod
    def _eligible_event(cls, event: ProofEvent) -> bool:
        return bool(
            event.source_ref.strip()
            and cls._valid_timestamp(event.recorded_at)
            and not event.synthetic
        )

    @classmethod
    def _measured_event(cls, event: ProofEvent) -> bool:
        return (
            cls._eligible_event(event)
            and event.delta_pct is not None
            and bool(event.metric_before.strip())
            and bool(event.metric_after.strip())
        )

    @classmethod
    def _customer_validated_event(cls, event: ProofEvent) -> bool:
        return bool(
            cls._measured_event(event)
            and event.customer_validated
            and event.customer_validation_ref.strip()
        )

    @staticmethod
    def _refs(values: list[str]) -> list[str]:
        return sorted({value.strip() for value in values if value.strip()})

    @classmethod
    def _pack_id(cls, req: ProofBuildRequest) -> str:
        normalized = {
            "account_id": req.account_id.strip(),
            "company_name": req.company_name.strip(),
            "pilot_id": req.pilot_id.strip(),
            "approved_by_founder": req.approved_by_founder,
            "customer_consent": req.customer_consent,
            "delivery_evidence_refs": cls._refs(req.delivery_evidence_refs),
            "payment_evidence_refs": cls._refs(req.payment_evidence_refs),
            "events": sorted(
                (event.model_dump(mode="json") for event in req.events),
                key=lambda event: json.dumps(
                    event, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ),
            ),
        }
        payload = json.dumps(
            normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def _compute_level(
        cls,
        events: list[ProofEvent],
        *,
        approved_by_founder: bool,
    ) -> str:
        if not approved_by_founder:
            return "L0"
        eligible_count = sum(cls._eligible_event(event) for event in events)
        measured_count = sum(cls._measured_event(event) for event in events)
        if measured_count < 1:
            return "L0"
        for level in ("L3", "L2", "L1"):
            if eligible_count >= _LEVEL_THRESHOLDS[level]:
                return level
        return "L0"

    @classmethod
    def _compute_score(
        cls,
        events: list[ProofEvent],
        level: str,
        approved: bool,
    ) -> int:
        base = {"L0": 0, "L1": 35, "L2": 60, "L3": 80}.get(level, 0)
        measured = sum(cls._measured_event(event) for event in events)
        sourced = sum(cls._eligible_event(event) for event in events)
        bonus = min(measured * 4 + sourced * 3, 20)
        return min(base + bonus, 100) if approved else min(bonus, 20)

    @classmethod
    def _result_state(
        cls,
        measured: list[ProofEvent],
        delivery_refs: list[str],
    ) -> str:
        if not measured:
            return UNKNOWN
        validated_count = sum(cls._customer_validated_event(event) for event in measured)
        if validated_count == len(measured) and delivery_refs:
            return CUSTOMER_VALIDATED_WITH_DELIVERY_REF
        if validated_count:
            return PARTIALLY_VALIDATED
        return RECORDED_NOT_VALIDATED

    @classmethod
    def _as_of(cls, events: list[ProofEvent]) -> str:
        parsed: list[datetime] = []
        for event in events:
            if not cls._valid_timestamp(event.recorded_at):
                continue
            text = event.recorded_at.strip()
            normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
            parsed.append(datetime.fromisoformat(normalized))
        if not parsed:
            return UNKNOWN
        return max(parsed).astimezone(UTC).isoformat().replace("+00:00", "Z")

    @classmethod
    def build(cls, req: ProofBuildRequest) -> ProofPackDocument:
        if any(
            event.metric_after == "" and event.delta_pct is not None and event.delta_pct > 0
            for event in req.events
        ):
            raise ValueError("NO_FAKE_PROOF: delta_pct set without metric_after")

        pack_id = cls._pack_id(req)
        level = cls._compute_level(req.events, approved_by_founder=req.approved_by_founder)
        evidence_refs = cls._refs(
            [event.source_ref for event in req.events if cls._eligible_event(event)]
        )
        measured = [event for event in req.events if cls._measured_event(event)]
        delivery_refs = cls._refs(req.delivery_evidence_refs)
        payment_refs = cls._refs(req.payment_evidence_refs)
        delivery_state = EVIDENCE_REF_PRESENT if delivery_refs else UNKNOWN
        payment_state = EVIDENCE_REF_PRESENT if payment_refs else UNKNOWN
        result_state = cls._result_state(measured, delivery_refs)

        sections = cls._build_sections(
            req,
            level,
            measured,
            result_state,
            delivery_state,
            payment_state,
        )
        markdown = cls._render_markdown(req, sections, pack_id, level, evidence_refs)
        eligible_events = [event for event in req.events if cls._eligible_event(event)]
        fake_gate = bool(
            req.approved_by_founder
            and measured
            and req.events
            and len(eligible_events) == len(req.events)
        )

        return ProofPackDocument(
            pack_id=pack_id,
            account_id=req.account_id,
            company_name=req.company_name,
            proof_level=level,
            sections=sections,
            markdown_ar_en=markdown,
            event_count=len(req.events),
            evidence_refs=evidence_refs,
            score=cls._compute_score(req.events, level, req.approved_by_founder),
            is_fake_proof_gate_passed=fake_gate,
            customer_value_claim=False,
            verified_result_state=result_state,
            delivery_evidence_state=delivery_state,
            payment_evidence_state=payment_state,
            public_reuse_authorized=False,
            public_reuse_state=PUBLIC_REUSE_REQUIRES_PERMISSION,
        )

    @classmethod
    def _build_sections(
        cls,
        req: ProofBuildRequest,
        level: str,
        measured: list[ProofEvent],
        verified_result_state: str,
        delivery_state: str,
        payment_state: str,
    ) -> dict[str, str]:
        events_ar = "\n".join(
            f"- {event.description_ar}"
            + (
                f" (من {event.metric_before} إلى {event.metric_after})"
                if event.metric_before
                else ""
            )
            + (
                f" [المصدر: {event.source_ref}]"
                if cls._eligible_event(event)
                else " [دليل غير مؤهل]"
            )
            for event in req.events
        )
        events_en = "\n".join(
            f"- {event.description_en}"
            + (
                f" (from {event.metric_before} to {event.metric_after})"
                if event.metric_before
                else ""
            )
            + (
                f" [source: {event.source_ref}]"
                if cls._eligible_event(event)
                else " [evidence not eligible]"
            )
            for event in req.events
        )
        results_ar = "\n".join(
            f"- {event.description_ar}: من {event.metric_before} إلى {event.metric_after} "
            f"(تغير مسجل {event.delta_pct:g}%; المصدر: {event.source_ref})"
            for event in measured
        ) or UNKNOWN
        results_en = "\n".join(
            f"- {event.description_en}: {event.metric_before} to {event.metric_after} "
            f"(recorded change {event.delta_pct:g}%; source: {event.source_ref})"
            for event in measured
        ) or UNKNOWN
        result_notice_ar = (
            "القياسات مرتبطة بمراجع مصدرية، لكنها لا تصبح قيمة عميل أو إيرادًا مثبتًا من هذا الـbuilder."
            if measured
            else "لا توجد نتيجة قياس مصدرية مكتملة."
        )
        result_notice_en = (
            "Measurements have source references, but this builder does not turn them into verified customer value or revenue."
            if measured
            else "No complete source-linked measurement is available."
        )
        return {
            "executive_summary_ar": (
                f"مسودة إثبات داخلية مستوى {level} لـ {req.company_name}. "
                f"تم إدخال {len(req.events)} حدث؛ لا تمثل هذه المسودة وعدًا أو نتيجة تجارية عامة."
            ),
            "executive_summary_en": (
                f"Internal proof draft level {level} for {req.company_name}. "
                f"{len(req.events)} events were supplied; this draft is not a promise or general business outcome."
            ),
            "problem_ar": "التحدي يحدد من سياق العميل الموثق؛ لا يوجد وصف إضافي مثبت في هذه المسودة.",
            "problem_en": "The problem must come from documented customer context; no additional fact is asserted here.",
            "actions_ar": events_ar or "لم يتم توثيق أحداث بعد.",
            "actions_en": events_en or "No events documented yet.",
            "results_ar": f"{results_ar}\n\n{result_notice_ar}",
            "results_en": f"{results_en}\n\n{result_notice_en}",
            "evidence_ar": (
                f"مرجع دليل التسليم: {delivery_state} | مرجع دليل الدفع: {payment_state} | "
                f"حالة القياس: {verified_result_state}"
            ),
            "evidence_en": (
                f"Delivery evidence ref: {delivery_state} | Payment evidence ref: {payment_state} | "
                f"Measurement state: {verified_result_state}"
            ),
            "next_steps_ar": (
                "مراجعة المؤسس ثم مراجعة العميل للأدلة قبل أي قرار STOP / EXPAND / REDESIGN أو إعادة استخدام عام."
                if level in ("L1", "L2", "L3")
                else "جمع أدلة مصدرية مؤرخة ومقياس أساس معتمد قبل رفع مستوى الإثبات."
            ),
            "next_steps_en": (
                "Founder review followed by customer evidence review before any STOP / EXPAND / REDESIGN or public reuse decision."
                if level in ("L1", "L2", "L3")
                else "Collect dated source evidence and an approved baseline before raising proof level."
            ),
        }

    @classmethod
    def _render_markdown(
        cls,
        req: ProofBuildRequest,
        sections: dict[str, str],
        pack_id: str,
        level: str,
        evidence_refs: list[str],
    ) -> str:
        as_of = cls._as_of(req.events)
        return f"""# طقم الإثبات — {req.company_name}
**Proof Pack — {req.company_name}**

المعرف: `{pack_id}` | المستوى: **{level}** | as_of: {as_of}
الحالة: **يتطلب موافقة المؤسس** | الأحداث: {len(req.events)}
مراجع الأدلة: {", ".join(evidence_refs) or UNKNOWN}
إعادة الاستخدام العام: **{PUBLIC_REUSE_REQUIRES_PERMISSION}**

---

## الملخص التنفيذي / Executive Summary

**{sections["executive_summary_ar"]}**

*{sections["executive_summary_en"]}*

---

## المشكلة / Problem

**{sections["problem_ar"]}**

*{sections["problem_en"]}*

---

## الإجراءات المتخذة / Actions Taken

{sections["actions_ar"]}

---
*Actions (EN):*

{sections["actions_en"]}

---

## النتائج / Results

{sections["results_ar"]}

---
*Results (EN):*

{sections["results_en"]}

---

## Evidence State / حالة الدليل

**{sections["evidence_ar"]}**

*{sections["evidence_en"]}*

---

## الخطوة التالية / Next Step

**{sections["next_steps_ar"]}**

*{sections["next_steps_en"]}*

---

> هذا الطقم للمراجعة الداخلية فقط — لن يُسلَّم أو يُنشر دون موافقة صريحة مناسبة.
> This pack is for internal review only — it will not be delivered or published without appropriate explicit approval.

> **القيمة التقديرية ليست قيمة مُتحقَّقة** — Estimated value is not Verified value.
"""


__all__ = [
    "CUSTOMER_VALIDATED_WITH_DELIVERY_REF",
    "EVIDENCE_REF_PRESENT",
    "PARTIALLY_VALIDATED",
    "PUBLIC_REUSE_REQUIRES_PERMISSION",
    "RECORDED_NOT_VALIDATED",
    "ProofBuildRequest",
    "ProofBuilder",
    "ProofEvent",
    "ProofPackDocument",
    "UNKNOWN",
]

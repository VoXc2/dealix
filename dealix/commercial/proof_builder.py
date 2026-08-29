"""Evidence-bound Proof Pack Builder.

Only source-linked, timestamped, non-synthetic events can contribute to proof
readiness. This compatibility builder creates an internal review draft only. It
must not create payment truth, verified revenue, customer value, or external
commercial authority from raw reference strings.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
REFERENCE_ONLY = "REFERENCE_PRESENT_NOT_VERIFIED"


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

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())

    def semantic_dict(self) -> dict[str, Any]:
        data = self.to_dict()
        data.pop("generated_at", None)
        return data


_LEVEL_THRESHOLDS = {"L0": 0, "L1": 3, "L2": 6, "L3": 9}


class ProofBuilder:
    """Build an approval-gated, source-bound internal proof draft."""

    @staticmethod
    def _eligible_event(event: ProofEvent) -> bool:
        return bool(
            event.source_ref.strip()
            and event.recorded_at.strip()
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
                    event,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            ),
        }
        payload = json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
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
    def build(cls, req: ProofBuildRequest) -> ProofPackDocument:
        if any(
            event.metric_after == ""
            and event.delta_pct is not None
            and event.delta_pct > 0
            for event in req.events
        ):
            raise ValueError("NO_FAKE_PROOF: delta_pct set without metric_after")

        pack_id = cls._pack_id(req)
        level = cls._compute_level(
            req.events,
            approved_by_founder=req.approved_by_founder,
        )
        evidence_refs = cls._refs(
            [event.source_ref for event in req.events if cls._eligible_event(event)]
        )
        measured = [event for event in req.events if cls._measured_event(event)]
        customer_validated = any(
            event.customer_validated and event.customer_validation_ref.strip()
            for event in measured
        )

        # These are untyped compatibility refs. Presence may be reported, but this
        # builder cannot verify payment/delivery truth. Canonical typed evidence
        # validation lives in the buyer/proof evidence path.
        delivery_state = (
            REFERENCE_ONLY if cls._refs(req.delivery_evidence_refs) else UNKNOWN
        )
        payment_state = (
            REFERENCE_ONLY if cls._refs(req.payment_evidence_refs) else UNKNOWN
        )

        if measured and customer_validated:
            verified_result_state = "RECORDED_MEASUREMENT_CUSTOMER_VALIDATED_DELIVERY_UNVERIFIED"
        elif measured:
            verified_result_state = "RECORDED_MEASUREMENT_NOT_CUSTOMER_VALIDATED"
        else:
            verified_result_state = UNKNOWN

        sections = cls._build_sections(
            req,
            level,
            measured,
            verified_result_state,
            delivery_state,
            payment_state,
        )
        markdown = cls._render_markdown(
            req,
            sections,
            pack_id,
            level,
            evidence_refs,
        )
        eligible_events = [event for event in req.events if cls._eligible_event(event)]
        fake_gate = bool(
            req.approved_by_founder
            and eligible_events
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
            verified_result_state=verified_result_state,
            delivery_evidence_state=delivery_state,
            payment_evidence_state=payment_state,
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
                else " [غير مثبت المصدر]"
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
                else " [source not verified]"
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
            "القياسات مرتبطة بمراجع مصدرية، لكنها لا تصبح قيمة عميل مثبتة أو دليل تسليم/دفع متحققًا داخل هذا المسار."
            if measured
            else "لا توجد نتيجة قياس مصدرية مكتملة."
        )
        result_notice_en = (
            "Measurements are source-linked, but this compatibility path does not turn them or raw refs into verified customer value, delivery, or payment truth."
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
                f"حالة مرجع التسليم: {delivery_state} | حالة مرجع الدفع: {payment_state} | "
                f"حالة النتيجة: {verified_result_state}"
            ),
            "evidence_en": (
                f"Delivery reference state: {delivery_state} | Payment reference state: {payment_state} | "
                f"Result state: {verified_result_state}"
            ),
            "next_steps_ar": (
                "مراجعة المؤسس ثم التحقق عبر مسار الأدلة canonical قبل أي قرار STOP / EXPAND / REDESIGN."
                if level in ("L1", "L2", "L3")
                else "جمع أدلة مصدرية مؤرخة ومقياس أساس معتمد قبل رفع مستوى الإثبات."
            ),
            "next_steps_en": (
                "Founder review followed by canonical evidence verification before any STOP / EXPAND / REDESIGN decision."
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
        as_of = max(
            (event.recorded_at for event in req.events if event.recorded_at),
            default=UNKNOWN,
        )
        return f"""# طقم الإثبات — {req.company_name}
**Proof Pack — {req.company_name}**

المعرف: `{pack_id}` | المستوى: **{level}** | as_of: {as_of}
الحالة: **يتطلب موافقة المؤسس** | الأحداث: {len(req.events)}
مراجع الأدلة: {", ".join(evidence_refs) or UNKNOWN}

---

## الملخص التنفيذي / Executive Summary

**{sections['executive_summary_ar']}**

*{sections['executive_summary_en']}*

---

## المشكلة / Problem

**{sections['problem_ar']}**

*{sections['problem_en']}*

---

## الإجراءات المتخذة / Actions Taken

{sections['actions_ar']}

---
*Actions (EN):*

{sections['actions_en']}

---

## النتائج / Results

{sections['results_ar']}

---
*Results (EN):*

{sections['results_en']}

---

## Evidence State / حالة الدليل

**{sections['evidence_ar']}**

*{sections['evidence_en']}*

---

## الخطوة التالية / Next Step

**{sections['next_steps_ar']}**

*{sections['next_steps_en']}*

---

> هذا الطقم للمراجعة الداخلية فقط — لن يُسلَّم للعميل دون موافقة المؤسس.
> This pack is for internal review only — will not be delivered without founder approval.

> Raw payment or delivery references are not verification. Canonical typed evidence is required.
> **القيمة التقديرية ليست قيمة مُتحقَّقة** — Estimated value is not Verified value.
"""


__all__ = [
    "ProofBuildRequest",
    "ProofBuilder",
    "ProofEvent",
    "ProofPackDocument",
    "REFERENCE_ONLY",
    "UNKNOWN",
]

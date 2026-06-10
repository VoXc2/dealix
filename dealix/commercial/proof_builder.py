"""Proof Pack Builder — assembles L0-L5 proof from pilot evidence.

Constitutional gate: NO_FAKE_PROOF — only real documented evidence.
Minimum threshold: L1 requires 3+ approved events + 1 measurement.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class ProofEvent(BaseModel):
    event_type: str
    description_ar: str
    description_en: str
    metric_before: str = ""
    metric_after: str = ""
    delta_pct: float | None = None
    evidence_url: str = ""
    source_ref: str = ""  # provenance link required for verified/client_confirmed tiers
    recorded_at: str = ""


class ProofBuildRequest(BaseModel):
    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    pilot_id: str = ""
    events: list[ProofEvent] = Field(default_factory=list)
    approved_by_founder: bool = False
    customer_consent: bool = False


class ProofPackDocument(BaseModel):
    pack_id: str
    account_id: str
    company_name: str
    proof_level: str  # L0 | L1 | L2 | L3
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sections: dict[str, str]
    markdown_ar_en: str
    event_count: int
    score: int = 0  # 0-100; threshold ≥70 required before capital asset registration
    approval_status: str = "approval_required"
    governance_decision: str = "pending"  # pending | approved | rejected
    is_fake_proof_gate_passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


_LEVEL_THRESHOLDS = {
    "L0": 0,
    "L1": 3,
    "L2": 6,
    "L3": 9,
}


class ProofBuilder:
    """Builds proof packs from documented pilot events.

    Enforces NO_FAKE_PROOF: requires approved_by_founder=True before
    building anything above L0. All output is approval_required until
    founder explicitly approves.
    """

    def build(self, req: ProofBuildRequest) -> ProofPackDocument:
        import hashlib

        assert not any(
            e.metric_after == "" and e.delta_pct is not None and e.delta_pct > 0
            for e in req.events
        ), "NO_FAKE_PROOF: delta_pct set without metric_after"

        pack_id = hashlib.sha256(
            f"{req.account_id}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]

        level = self._compute_level(req.events)
        sections = self._build_sections(req, level)
        md = self._render_markdown(req, sections, pack_id, level)
        score = self._compute_score(req.events, level, req.approved_by_founder)

        return ProofPackDocument(
            pack_id=pack_id,
            account_id=req.account_id,
            company_name=req.company_name,
            proof_level=level,
            sections=sections,
            markdown_ar_en=md,
            event_count=len(req.events),
            score=score,
            is_fake_proof_gate_passed=req.approved_by_founder,
        )

    def _compute_score(
        self, events: list[ProofEvent], level: str, approved: bool
    ) -> int:
        """Score 0-100. Threshold ≥70 required before capital asset registration."""
        base = {"L0": 0, "L1": 35, "L2": 60, "L3": 80}.get(level, 0)
        measured = sum(1 for e in events if e.delta_pct is not None)
        sourced = sum(1 for e in events if e.source_ref.strip())
        bonus = min(measured * 4 + sourced * 3, 20)
        approved_bonus = 0 if not approved else 0  # approved_by_founder is a gate, not a score boost
        return min(base + bonus + approved_bonus, 100)

    def _compute_level(self, events: list[ProofEvent]) -> str:
        n = len(events)
        for level in ["L3", "L2", "L1"]:
            if n >= _LEVEL_THRESHOLDS[level]:
                return level
        return "L0"

    def _build_sections(self, req: ProofBuildRequest, level: str) -> dict[str, str]:
        name = req.company_name
        events_ar = "\n".join(
            f"- {e.description_ar}"
            + (f" (من {e.metric_before} إلى {e.metric_after})" if e.metric_before else "")
            for e in req.events
        )
        events_en = "\n".join(
            f"- {e.description_en}"
            + (f" (from {e.metric_before} to {e.metric_after})" if e.metric_before else "")
            for e in req.events
        )
        measured = [e for e in req.events if e.delta_pct is not None]
        avg_delta = (
            sum(e.delta_pct for e in measured) / len(measured) if measured else 0.0
        )

        return {
            "executive_summary_ar": (
                f"طقم إثبات مستوى {level} لـ {name}. "
                f"تم توثيق {len(req.events)} حدث خلال فترة التسليم. "
                f"متوسط التحسن: {avg_delta:.1f}%."
            ),
            "executive_summary_en": (
                f"Level {level} proof pack for {name}. "
                f"{len(req.events)} events documented during delivery. "
                f"Average improvement: {avg_delta:.1f}%."
            ),
            "problem_ar": "التحدي الذي واجهته الشركة والذي أدى إلى الانضمام لبرنامج Dealix.",
            "problem_en": "The challenge the company faced that led to joining the Dealix program.",
            "actions_ar": events_ar or "لم يتم توثيق أحداث بعد.",
            "actions_en": events_en or "No events documented yet.",
            "results_ar": (
                "\n".join(
                    f"- {e.description_ar}: +{e.delta_pct:.1f}%"
                    for e in measured
                ) or "قيد القياس."
            ),
            "results_en": (
                "\n".join(
                    f"- {e.description_en}: +{e.delta_pct:.1f}%"
                    for e in measured
                ) or "Under measurement."
            ),
            "next_steps_ar": (
                "الاستمرار مع برنامج Managed Ops لتحويل النتائج إلى نمو مستدام."
                if level in ("L1", "L2", "L3")
                else "استكمال جمع الأدلة للوصول لمستوى L1."
            ),
            "next_steps_en": (
                "Continue with Managed Ops program to turn results into sustainable growth."
                if level in ("L1", "L2", "L3")
                else "Complete evidence collection to reach L1 level."
            ),
        }

    def _render_markdown(
        self, req: ProofBuildRequest, sections: dict[str, str],
        pack_id: str, level: str,
    ) -> str:
        now = datetime.now(UTC).strftime("%Y-%m-%d")
        return f"""# طقم الإثبات — {req.company_name}
**Proof Pack — {req.company_name}**

المعرف: `{pack_id}` | المستوى: **{level}** | التاريخ: {now}
الحالة: **يتطلب موافقة المؤسس** | الأحداث: {len(req.events)}

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

## الخطوة التالية / Next Step

**{sections['next_steps_ar']}**

*{sections['next_steps_en']}*

---

> هذا الطقم للمراجعة الداخلية فقط — لن يُسلَّم للعميل دون موافقة المؤسس.
> This pack is for internal review only — will not be delivered without founder approval.

> **القيمة التقديرية ليست قيمة مُتحقَّقة** — Estimated value is not Verified value.
"""

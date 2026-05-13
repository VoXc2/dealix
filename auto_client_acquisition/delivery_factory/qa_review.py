"""QA Review — Dealix 5-gate Quality System + 100-point Project Quality Score.

نظام الجودة بخمس بوابات + درجة جودة المشروع.

Per docs/strategy/dealix_delivery_standard_and_quality_system.md §4–5.
Every project must pass all 5 gates AND score ≥ 80/100 to ship (Stage 6 Deliver).
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from core.logging import get_logger

log = get_logger(__name__)

QUALITY_FLOOR = 80


class GateName(StrEnum):
    BUSINESS = "business"
    DATA = "data"
    AI = "ai"
    COMPLIANCE = "compliance"
    DELIVERY = "delivery"


class GateCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question_ar: str
    question_en: str
    passed: bool
    note: str | None = None


class GateResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    gate: GateName
    checks: list[GateCheck]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)


class QualityScore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    business_impact: int = Field(ge=0, le=20)
    data_quality: int = Field(ge=0, le=15)
    output_quality_ar_en: int = Field(ge=0, le=15)
    customer_usability: int = Field(ge=0, le=10)
    safety_compliance: int = Field(ge=0, le=15)
    productization: int = Field(ge=0, le=15)
    retainer_upgradeability: int = Field(ge=0, le=10)

    @property
    def total(self) -> int:
        return (
            self.business_impact
            + self.data_quality
            + self.output_quality_ar_en
            + self.customer_usability
            + self.safety_compliance
            + self.productization
            + self.retainer_upgradeability
        )


class QAReport(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    report_id: str = Field(default_factory=lambda: f"qa_{uuid4().hex[:12]}")
    project_id: str
    gates: list[GateResult]
    score: QualityScore
    ships: bool
    reasons_blocked_ar: list[str] = Field(default_factory=list)
    reasons_blocked_en: list[str] = Field(default_factory=list)
    reviewer: str
    reviewed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _business_gate_questions() -> list[tuple[str, str]]:
    return [
        ("هل المشكلة واضحة؟", "Is the problem statement explicit?"),
        ("هل المخرج يهمّ الإدارة؟", "Does the output matter to executive decision-makers?"),
        ("هل فيه KPI رقمي؟", "Is there a numeric KPI?"),
        ("هل فيه Next Action؟", "Is there a clear next action?"),
        ("هل فيه مسار توسّع؟", "Is there an upsell path?"),
    ]


def _data_gate_questions() -> list[tuple[str, str]]:
    return [
        ("هل كل مصدر بيانات موثّق؟", "Is every data source attributed?"),
        ("هل التكرارات مُعالجة؟", "Are duplicates handled?"),
        ("هل الحقول الناقصة موثّقة؟", "Are missing fields documented?"),
        ("هل PII مُكتشف وأُخفي عند اللزوم؟", "Is PII detected and redacted where required?"),
        ("هل أساس PDPL موثّق؟", "Is lawful basis (PDPL Art. 5) documented?"),
        ("هل درجة جودة البيانات محسوبة؟", "Is data quality score calculated and shared?"),
    ]


def _ai_gate_questions() -> list[tuple[str, str]]:
    return [
        ("هل المخرجات دقيقة؟", "Are outputs accurate (sampled)?"),
        ("هل تجنّبنا الهلوسة (إجابات بمصادر)؟", "Are hallucinations caught (citation-grounded where applicable)?"),
        ("هل المصادر مُستشهدة؟", "Are sources cited?"),
        ("هل نبرة العربي مناسبة؟", "Is Arabic tone appropriate for sector and buyer?"),
        ("هل الحالات الحدية مختبَرة؟", "Are edge cases tested?"),
    ]


def _compliance_gate_questions() -> list[tuple[str, str]]:
    return [
        ("هل توجد ادعاءات مبالغ فيها؟", "Are there exaggerated or unverifiable claims?"),
        ("هل التواصل البارد متوافق مع PDPL (13/14)؟", "Is cold outreach PDPL-compliant (Art. 13 notice / Art. 14 consent)?"),
        ("هل PII غائب عن التقارير؟", "Is PII absent from reports?"),
        ("هل الموافقة البشرية مُسجَّلة عند اللزوم؟", "Is human approval logged where required?"),
        ("هل سجل التدقيق كامل وقابل للاستعلام؟", "Is the audit trail complete and queryable?"),
    ]


def _delivery_gate_questions() -> list[tuple[str, str]]:
    return [
        ("هل كل المخرجات في حزمة التسليم؟", "Are all deliverables in the handoff packet?"),
        ("هل التقرير التنفيذي مفهوم لقارئ غير تقني؟", "Is the executive report clear to a non-technical reader?"),
        ("هل العميل يعرف ماذا يفعل بعدها؟", "Does the customer know what to do next?"),
        ("هل جلسة التسليم مُسجَّلة/مُكتملة؟", "Is the handoff session scheduled/completed?"),
        ("هل عرض التجديد/الخطوة التالية مكتوب؟", "Is the renewal / next-step proposal drafted?"),
    ]


_GATE_QUESTIONS: dict[GateName, list[tuple[str, str]]] = {
    GateName.BUSINESS: _business_gate_questions(),
    GateName.DATA: _data_gate_questions(),
    GateName.AI: _ai_gate_questions(),
    GateName.COMPLIANCE: _compliance_gate_questions(),
    GateName.DELIVERY: _delivery_gate_questions(),
}


def build_blank_gates() -> list[GateResult]:
    """Return all 5 gates with empty (unchecked) questions — caller fills `passed`."""
    return [
        GateResult(
            gate=g,
            checks=[
                GateCheck(question_ar=ar, question_en=en, passed=False)
                for ar, en in qs
            ],
        )
        for g, qs in _GATE_QUESTIONS.items()
    ]


def evaluate(
    project_id: str,
    gates: list[GateResult],
    score: QualityScore,
    reviewer: str,
) -> QAReport:
    """Decide ships=True only when all gates pass AND total ≥ QUALITY_FLOOR."""
    reasons_ar: list[str] = []
    reasons_en: list[str] = []

    for gr in gates:
        if not gr.passed:
            failed = [c for c in gr.checks if not c.passed]
            for c in failed:
                reasons_ar.append(f"[{gr.gate}] {c.question_ar}")
                reasons_en.append(f"[{gr.gate}] {c.question_en}")

    if score.total < QUALITY_FLOOR:
        reasons_ar.append(
            f"درجة الجودة {score.total} أقل من الحد الأدنى {QUALITY_FLOOR}."
        )
        reasons_en.append(
            f"Quality score {score.total} below floor {QUALITY_FLOOR}."
        )

    ships = len(reasons_ar) == 0
    report = QAReport(
        project_id=project_id,
        gates=gates,
        score=score,
        ships=ships,
        reasons_blocked_ar=reasons_ar,
        reasons_blocked_en=reasons_en,
        reviewer=reviewer,
    )
    log.info(
        "qa_evaluated",
        project_id=project_id,
        total=score.total,
        ships=ships,
        blocked_count=len(reasons_ar),
    )
    return report

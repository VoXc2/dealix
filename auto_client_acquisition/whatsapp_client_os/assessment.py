"""Dealix Company Readiness Scan — «فحص جاهزية الإيرادات والمتابعة».

A short, professional readiness scan (not «استبيان») that produces:
- three pillar sub-scores (Revenue / Follow-up / Automation) + an overall 0–100,
- a risk band,
- ONE recommended next offer tied to the canonical ``service_catalog``,
- a first-workflow sketch, required permission levels, and a next action.

Scoring is deterministic and data-driven from ``AXES`` (mirrored in
``data/whatsapp/assessment_questions.yaml``). Every recommendation carries an
``evidence_level`` and a real catalog id — no invented claims.
"""

from __future__ import annotations

import uuid
from typing import Any

from auto_client_acquisition.service_catalog.registry import get_offering
from auto_client_acquisition.whatsapp_client_os.schemas import (
    AssessmentAnswer,
    AssessmentAxis,
    ClientAssessment,
    ReadinessScore,
    RiskLevel,
)

# ── Canonical axes (source of truth; YAML mirrors this) ──────────────────
# Each axis: pillar + ordered options with a 0–10 readiness score.
AXES: tuple[dict[str, Any], ...] = (
    {
        "axis": "lead_flow",
        "pillar": "revenue_readiness",
        "question_ar": "هل عندكم استفسارات أو leads شهريًا؟",
        "options": [
            {"id": "lead_flow_high", "label_ar": "نعم، كثير (50+ شهريًا)", "score": 9},
            {"id": "lead_flow_some", "label_ar": "نعم، متوسط", "score": 6},
            {"id": "lead_flow_few", "label_ar": "قليل", "score": 3},
            {"id": "lead_flow_none", "label_ar": "لا / غير متأكد", "score": 1},
        ],
    },
    {
        "axis": "channel_chaos",
        "pillar": "follow_up_maturity",
        "question_ar": "وين تجيكم الاستفسارات غالبًا؟",
        "options": [
            {"id": "channel_one", "label_ar": "قناة واحدة منظمة", "score": 9},
            {"id": "channel_two", "label_ar": "قناتين (واتساب + إيميل)", "score": 6},
            {"id": "channel_many", "label_ar": "قنوات متعددة ومبعثرة", "score": 3},
            {"id": "channel_unsure", "label_ar": "غير متأكد", "score": 2},
        ],
    },
    {
        "axis": "follow_up",
        "pillar": "follow_up_maturity",
        "question_ar": "هل في متابعة موحّدة للـ leads؟",
        "options": [
            {"id": "follow_up_yes", "label_ar": "نعم، عملية واضحة", "score": 9},
            {"id": "follow_up_partial", "label_ar": "جزئيًا / يدوي", "score": 5},
            {"id": "follow_up_no", "label_ar": "لا، تضيع كثير", "score": 2},
        ],
    },
    {
        "axis": "crm",
        "pillar": "follow_up_maturity",
        "question_ar": "هل تستخدمون CRM؟",
        "options": [
            {"id": "crm_active", "label_ar": "نعم، فعّال", "score": 9},
            {"id": "crm_partial", "label_ar": "موجود لكن غير منظم", "score": 5},
            {"id": "crm_none", "label_ar": "لا / Excel فقط", "score": 2},
        ],
    },
    {
        "axis": "decision_maker",
        "pillar": "revenue_readiness",
        "question_ar": "مين يقرر الشراء عندكم؟",
        "options": [
            {"id": "dm_clear", "label_ar": "واضح (شخص/لجنة محددة)", "score": 9},
            {"id": "dm_shared", "label_ar": "أكثر من شخص", "score": 6},
            {"id": "dm_unclear", "label_ar": "غير واضح", "score": 3},
        ],
    },
    {
        "axis": "offer_clarity",
        "pillar": "revenue_readiness",
        "question_ar": "هل عروضكم وأسعاركم واضحة؟",
        "options": [
            {"id": "offer_clear", "label_ar": "نعم، واضحة وموثّقة", "score": 9},
            {"id": "offer_partial", "label_ar": "واضحة جزئيًا", "score": 5},
            {"id": "offer_unclear", "label_ar": "غير واضحة", "score": 2},
        ],
    },
    {
        "axis": "reporting",
        "pillar": "follow_up_maturity",
        "question_ar": "هل الإدارة تشوف تقرير أسبوعي للمبيعات؟",
        "options": [
            {"id": "report_weekly", "label_ar": "نعم، أسبوعي", "score": 9},
            {"id": "report_monthly", "label_ar": "شهري فقط", "score": 5},
            {"id": "report_none", "label_ar": "لا يوجد تقرير", "score": 2},
        ],
    },
    {
        "axis": "automation_readiness",
        "pillar": "automation_readiness",
        "question_ar": "هل عندكم أدوات مربوطة (CRM/تقويم/واتساب أعمال)؟",
        "options": [
            {"id": "auto_connected", "label_ar": "نعم، مربوطة", "score": 9},
            {"id": "auto_some", "label_ar": "بعضها", "score": 5},
            {"id": "auto_none", "label_ar": "لا شيء مربوط", "score": 2},
        ],
    },
    {
        "axis": "compliance_privacy",
        "pillar": "automation_readiness",
        "question_ar": "هل بياناتكم منظمة وواضحة الحساسية؟",
        "options": [
            {"id": "comp_none", "label_ar": "لا بيانات حساسة", "score": 9},
            {
                "id": "comp_some",
                "label_ar": "بيانات شخصية (أرقام/إيميلات)",
                "score": 6,
                "sensitive": True,
            },
            {
                "id": "comp_high",
                "label_ar": "بيانات حساسة (مالية/صحية/هويات)",
                "score": 3,
                "sensitive": True,
            },
            {"id": "comp_unsure", "label_ar": "غير متأكد", "score": 4, "sensitive": True},
        ],
    },
    {
        "axis": "urgency",
        "pillar": "revenue_readiness",
        "question_ar": "وش تبغون تحققون خلال 14 يوم؟",
        "options": [
            {"id": "urgency_now", "label_ar": "نتيجة سريعة الآن", "score": 9},
            {"id": "urgency_soon", "label_ar": "خلال هذا الشهر", "score": 6},
            {"id": "urgency_explore", "label_ar": "نستكشف فقط", "score": 3},
        ],
    },
)

AXIS_ORDER: tuple[AssessmentAxis, ...] = tuple(a["axis"] for a in AXES)  # type: ignore[misc]

_PILLAR_AXES: dict[str, tuple[str, ...]] = {
    "revenue_readiness": ("lead_flow", "decision_maker", "offer_clarity", "urgency"),
    "follow_up_maturity": ("channel_chaos", "follow_up", "crm", "reporting"),
    "automation_readiness": ("automation_readiness", "compliance_privacy"),
}

# Option ids that signal sensitive data → force human review on L5 paths.
_SENSITIVE_OPTION_IDS: frozenset[str] = frozenset(
    {opt["id"] for ax in AXES for opt in ax["options"] if opt.get("sensitive")}
)

# (axis, option_id) → score lookup
_SCORE_LOOKUP: dict[tuple[str, str], int] = {
    (ax["axis"], opt["id"]): int(opt["score"]) for ax in AXES for opt in ax["options"]
}


def axis_spec(axis: str) -> dict[str, Any] | None:
    for ax in AXES:
        if ax["axis"] == axis:
            return ax
    return None


def score_for(axis: str, option_id: str) -> int:
    """0–10 readiness score for a chosen option (0 if unknown)."""
    return _SCORE_LOOKUP.get((axis, option_id), 0)


def make_answer(axis: AssessmentAxis, option_id: str) -> AssessmentAnswer:
    return AssessmentAnswer(axis=axis, option_id=option_id, score=score_for(axis, option_id))


def next_axis(answered: list[str]) -> str | None:
    """Next unanswered axis in canonical order, or None when complete."""
    done = set(answered)
    for ax in AXIS_ORDER:
        if ax not in done:
            return ax
    return None


def progress(answered: list[str]) -> tuple[int, int]:
    """(answered_count, total) — used for «الخطوة X من Y»."""
    valid = set(AXIS_ORDER)
    return (len({a for a in answered if a in valid}), len(AXIS_ORDER))


def _pillar_score(answers: dict[str, int], axes: tuple[str, ...]) -> int:
    vals = [answers[a] for a in axes if a in answers]
    if not vals:
        return 0
    # mean of 0–10 scores → 0–100
    return round(sum(vals) / len(vals) * 10)


def score_assessment(answers: list[AssessmentAnswer]) -> ReadinessScore:
    by_axis = {a.axis: int(a.score) for a in answers}
    revenue = _pillar_score(by_axis, _PILLAR_AXES["revenue_readiness"])
    follow_up = _pillar_score(by_axis, _PILLAR_AXES["follow_up_maturity"])
    automation = _pillar_score(by_axis, _PILLAR_AXES["automation_readiness"])
    overall = round(0.40 * revenue + 0.35 * follow_up + 0.25 * automation)
    risk = _risk_band(overall, answers)
    return ReadinessScore(
        revenue_readiness=revenue,
        follow_up_maturity=follow_up,
        automation_readiness=automation,
        overall=overall,
        risk=risk,
    )


def has_sensitive_data(answers: list[AssessmentAnswer]) -> bool:
    return any(a.option_id in _SENSITIVE_OPTION_IDS and int(a.score) <= 4 for a in answers)


def _risk_band(overall: int, answers: list[AssessmentAnswer]) -> RiskLevel:
    if has_sensitive_data(answers) or overall < 40:
        return "high"
    if overall >= 75:
        return "low"
    return "medium"


# ── Offer recommendation (deterministic, tied to service_catalog) ────────
_FIRST_WORKFLOW_AR = "Lead intake → مسودة متابعة → موافقة → إرسال يدوي → تقرير"


def recommend_offer(score: ReadinessScore, answers: list[AssessmentAnswer]) -> dict[str, Any]:
    """Pick the canonical customer-facing next offer without legacy fixed pricing."""
    by_axis = {a.axis: int(a.score) for a in answers}
    lead_present = by_axis.get("lead_flow", 0) >= 4

    if score.overall < 45:
        offer_id = "free_mini_diagnostic"
        rationale = [
            "الجاهزية الكلية منخفضة — نبدأ بتشخيص مجاني قبل أي بناء.",
            "نثبت المشكلة والفرصة أولًا قبل أي التزام تجاري.",
        ]
    else:
        offer_id = "revenue_command_pilot_30d"
        if score.follow_up_maturity < 55 and lead_present:
            rationale = [
                "عندكم leads لكن المتابعة تتسرّب.",
                "الخطوة التالية جلسة discovery لتحديد baseline ونطاق Pilot لمدة 30 يومًا.",
                "السعر والنطاق لا يُحددان هنا؛ يصدران في customer-specific quote موثق بعد discovery.",
            ]
        elif score.automation_readiness < 50:
            rationale = [
                "نحتاج أولًا تحديد أين تتعطل البيانات والتشغيل قبل أي أتمتة إضافية.",
                "جلسة discovery تحدد baseline ونطاق Pilot محدود ثم customer-specific quote موثق.",
            ]
        elif score.overall >= 75 and score.automation_readiness >= 65:
            rationale = [
                "الجاهزية مرتفعة بما يكفي للانتقال من التشخيص إلى Pilot محدود ومقاس.",
                "نثبت النطاق والـbaseline في discovery ثم نصدر customer-specific quote موثق.",
            ]
        else:
            rationale = [
                "الجاهزية مناسبة لخطوة تنفيذ محدودة بدل اشتراك ثابت مسبقًا.",
                "نحدد النطاق والـbaseline في discovery ثم نصدر customer-specific quote موثق.",
            ]

    offering = get_offering(offer_id)
    name_ar = offering.name_ar if offering else offer_id
    required = _required_permissions(offer_id)
    next_action = _next_action_ar(offer_id)
    if has_sensitive_data(answers):
        rationale.append("⚠️ يوجد بيانات حسّاسة — أي ربط يحتاج مراجعة بشرية ومسار آمن.")
    return {
        "offer_id": offer_id,
        "offer_name_ar": name_ar,
        "rationale_ar": rationale,
        "first_workflow_ar": _FIRST_WORKFLOW_AR,
        "required_permissions": required,
        "next_action_ar": next_action,
    }


def _required_permissions(offer_id: str) -> list[str]:
    base = ["L1: ملف/رابط يرسله العميل", "L1: رابط حجز التقويم"]
    if offer_id == "revenue_command_pilot_30d":
        base.insert(0, "L2: قراءة leads من CRM (بعد موافقة)")
    base.append("L4: إرسال متابعة بعد موافقة صريحة")
    return base


def _next_action_ar(offer_id: str) -> str:
    if offer_id == "free_mini_diagnostic":
        return "ابدأ التشخيص المجاني (24 ساعة)."
    if offer_id == "revenue_command_pilot_30d":
        return "احجز جلسة discovery لتوثيق نطاق Pilot لمدة 30 يومًا والـquote."
    return "احجز مكالمة 10 دقائق لتأكيد النطاق."


def build_assessment(
    *,
    client_handle: str,
    answers: list[AssessmentAnswer],
    company_name: str = "",
    assessment_id: str = "",
) -> ClientAssessment:
    """Assemble a completed ClientAssessment from answers (idempotent)."""
    score = score_assessment(answers)
    rec = recommend_offer(score, answers)
    completed = len({a.axis for a in answers}) >= len(AXIS_ORDER)
    return ClientAssessment(
        assessment_id=assessment_id or f"asmt_{uuid.uuid4().hex[:12]}",
        client_handle=client_handle,
        company_name=company_name,
        answers=answers,
        score=score,
        recommended_offer=rec["offer_id"],
        recommended_offer_ar=rec["offer_name_ar"],
        rationale_ar=rec["rationale_ar"],
        first_workflow_ar=rec["first_workflow_ar"],
        required_permissions=rec["required_permissions"],
        next_action_ar=rec["next_action_ar"],
        evidence_level="L1",
        completed=completed,
    )


__all__ = [
    "AXES",
    "AXIS_ORDER",
    "axis_spec",
    "build_assessment",
    "has_sensitive_data",
    "make_answer",
    "next_axis",
    "progress",
    "recommend_offer",
    "score_assessment",
    "score_for",
]

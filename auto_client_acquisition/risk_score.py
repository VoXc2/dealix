"""Revenue & AI Ops Risk Score — pure governance-readiness scoring.

Powers the public lead-magnet endpoint `POST /api/v1/public/risk-score`.
Given a short questionnaire about a company's revenue/AI operating posture,
returns a 0-100 risk score (higher = less governed = more risk), a band,
the specific governance gaps, and the recommended next step.

Hard rules:
- The score is an ESTIMATE — every result is marked `is_estimate: True`.
- No ROI / outcome claims. No guarantees. The recommended next step is
  always the free diagnostic (ladder rung 0), never a paid promise.
- Pure function: no I/O, no external calls. Safe to unit-test in isolation.
"""
from __future__ import annotations

from typing import Any

# Six governance controls. Each ABSENT control adds risk. The keys are the
# truthy answer expected from the questionnaire ("yes, we have this").
_CONTROLS: dict[str, dict[str, str]] = {
    "has_crm": {
        "ar": "لا يوجد CRM موثوق لتتبع الإيراد",
        "en": "No reliable CRM tracking revenue",
    },
    "pipeline_reliable": {
        "ar": "pipeline غير موثوق — الأرقام لا يُعتمد عليها",
        "en": "Pipeline is not reliable — numbers cannot be trusted",
    },
    "approval_before_external_action": {
        "ar": "لا توجد موافقة قبل الإجراءات الخارجية",
        "en": "No approval boundary before external actions",
    },
    "followup_documented": {
        "ar": "المتابعة غير موثَّقة",
        "en": "Follow-up is not documented",
    },
    "can_link_workflow_to_value": {
        "ar": "لا يمكن ربط أي workflow بقيمة مالية",
        "en": "Workflows cannot be linked to financial value",
    },
    "has_evidence_pack": {
        "ar": "لا يوجد سجل أدلة لأي مبادرة ذكاء اصطناعي",
        "en": "No evidence trail for any AI initiative",
    },
}

# Each absent control adds this much risk (6 x 14 = 84 max from controls).
_RISK_PER_GAP = 14
# Compounder: using AI in revenue work WITHOUT an approval boundary.
_UNGOVERNED_AI_PENALTY = 16

_BANDS = (
    (25, "low", "منخفض — تشغيل محكوم نسبياً"),
    (55, "moderate", "متوسط — فجوات حوكمة تحتاج معالجة"),
    (100, "high", "مرتفع — تشغيل غير محكوم، مخاطر إيراد وثقة"),
)


def score(answers: dict[str, Any]) -> dict[str, Any]:
    """Score a risk-score questionnaire submission.

    `answers` accepts the six control keys in `_CONTROLS` (truthy = control
    present) plus optional `uses_ai`. Qualification fields (`team_size`,
    `budget_band`, `urgency`) are ignored here — they describe the lead, not
    the governance posture — and are persisted separately by the caller.

    Returns a dict with `risk_score` (0-100), `risk_band`, `risk_band_label`,
    `gaps` (list of {key, ar, en}), `recommended_next_step`, and
    `is_estimate: True`.
    """
    gaps: list[dict[str, str]] = []
    risk = 0
    for key, label in _CONTROLS.items():
        if not _truthy(answers.get(key)):
            risk += _RISK_PER_GAP
            gaps.append({"key": key, "ar": label["ar"], "en": label["en"]})

    if _truthy(answers.get("uses_ai")) and not _truthy(
        answers.get("approval_before_external_action")
    ):
        risk += _UNGOVERNED_AI_PENALTY
        gaps.append(
            {
                "key": "ungoverned_ai",
                "ar": "ذكاء اصطناعي مُستخدَم في الإيراد بلا حدود موافقة",
                "en": "AI used in revenue work with no approval boundary",
            }
        )

    risk = max(0, min(100, risk))

    band = band_label = ""
    for ceiling, name, label in _BANDS:
        if risk <= ceiling:
            band, band_label = name, label
            break

    return {
        "risk_score": risk,
        "risk_band": band,
        "risk_band_label": band_label,
        "gaps": gaps,
        "gap_count": len(gaps),
        "recommended_next_step": {
            "offer": "free_ai_ops_diagnostic",
            "ar": "احجز التشخيص المجاني لعمليات الذكاء الاصطناعي — تقرير صفحة "
            "واحدة بأهم 3 أولويات.",
            "en": "Book the free AI Ops Diagnostic — a one-page report with "
            "your top 3 priorities.",
        },
        "is_estimate": True,
    }


def _truthy(value: Any) -> bool:
    """Interpret questionnaire answers leniently (JSON bool, "yes"/"no", 1/0)."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"yes", "true", "1", "y", "نعم"}
    return False

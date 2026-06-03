"""V12 Support OS — SLA target by priority."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Priority = Literal["p0", "p1", "p2", "p3"]


@dataclass
class SLATarget:
    priority: Priority
    minutes: int
    label_ar: str
    label_en: str


_TARGETS: dict[Priority, SLATarget] = {
    "p0": SLATarget(
        priority="p0",
        minutes=60,
        label_ar="استجابة خلال 15-60 دقيقة (طوارئ: أمن/دفع/خصوصية)",
        label_en="Respond within 15-60 minutes (security/payment/privacy emergency)",
    ),
    "p1": SLATarget(
        priority="p1",
        minutes=60 * 24,
        label_ar="استجابة في نفس اليوم (عميل متوقّف)",
        label_en="Respond same day (blocked customer)",
    ),
    "p2": SLATarget(
        priority="p2",
        minutes=60 * 24,
        label_ar="استجابة خلال 24 ساعة (دعم اعتيادي)",
        label_en="Respond within 24 hours (normal support)",
    ),
    "p3": SLATarget(
        priority="p3",
        minutes=60 * 48,
        label_ar="استجابة خلال 48 ساعة (سؤال أو اقتراح)",
        label_en="Respond within 48 hours (question/improvement)",
    ),
}


def compute_sla(priority: Priority) -> SLATarget:
    return _TARGETS.get(priority, _TARGETS["p2"])


def category_to_priority(category: str) -> Priority:
    """Default priority lookup per V12 plan."""
    p0 = {"refund", "privacy_pdpl", "payment", "angry_customer"}
    p1 = {"technical_issue", "billing"}
    p3 = {"upgrade_question", "diagnostic_question", "proof_pack_question"}
    if category in p0:
        return "p0"
    if category in p1:
        return "p1"
    if category in p3:
        return "p3"
    return "p2"

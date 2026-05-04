"""
Objection Classifier — deterministic keyword-based.

Maps customer objections to one of 8 canonical classes. Same approach as
the support classifier (no LLM call): fast, offline, predictable.

Classes:
    price            — "غالي" / "السعر مرتفع" / "expensive"
    timing           — "ما عندي وقت" / "الفصل القادم" / "later"
    trust            — "ما أعرفكم" / "وين الـ case studies" / "شركة جديدة"
    already_have_agency — "عندنا وكالة" / "we have an agency"
    need_team_approval — "أحتاج رأي الفريق" / "المجلس" / "co-founder"
    not_priority     — "ليس أولوية الآن" / "not the priority"
    send_details     — "أرسل لي التفاصيل" / "send me a deck"
    want_guarantee   — "تضمنون نتائج؟" / "guaranteed results?"
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ClassificationResult:
    objection_class: str
    matched_keyword: str | None
    confidence: float


_RULES: list[tuple[str, list[str]]] = [
    ("want_guarantee", [
        "تضمنون", "تضمن", "ضمان", "guarantee", "guaranteed", "نتائج مضمونة",
    ]),
    ("price", [
        "غالي", "السعر مرتفع", "السعر عالي", "ثمين", "expensive", "too much",
        "تخفيض", "خصم", "discount",
    ]),
    ("timing", [
        "ما عندي وقت", "ليس عندي وقت", "بعدين", "الربع القادم", "الفصل القادم",
        "later", "next quarter", "بعد رمضان", "بعد الإجازة",
    ]),
    ("already_have_agency", [
        "عندنا وكالة", "متعاقدين مع وكالة", "عندنا فريق",
        "we have an agency", "already have an agency",
    ]),
    ("need_team_approval", [
        "رأي الفريق", "رأي المجلس", "أرجع للفريق", "co-founder",
        "team approval", "board approval", "اشاور الفريق",
    ]),
    ("trust", [
        "ما أعرفكم", "ما نعرفكم", "شركة جديدة", "أول مرة", "case study",
        "case studies", "references", "credibility", "ثقة",
    ]),
    ("not_priority", [
        "ليست أولوية", "ليس أولوية", "لاحقاً", "أولوياتنا الآن",
        "not a priority", "not the priority", "later focus",
    ]),
    ("send_details", [
        "أرسل التفاصيل", "أرسل لي", "ابعث", "deck", "send me", "details",
        "more info", "معلومات أكثر",
    ]),
]


_FALLBACK_CLASS = "send_details"  # Safest default — gives them a deck


def classify(text: str) -> ClassificationResult:
    if not text:
        return ClassificationResult(_FALLBACK_CLASS, None, 0.0)
    haystack = text.lower()
    for cls, words in _RULES:
        for w in words:
            if all(c.isascii() for c in w):
                pattern = r"\b" + re.escape(w.lower()) + r"\b"
            else:
                pattern = re.escape(w.lower())
            if re.search(pattern, haystack):
                return ClassificationResult(cls, w, 0.85)
    return ClassificationResult(_FALLBACK_CLASS, None, 0.3)


def known_classes() -> tuple[str, ...]:
    return tuple(cls for cls, _ in _RULES)

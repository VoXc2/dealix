"""Next-best-action — bilingual concrete sentence, always approval-gated."""
from __future__ import annotations

from typing import Any


_TEMPLATES: dict[str, tuple[str, str]] = {
    "diagnostic": (
        "احجز جلسة Diagnostic مدّتها 30-60 دقيقة لمراجعة القمع.",
        "Book a 30-60 min Diagnostic session to review the funnel.",
    ),
    "growth_starter": (
        "ابدأ Growth Starter Pilot لتوليد 10 فرص مؤهَّلة في 7 أيام.",
        "Start a Growth Starter Pilot — 10 qualified opportunities in 7 days.",
    ),
    "data_to_revenue": (
        "نظِّف القائمة وصنِّف العملاء قبل أيّ تواصل خارجي.",
        "Clean the list and segment customers before any outbound contact.",
    ),
    "executive_growth_os": (
        "فعِّل الموجز التنفيذي الأسبوعي لمراجعة القرارات المعلَّقة.",
        "Activate the weekly executive brief to review pending decisions.",
    ),
    "partnership_growth": (
        "ابحث عن 3 شراكات مناسبة قبل أيّ نشاط خارجي.",
        "Identify 3 partner-fit candidates before any outbound activity.",
    ),
}


def next_best_action(brain: Any) -> str:
    """Return a concrete bilingual next action string.

    Always concrete, always closes with an explicit ``approval_required``
    marker so downstream consumers can enforce the gate.
    """
    service = str(getattr(brain, "service_recommendation", "growth_starter") or "growth_starter")
    ar, en = _TEMPLATES.get(service, _TEMPLATES["growth_starter"])
    return (
        f"{ar} / {en} "
        "(approval_required — لا يُنفَّذ إلا بعد موافقة المؤسس)"
    )

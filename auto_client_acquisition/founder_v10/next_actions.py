"""Bilingual deterministic next-action picker."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.founder_v10.blockers import find_blockers


def _top_decision_titles() -> dict[str, str]:
    try:
        from auto_client_acquisition.self_growth_os import daily_growth_loop
        loop = daily_growth_loop.build_today() or {}
        decisions = loop.get("decisions") or []
        if not decisions:
            return {}
        top = decisions[0]
        if isinstance(top, dict):
            return {
                "ar": str(
                    top.get("title_ar")
                    or top.get("name_ar")
                    or top.get("title")
                    or ""
                ),
                "en": str(
                    top.get("title_en")
                    or top.get("name_en")
                    or top.get("title")
                    or ""
                ),
            }
    except Exception:
        return {}
    return {}


def compute_next_action() -> dict[str, Any]:
    """Bilingual next action — never crashes, always returns both keys."""
    try:
        blockers = find_blockers()
    except Exception:
        blockers = []

    if any(b.severity in {"blocked", "high"} for b in blockers):
        return {
            "next_action_ar": "عالج الحواجز الحرجة قبل أيّ خطوة خارجية.",
            "next_action_en": "Resolve high/blocked items before any external step.",
            "rationale": "blockers_detected",
        }

    titles = _top_decision_titles()
    if titles.get("ar") or titles.get("en"):
        return {
            "next_action_ar": titles.get("ar") or "نفّذ القرار الأعلى من حلقة النمو.",
            "next_action_en": titles.get("en") or "Execute the top growth-loop decision.",
            "rationale": "top_decision_from_growth_loop",
        }

    return {
        "next_action_ar": "راجع لوحة المؤسس واحدد أوّل عميل اليوم.",
        "next_action_en": "Review the founder dashboard and pick today's first customer.",
        "rationale": "default_review_dashboard",
    }

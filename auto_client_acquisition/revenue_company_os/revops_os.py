"""
RevOps OS — funnel snapshot + weakest stage + recommendation.

Pure: takes counters from the funnel_events table + service_sessions and
returns the weekly RevOps brief.
"""

from __future__ import annotations

from typing import Any


def funnel_summary(funnel_event_counts: dict[str, int]) -> dict[str, Any]:
    """
    funnel_event_counts is keyed by stage:
      lead, mql, sql, pilot, paying, renewed, churned
    """
    counts = {k: int(funnel_event_counts.get(k, 0)) for k in
              ("lead", "mql", "sql", "pilot", "paying", "renewed", "churned")}

    def rate(num: int, den: int) -> float:
        return round(num / den, 3) if den > 0 else 0.0

    rates = {
        "lead_to_mql":     rate(counts["mql"],     counts["lead"]),
        "mql_to_sql":      rate(counts["sql"],     counts["mql"]),
        "sql_to_pilot":    rate(counts["pilot"],   counts["sql"]),
        "pilot_to_paying": rate(counts["paying"],  counts["pilot"]),
        "paying_to_renewed": rate(counts["renewed"], counts["paying"]),
    }

    weakest = min(rates.items(), key=lambda kv: kv[1]) if any(v > 0 for v in rates.values()) else (None, 0.0)

    return {
        "counts": counts,
        "rates": rates,
        "weakest_stage": weakest[0],
        "weakest_rate": weakest[1],
    }


def build_brief(funnel_event_counts: dict[str, int]) -> dict[str, Any]:
    summary = funnel_summary(funnel_event_counts)
    weakest = summary["weakest_stage"]
    rec = _recommend_for_weakest(weakest)
    return {
        "role": "revops",
        "brief_type": "weekly_revops",
        "summary": summary["counts"],
        "rates": summary["rates"],
        "top_decisions": [
            {
                "type": "funnel_focus",
                "title_ar": f"أضعف مرحلة هذا الأسبوع: {weakest or '—'}",
                "why_now_ar": "تركيز على المرحلة الأضعف يُضاعف conversion دون زيادة الـ leads.",
                "recommended_action_ar": rec,
                "risk_level": "low",
                "proof_impact": ["funnel_focus_set", "weekly_learning_captured"],
                "action_mode": "approval_required",
                "buttons_ar": ["اعتمد التوصية", "اعرض Funnel", "صعّد"],
            },
        ],
    }


def _recommend_for_weakest(stage: str | None) -> str:
    if stage == "lead_to_mql":
        return "حسّن intake form + قاعدة تأهيل ICP — أضف 2 سؤال للتأكيد."
    if stage == "mql_to_sql":
        return "أرسل Free Diagnostic لكل MQL خلال 24 ساعة + احجز callback."
    if stage == "sql_to_pilot":
        return "اعرض Pilot 499 صراحة في follow-up + Proof Pack sample."
    if stage == "pilot_to_paying":
        return "حسّن Proof Pack + اطلب رد فعل خلال 48 ساعة من التسليم."
    if stage == "paying_to_renewed":
        return "ابدأ Quarterly Review قبل شهر من renewal + اعرض Executive Growth OS."
    return "حافظ على الإيقاع الأسبوعي + كرّر الـ wedge segment."

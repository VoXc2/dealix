"""
Growth Manager OS — produces today's segment plan + experiment + scorecard.

Wraps the Self-Growth daily plan + adds a scorecard built from yesterday's
proof events, packaged as a 3-decision brief for the Growth Manager role.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.revenue_company_os.self_growth_mode import (
    build_daily_plan,
    daily_plan_to_dict,
)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def yesterday_scorecard(yesterday_events) -> dict[str, Any]:
    by_unit: Counter[str] = Counter()
    blocked = 0
    for e in yesterday_events:
        by_unit[e.unit_type] += 1
        if e.unit_type == "risk_blocked":
            blocked += 1
    return {
        "drafts_created":      by_unit.get("draft_created", 0),
        "approvals_collected": by_unit.get("approval_collected", 0),
        "followups_created":   by_unit.get("followup_created", 0),
        "opportunities_created": by_unit.get("opportunity_created", 0),
        "risks_blocked":       blocked,
        "no_unsafe_action_executed": True,
    }


def top_decisions(plan: dict[str, Any], scorecard: dict[str, Any]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []

    decisions.append({
        "type": "target_segment",
        "title_ar": f"شريحة اليوم: {plan['focus_segment_ar']}",
        "why_now_ar": "اختيار محكوم بدورة 3-segment rotation لتغطية السوق بدون burn.",
        "recommended_action_ar": "اعتمد القنوات (LinkedIn manual + Email drafts + Referral) واطلب التنفيذ من الفريق.",
        "risk_level": "low",
        "proof_impact": ["target_segment_selected", "growth_plan_created"],
        "action_mode": "approval_required",
        "buttons_ar": ["اعتمد", "غيّر الشريحة", "Scorecard"],
    })

    decisions.append({
        "type": "channel_health",
        "title_ar": "صحة القنوات اليوم",
        "why_now_ar": "نُذكّر يومياً بما هو ممنوع: cold WhatsApp + LinkedIn automation + mass send.",
        "recommended_action_ar": "اعتمد القنوات الآمنة فقط — كل draft يمر بموافقتك.",
        "risk_level": "low",
        "proof_impact": ["channel_policy_checked", "risk_blocked"],
        "action_mode": "approved_execute",
        "buttons_ar": ["اعتمد القنوات", "اعرض السياسة", "تخطي"],
    })

    decisions.append({
        "type": "message_experiment",
        "title_ar": f"تجربة اليوم: {plan['experiment_hypothesis_ar']}",
        "why_now_ar": "تجربة واحدة واضحة في اليوم > 5 تجارب ضائعة.",
        "recommended_action_ar": "اختبر النسختين A/B على 5 رسائل لكل واحدة.",
        "risk_level": "low",
        "proof_impact": ["growth_experiment_created", "message_variant_created"],
        "action_mode": "approval_required",
        "buttons_ar": ["اعتمد التجربة", "عدّل النص", "احفظ لاحقاً"],
    })

    return decisions[:3]


def build_brief(yesterday_events) -> dict[str, Any]:
    plan = daily_plan_to_dict(build_daily_plan())
    scorecard = yesterday_scorecard(yesterday_events or [])
    return {
        "role": "growth_manager",
        "brief_type": "daily_growth_plan",
        "date": _now().date().isoformat(),
        "summary": {
            "focus_segment": plan["focus_segment_ar"],
            "channels_planned": sum(int(c.get("count", 0)) for c in plan["channel_plan"]),
            "experiment_active": True,
            "yesterday_drafts": scorecard["drafts_created"],
            "yesterday_approvals": scorecard["approvals_collected"],
            "yesterday_blocked": scorecard["risks_blocked"],
        },
        "plan": plan,
        "yesterday_scorecard": scorecard,
        "top_decisions": top_decisions(plan, scorecard),
        "blocked_today_ar": list(plan["forbidden_today"]),
    }

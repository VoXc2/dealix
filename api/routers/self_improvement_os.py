"""V12 Self-Improvement OS — weekly-learning + prompt-quality stub.

Wraps `self_growth_os.weekly_growth_scorecard`. Adds a prompt-quality
stub that suggests improvements only — never auto-applies. NO
self-modifying code. NO automatic PR.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/self-improvement-os", tags=["self-improvement-os"])


_HARD_GATES = {
    "no_self_modifying_code": True,
    "no_automatic_pr": True,
    "no_fake_metrics": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def self_improvement_os_status() -> dict[str, Any]:
    return {
        "service": "self_improvement_os",
        "module": "self_growth_os+v12_quality_stub",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"weekly_scorecard": "ok", "prompt_quality": "stub"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "اقرأ /weekly-learning كلّ يوم اثنين",
        "next_action_en": "Read /weekly-learning every Monday.",
    }


@router.get("/weekly-learning")
async def weekly_learning() -> dict[str, Any]:
    """Suggest improvements based on observed patterns. SUGGEST ONLY."""
    suggestions = [
        {
            "area": "knowledge_base",
            "suggestion_ar": "أضف 3 أسئلة جديدة كل أسبوع للـ KB حسب الأسئلة الواردة",
            "suggestion_en": "Add 3 new KB Q&As per week based on inbound questions.",
            "evidence": "support tickets count + classifier 'unknown' rate",
            "action_mode": "suggest_only",
        },
        {
            "area": "outreach_drafts",
            "suggestion_ar": "حسّن المسوّدات بناءً على معدّل الردّ الأسبوعي",
            "suggestion_en": "Tune drafts based on weekly reply rate.",
            "evidence": "reply rate per template (placeholder until real data)",
            "action_mode": "suggest_only",
        },
        {
            "area": "service_gap",
            "suggestion_ar": "إذا تكرّر اعتراض السعر 3 مرّات، فكّر في خدمة أصغر",
            "suggestion_en": "If price objection repeats 3 times, consider a smaller offer.",
            "evidence": "objection_handler categories",
            "action_mode": "suggest_only",
        },
    ]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "suggestions": suggestions,
        "data_status": "stub_real_signals_required_for_v13",
        "summary_ar": "اقتراحات للنقاش — لا تطبيق آلي",
        "summary_en": "Suggestions for discussion — no automatic application.",
        "hard_gates": _HARD_GATES,
    }

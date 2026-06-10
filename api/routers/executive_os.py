"""V12 Executive OS — daily-brief + weekly-pack + risk-summary.

Wraps `executive_reporting`. Adds top-3 daily decisions composed
from the WorkItem queue. NO fake forecast; if data is missing,
states `insufficient_data` honestly.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.full_ops import (
    get_default_queue,
    prioritize,
)

router = APIRouter(prefix="/api/v1/executive-os", tags=["executive-os"])


_HARD_GATES = {
    "no_fake_revenue": True,
    "no_fake_forecast": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def executive_os_status() -> dict[str, Any]:
    return {
        "service": "executive_os",
        "module": "executive_reporting+v12_brief",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"daily_brief": "ok", "weekly_pack": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "اقرأ /daily-brief صباحاً و /weekly-pack الإثنين",
        "next_action_en": "Read /daily-brief in the morning and /weekly-pack on Monday.",
    }


@router.get("/daily-brief")
async def daily_brief() -> dict[str, Any]:
    """Top-3 decisions composed from the WorkItem queue.

    No revenue claim. No forecast. If queue is empty, says so.
    """
    queue = get_default_queue()
    items = queue.list_all()
    top3 = prioritize(items)[:3]
    if not top3:
        return {
            "schema_version": 1,
            "generated_at": datetime.now(UTC).isoformat(),
            "decisions": [],
            "summary_ar": (
                "لا توجد قرارات معلّقة الآن. ابدأ Phase E بـ 3 warm intros."
            ),
            "summary_en": (
                "No pending decisions. Start Phase E with 3 warm intros."
            ),
            "data_status": "insufficient_data",
            "hard_gates": _HARD_GATES,
        }
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "decisions": [it.model_dump(mode="json") for it in top3],
        "summary_ar": "أهم 3 قرارات اليوم — تابع p0 أولاً",
        "summary_en": "Top 3 decisions today — handle p0 first.",
        "data_status": "live",
        "hard_gates": _HARD_GATES,
    }


@router.get("/weekly-pack")
async def weekly_pack() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_all()
    by_priority = {p: len([i for i in items if i.priority == p]) for p in ("p0", "p1", "p2", "p3")}
    by_os = {os_t: len([i for i in items if i.os_type == os_t]) for os_t in (
        "growth", "sales", "support", "customer_success", "delivery",
        "partnership", "compliance", "executive", "self_improvement",
    )}
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "by_priority": by_priority,
        "by_os_type": by_os,
        "total_items": len(items),
        "summary_ar": "ملخّص أسبوعي للقرارات المعلّقة عبر 9 أنظمة OS",
        "summary_en": "Weekly summary of pending decisions across 9 OSes.",
        "risks_ar": "لا ادّعاءات إيرادات؛ لا تنبّؤ مزيّف",
        "risks_en": "No revenue claims; no fake forecast.",
        "hard_gates": _HARD_GATES,
    }

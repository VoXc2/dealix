"""V12 — Full-Ops umbrella router.

Single ``GET /api/v1/full-ops/daily-command-center`` returning all 5
active OS queues + top-3 decisions + blocked actions + hard gates.

Read-only. No external calls. Returns 200 always; degraded sections
are reported in ``degraded_sections`` rather than raising 5xx.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.full_ops import (
    WorkItem,
    get_default_queue,
    prioritize,
)

router = APIRouter(prefix="/api/v1/full-ops", tags=["full-ops"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "no_linkedin_automation": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


def _safe(name: str, fn, default, degraded: list[str]) -> Any:
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001 — never crash command center
        degraded.append(name)
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_default": default,
        }


def _growth_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("growth")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _sales_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("sales")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _support_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("support")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _cs_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("customer_success")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _delivery_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("delivery")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _compliance_alerts() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("compliance")
    escalated = [it for it in items if it.status == "escalated"]
    return {
        "count": len(items),
        "escalated": len(escalated),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _executive_summary() -> dict[str, Any]:
    queue = get_default_queue()
    all_items = queue.list_all()
    by_priority = {p: len(queue.list_by_priority(p)) for p in ("p0", "p1", "p2", "p3")}
    return {
        "total_items": len(all_items),
        "by_priority": by_priority,
    }


def _blocked_actions() -> dict[str, Any]:
    queue = get_default_queue()
    blocked = queue.list_by_status("blocked")
    return {
        "count": len(blocked),
        "first_3": [b.model_dump(mode="json") for b in prioritize(blocked)[:3]],
    }


def _today_top_3() -> list[dict[str, Any]]:
    queue = get_default_queue()
    return [it.model_dump(mode="json") for it in prioritize(queue.list_all())[:3]]


@router.get("/status")
async def full_ops_status() -> dict[str, Any]:
    return {
        "service": "full_ops",
        "module": "full_ops",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"work_queue": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "افتح /daily-command-center للحصول على القرارات اليومية",
        "next_action_en": "Open /daily-command-center for today's decisions.",
    }


@router.get("/daily-command-center")
async def daily_command_center() -> dict[str, Any]:
    """Single bilingual snapshot across all 9 OSes.

    Read-only. 200 always. Degraded sections reported in
    ``degraded_sections`` rather than 5xx.
    """
    degraded: list[str] = []
    growth = _safe("growth_queue", _growth_queue, {"count": 0, "top_3": []}, degraded)
    sales = _safe("sales_queue", _sales_queue, {"count": 0, "top_3": []}, degraded)
    support = _safe("support_queue", _support_queue, {"count": 0, "top_3": []}, degraded)
    cs = _safe("cs_queue", _cs_queue, {"count": 0, "top_3": []}, degraded)
    delivery = _safe("delivery_queue", _delivery_queue, {"count": 0, "top_3": []}, degraded)
    compliance = _safe(
        "compliance_alerts",
        _compliance_alerts,
        {"count": 0, "escalated": 0, "top_3": []},
        degraded,
    )
    executive = _safe(
        "executive_summary",
        _executive_summary,
        {"total_items": 0, "by_priority": {}},
        degraded,
    )
    blocked = _safe(
        "blocked_actions", _blocked_actions, {"count": 0, "first_3": []}, degraded
    )
    top_3 = _safe("today_top_3", _today_top_3, [], degraded)

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "مركز الأوامر اليومي — Dealix Full-Ops",
        "title_en": "Daily Command Center — Dealix Full-Ops",
        "today_top_3_decisions": top_3,
        "growth_queue": growth,
        "sales_queue": sales,
        "support_queue": support,
        "cs_queue": cs,
        "delivery_queue": delivery,
        "compliance_alerts": compliance,
        "executive_summary": executive,
        "blocked_actions": blocked,
        "proof_summary": {
            "note_ar": "أدلة العميل توثَّق في docs/proof-events/ عند توفّرها",
            "note_en": "Customer proof events are recorded under docs/proof-events/ when available.",
        },
        "next_best_actions": {
            "ar": "ابدأ بأعلى p0/p1 في كل قائمة، وتجاهل المحظور",
            "en": "Start with the highest p0/p1 in each queue; skip blocked items.",
        },
        "hard_gates": _HARD_GATES,
        "degraded": bool(degraded),
        "degraded_sections": degraded,
    }

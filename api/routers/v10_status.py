"""V10 umbrella status — single endpoint that summarizes the 10 v10 modules.

Read-only. No DB write. No external call. Returns 200 even if a sub-module
is partially unavailable; degraded sub-modules are listed in the response.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/v10", tags=["v10"])


_V10_MODULES = (
    "llm_gateway_v10",
    "safety_v10",
    "observability_v10",
    "workflow_os_v10",
    "crm_v10",
    "customer_inbox_v10",
    "growth_v10",
    "knowledge_v10",
    "ai_workforce_v10",
    "founder_v10",
)


def _check_module(name: str) -> dict[str, Any]:
    try:
        __import__(f"auto_client_acquisition.{name}")
        return {"name": name, "status": "ok"}
    except BaseException as exc:
        return {
            "name": name,
            "status": "degraded",
            "error_type": type(exc).__name__,
        }


@router.get("/status")
async def v10_umbrella_status() -> dict[str, Any]:
    checks = [_check_module(m) for m in _V10_MODULES]
    degraded_sections = [c["name"] for c in checks if c["status"] != "ok"]
    degraded = bool(degraded_sections)
    return {
        "service": "v10_umbrella",
        "module": "v10",
        "status": "degraded" if degraded else "operational",
        "version": "v10",
        "degraded": degraded,
        "degraded_sections": degraded_sections,
        "checks": checks,
        "modules_total": len(_V10_MODULES),
        "modules_ok": sum(1 for c in checks if c["status"] == "ok"),
        "hard_gates": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
        "next_action_ar": (
            "راجع وحدة v10 المتأخّرة" if degraded else "كل وحدات v10 جاهزة"
        ),
        "next_action_en": (
            "Review the degraded v10 module."
            if degraded
            else "All v10 modules ready."
        ),
    }

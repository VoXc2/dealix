"""V11 — customer-serving closure umbrella status.

Read-only. Reports the V11 readiness signals: dashboard cache, runtime
paths, Phase E doc kit presence, hard gates. Returns 200 even with
degraded sub-checks; never 5xx.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/v11", tags=["v11"])


_REPO_ROOT = Path(__file__).resolve().parents[2]
_PHASE_E_DOCS = (
    "00_GO_NO_GO.md",
    "01_FIRST_3_WARM_INTROS_BOARD.md",
    "02_FIRST_10_WARM_MESSAGES_AR_EN.md",
    "03_MINI_DIAGNOSTIC_TEMPLATE.md",
    "04_DIAGNOSTIC_SCRIPT_USAGE.md",
    "05_PILOT_499_OFFER.md",
    "06_MANUAL_PAYMENT_FALLBACK.md",
    "07_7_DAY_PILOT_DELIVERY_PLAN.md",
    "08_PROOF_PACK_TEMPLATE.md",
    "09_CUSTOMER_REVIEW_AND_UPSELL.md",
    "10_DAILY_FOUNDER_LOOP.md",
    "11_FIRST_CUSTOMER_EVIDENCE_TABLE.md",
)


def _check_dashboard_cache() -> dict[str, Any]:
    try:
        from auto_client_acquisition.founder_v10 import (
            cached_dashboard_payload,  # noqa: F401
        )
        return {"name": "dashboard_cache", "status": "ok"}
    except BaseException as exc:  # noqa: BLE001
        return {"name": "dashboard_cache", "status": "degraded",
                "error_type": type(exc).__name__}


def _check_runtime_paths() -> dict[str, Any]:
    try:
        from auto_client_acquisition.runtime_paths import resolve_registry_dir
        path = resolve_registry_dir()
        return {
            "name": "runtime_paths",
            "status": "ok" if path.exists() else "degraded",
            "registry_dir_exists": path.exists(),
        }
    except BaseException as exc:  # noqa: BLE001
        return {"name": "runtime_paths", "status": "degraded",
                "error_type": type(exc).__name__}


def _check_phase_e_docs() -> dict[str, Any]:
    base = _REPO_ROOT / "docs" / "phase-e"
    if not base.exists():
        return {"name": "phase_e_docs", "status": "degraded",
                "missing": list(_PHASE_E_DOCS)}
    missing = [d for d in _PHASE_E_DOCS if not (base / d).exists()]
    return {
        "name": "phase_e_docs",
        "status": "ok" if not missing else "degraded",
        "present": len(_PHASE_E_DOCS) - len(missing),
        "total": len(_PHASE_E_DOCS),
        "missing": missing,
    }


@router.get("/status")
async def v11_status() -> dict[str, Any]:
    checks = [
        _check_dashboard_cache(),
        _check_runtime_paths(),
        _check_phase_e_docs(),
    ]
    degraded_sections = [c["name"] for c in checks if c["status"] != "ok"]
    degraded = bool(degraded_sections)
    return {
        "service": "v11_customer_closure",
        "module": "v11",
        "status": "degraded" if degraded else "operational",
        "version": "v11",
        "degraded": degraded,
        "degraded_sections": degraded_sections,
        "checks": checks,
        "hard_gates": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "no_linkedin_automation": True,
            "no_fake_proof": True,
            "approval_required_for_external_actions": True,
        },
        "next_action_ar": (
            "راجع الفحص المتأخّر؛ التشغيل الأساسي مستمر."
            if degraded
            else "كل تجهيزات V11 جاهزة — ابدأ ب 3 warm intros."
        ),
        "next_action_en": (
            "Review the degraded check; core ops continue."
            if degraded
            else "V11 closure is ready — start with 3 warm intros."
        ),
    }

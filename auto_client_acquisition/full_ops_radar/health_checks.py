"""Per-subsystem health checks for Full-Ops Score.

Each check returns True/False (best-effort, never raises). The score
module weights each layer accordingly.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import safe_import


def _module_present(path: str) -> bool:
    return safe_import(path) is not None


def check_leadops() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.leadops_spine")
    return {"layer": "leadops", "available": ok, "max_weight": 15}


def check_customer_brain() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.customer_brain")
    return {"layer": "customer_brain", "available": ok, "max_weight": 10}


def check_service_sessions() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.service_sessions")
    return {"layer": "service_sessions", "available": ok, "max_weight": 10}


def check_approval_center() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.approval_center")
    return {"layer": "approval_center", "available": ok, "max_weight": 10}


def check_payment_ops() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.payment_ops")
    return {"layer": "payment_ops", "available": ok, "max_weight": 10}


def check_support() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.support_inbox")
    return {"layer": "support", "available": ok, "max_weight": 10}


def check_proof_ledger() -> dict[str, Any]:
    ok = _module_present("auto_client_acquisition.proof_ledger")
    return {"layer": "proof_ledger", "available": ok, "max_weight": 10}


def check_customer_portal() -> dict[str, Any]:
    """Customer portal is the FastAPI router; check by import."""
    ok = _module_present("api.routers.customer_company_portal")
    return {"layer": "customer_portal", "available": ok, "max_weight": 10}


def check_executive_dashboard() -> dict[str, Any]:
    ok = (
        _module_present("auto_client_acquisition.executive_pack_v2")
        or _module_present("auto_client_acquisition.executive_reporting")
    )
    return {"layer": "executive_dashboard", "available": ok, "max_weight": 10}


def check_safety_compliance() -> dict[str, Any]:
    """Hard gates module is the floor — any one of these counts."""
    ok = (
        _module_present("auto_client_acquisition.whatsapp_safe_send")
        or _module_present("auto_client_acquisition.designops.safety_gate")
        or _module_present("auto_client_acquisition.consent_table")
    )
    return {"layer": "safety_compliance", "available": ok, "max_weight": 5}


def run_all_health_checks() -> list[dict[str, Any]]:
    return [
        check_leadops(),
        check_customer_brain(),
        check_service_sessions(),
        check_approval_center(),
        check_payment_ops(),
        check_support(),
        check_proof_ledger(),
        check_customer_portal(),
        check_executive_dashboard(),
        check_safety_compliance(),
    ]

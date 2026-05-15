"""Founder-facing read-only risk + policy snapshot."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.governance_os.policy_registry import (
    forbidden_actions,
    load_policy_registry,
)
from auto_client_acquisition.service_sessions import list_sessions

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])


def build_risk_dashboard_payload() -> dict[str, Any]:
    """Shared payload for HTTP and founder scorecard (read-only)."""
    sessions = list_sessions(limit=100)
    blocked = sum(1 for s in sessions if s.status == "blocked")
    waiting = sum(1 for s in sessions if s.status == "waiting_for_approval")
    reg = load_policy_registry()
    return {
        "schema_version": 1,
        "policy_registry_version": reg.get("version", 0),
        "forbidden_actions": forbidden_actions(),
        "risk_categories": reg.get("risk_categories", []),
        "service_sessions": {
            "sampled": len(sessions),
            "blocked_count": blocked,
            "waiting_for_approval_count": waiting,
        },
        "related_readonly_endpoints": {
            "business_metrics_board": "/api/v1/metrics",
        },
        "read_only": True,
    }


@router.get("/risk-dashboard")
def get_risk_dashboard() -> dict[str, Any]:
    """Aggregate lightweight signals — read-only, no mutations."""
    return build_risk_dashboard_payload()

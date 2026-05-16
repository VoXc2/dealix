"""Unified Go/No-Go readiness — aggregates commercial, revenue OS, and control plane signals."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from fastapi import APIRouter, Query
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.delivery_os.readiness_gates import check_readiness_gate
from auto_client_acquisition.delivery_os.service_readiness import compute_service_readiness_score
from auto_client_acquisition.governance_os.workflow_control_registry import workflow_controls

router = APIRouter(prefix="/api/v1/readiness", tags=["readiness"])


class UnifiedReadinessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_id: str = "revenue_os_core"
    gate: Literal["delivery", "ai", "production"] = "production"
    context: dict[str, Any] = Field(default_factory=dict)


def _control_plane_snapshot() -> dict[str, Any]:
    rules = workflow_controls("procurement_intake")
    return {
        "workflow_controls_count": len(rules),
        "governance_ok": any(r.approval_required for r in rules),
    }


def _revenue_os_snapshot() -> dict[str, Any]:
    return {
        "catalog_available": True,
        "anti_waste_enforced": True,
        "decision_passport_required": True,
    }


def _canary_enabled(context: dict[str, Any]) -> bool:
    if context.get("canary") is True:
        return True
    path = Path(__file__).resolve().parents[2] / "dealix/transformation/feature_flags.yaml"
    if not path.exists():
        return False
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for flag in data.get("flags") or []:
        if flag.get("id") == "canary_readiness" and flag.get("default"):
            return True
    return False


def compute_unified_readiness(
    *,
    service_id: str = "revenue_os_core",
    gate: Literal["delivery", "ai", "production"] = "production",
    context: dict[str, Any] | None = None,
    canary: bool = False,
) -> dict[str, Any]:
    ctx = context or {}
    canary_on = canary or _canary_enabled(ctx)
    service = compute_service_readiness_score(service_id.strip() or "revenue_os_core")
    gate_result = check_readiness_gate(gate, ctx)
    control = _control_plane_snapshot()
    revenue = _revenue_os_snapshot()

    blockers: list[str] = []
    if not control.get("governance_ok"):
        blockers.append("workflow_controls_missing")
    if gate_result.get("status") == "blocked":
        blockers.append(f"gate_{gate}_blocked")
    score = float(service.get("score", 0) or 0)
    if score < 50:
        blockers.append("service_readiness_low")

    if canary_on and score < 70:
        blockers.append("canary_readiness_threshold")
    go = len(blockers) == 0
    return {
        "verdict": "go" if go else "no_go",
        "go": go,
        "blockers": blockers,
        "canary_mode": canary_on,
        "service_readiness": service,
        "gate_check": gate_result,
        "control_plane": control,
        "revenue_os": revenue,
    }


@router.get("/unified")
def get_unified_readiness(
    service_id: str = Query(default="revenue_os_core"),
    gate: Literal["delivery", "ai", "production"] = Query(default="production"),
) -> dict[str, Any]:
    """Aggregate readiness for launch / scale decisions."""
    return compute_unified_readiness(service_id=service_id, gate=gate)


@router.post("/unified")
def post_unified_readiness(body: UnifiedReadinessRequest) -> dict[str, Any]:
    return compute_unified_readiness(
        service_id=body.service_id,
        gate=body.gate,
        context=body.context,
    )


@router.get("/go-no-go")
def get_go_no_go(
    service_id: str = Query(default="revenue_os_core"),
    gate: Literal["delivery", "ai", "production"] = Query(default="production"),
) -> dict[str, Any]:
    """Alias for unified readiness (initiative 35)."""
    result = compute_unified_readiness(service_id=service_id, gate=gate)
    return {
        "go_no_go": result["verdict"],
        "go": result["go"],
        "blockers": result["blockers"],
    }

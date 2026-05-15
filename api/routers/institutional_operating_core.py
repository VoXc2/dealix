"""Institutional Operating Core API surface."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.institutional_intelligence_layer import (
    SYSTEMS_56_TO_65,
    InstitutionalDependencySnapshot,
    operating_core_verdict,
)

router = APIRouter(
    prefix="/api/v1/institutional-operating-core",
    tags=["institutional-operating-core"],
)


class DependencySnapshotBody(BaseModel):
    decision_dependency_pct: float = Field(ge=0.0, le=100.0)
    execution_dependency_pct: float = Field(ge=0.0, le=100.0)
    governance_dependency_pct: float = Field(ge=0.0, le=100.0)
    memory_dependency_pct: float = Field(ge=0.0, le=100.0)
    resilience_dependency_pct: float = Field(ge=0.0, le=100.0)
    economic_dependency_pct: float = Field(ge=0.0, le=100.0)
    systems_ready: dict[str, bool] = Field(default_factory=dict)


@router.get("/status")
async def status() -> dict[str, Any]:
    """Institutional intelligence layer readiness scaffold."""
    return {
        "service": "institutional_operating_core",
        "objective": "institutional_dependency_over_agent_count",
        "systems_56_to_65": SYSTEMS_56_TO_65,
        "hard_rule": (
            "Dealix reaches infrastructure status only when institutional dependency "
            "and system readiness are both satisfied."
        ),
    }


@router.post("/dependency/verdict")
async def dependency_verdict(body: DependencySnapshotBody) -> dict[str, Any]:
    """Compute institutional dependency verdict for an enterprise account."""
    snapshot = InstitutionalDependencySnapshot(
        decision_dependency_pct=body.decision_dependency_pct,
        execution_dependency_pct=body.execution_dependency_pct,
        governance_dependency_pct=body.governance_dependency_pct,
        memory_dependency_pct=body.memory_dependency_pct,
        resilience_dependency_pct=body.resilience_dependency_pct,
        economic_dependency_pct=body.economic_dependency_pct,
    )
    normalized = {
        system: bool(body.systems_ready.get(system, False))
        for system in SYSTEMS_56_TO_65
    }
    return operating_core_verdict(snapshot=snapshot, systems_ready=normalized)

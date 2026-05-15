"""
Governance Engine API — Engine 4 of the Agentic Enterprise Platform.

Read-only and audit-emitting endpoints. No endpoint sends or charges.
See docs/agentic_operations/AGENTIC_ENTERPRISE_PLATFORM.md.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from dealix.contracts.audit_log import AuditEntry
from dealix.contracts.decision import DecisionOutput
from dealix.engines import ENGINE_REGISTRY, all_status_reports
from dealix.engines.governance.engine import GOVERNANCE_ENGINE
from dealix.engines.governance.explainability import Explanation
from dealix.engines.governance.models import EvaluateResult
from dealix.engines.governance.risk import RiskSnapshot

router = APIRouter(prefix="/api/v1/governance-engine", tags=["governance-engine"])


@router.get("/status")
def get_status() -> dict[str, Any]:
    """Engine-layer summary + the Governance Engine's own status report."""
    specs = ENGINE_REGISTRY.all()
    status_counts: dict[str, int] = {}
    for spec in specs:
        status_counts[spec.status.value] = status_counts.get(spec.status.value, 0) + 1
    return {
        "platform": "Agentic Enterprise Platform",
        "engine_count": len(specs),
        "status_counts": status_counts,
        "governance_engine": GOVERNANCE_ENGINE.status_report(),
        "read_only": True,
    }


@router.get("/engines")
def list_engines() -> dict[str, Any]:
    """The registry — all 12 engines and their honest build status."""
    return {
        "engine_count": len(ENGINE_REGISTRY),
        "engines": [spec.to_dict() for spec in ENGINE_REGISTRY.all()],
    }


@router.get("/engines/status")
def engines_status() -> dict[str, Any]:
    """A status report for every engine (verifies each engine's foundation)."""
    return {"reports": all_status_reports()}


@router.post("/evaluate", response_model=EvaluateResult)
def evaluate_decision(
    decision: DecisionOutput,
    submit_approvals: bool = Query(
        default=False,
        description="When true, escalated actions also raise an approval request.",
    ),
) -> EvaluateResult:
    """Run a DecisionOutput's actions through policy; audit and explain each."""
    return GOVERNANCE_ENGINE.evaluate_decision(decision, submit_approvals=submit_approvals)


@router.get("/explain/{decision_id}", response_model=list[Explanation])
def explain_decision(decision_id: str) -> list[Explanation]:
    """Replay a previously-evaluated decision's audit chain into explanations."""
    return GOVERNANCE_ENGINE.explain_decision(decision_id)


@router.get("/risk-snapshot", response_model=RiskSnapshot)
def risk_snapshot() -> RiskSnapshot:
    """Aggregated, read-only risk posture across existing Dealix signals."""
    return GOVERNANCE_ENGINE.risk_snapshot()


@router.get("/audit/recent", response_model=list[AuditEntry])
def recent_audit(limit: int = Query(default=100, ge=1, le=1000)) -> list[AuditEntry]:
    """Most recent audit entries from the Governance Engine's audit sink."""
    return GOVERNANCE_ENGINE.recent_audit(limit=limit)

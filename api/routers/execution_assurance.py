"""Execution Assurance System HTTP surface.

  GET /api/v1/execution-assurance/status
  GET /api/v1/execution-assurance/scorecard
  GET /api/v1/execution-assurance/health
  GET /api/v1/execution-assurance/acceptance-gate
  GET /api/v1/execution-assurance/machines/{machine_id}

Read-only. Read-safe. Never invents green status.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.execution_assurance_os import (
    MATURITY_LEVELS,
    aggregate_score,
    build_full_ops_health,
    evaluate_acceptance_gate,
    evaluate_dod,
    load_machine_registry,
    score_machine,
    validate_registry,
)

router = APIRouter(
    prefix="/api/v1/execution-assurance",
    tags=["execution-assurance"],
)

_HARD_GATES: dict[str, bool] = {
    "no_fake_green": True,
    "maturity_attested_in_registry": True,
    "read_only": True,
    "every_score_traceable_to_dod": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    reg = load_machine_registry()
    ok, errors = validate_registry(reg)
    return {
        "service": "execution_assurance_os",
        "version": "1.0.0",
        "schema_version": reg.schema_version,
        "last_reviewed": reg.last_reviewed,
        "machines": len(reg.machines),
        "registry_valid": ok,
        "registry_errors": errors,
        "maturity_levels": MATURITY_LEVELS,
        "hard_gates": _HARD_GATES,
    }


@router.get("/scorecard")
async def scorecard() -> dict[str, Any]:
    reg = load_machine_registry()
    return {**aggregate_score(reg).to_dict(), "hard_gates": _HARD_GATES}


@router.get("/health")
async def health() -> dict[str, Any]:
    reg = load_machine_registry()
    return build_full_ops_health(reg).to_dict()


@router.get("/acceptance-gate")
async def acceptance_gate() -> dict[str, Any]:
    reg = load_machine_registry()
    gates = [evaluate_acceptance_gate(m) for m in reg.machines]
    return {
        "machines_total": len(gates),
        "machines_passing": sum(1 for g in gates if g.passed),
        "gates": [
            {
                "machine_id": g.machine_id,
                "passed": g.passed,
                "criteria": list(g.criteria),
                "unmet": list(g.unmet),
            }
            for g in gates
        ],
        "hard_gates": _HARD_GATES,
    }


@router.get("/machines/{machine_id}")
async def machine_detail(machine_id: str) -> dict[str, Any]:
    reg = load_machine_registry()
    spec = reg.get(machine_id)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"unknown machine: {machine_id}")
    score = score_machine(spec)
    dod = evaluate_dod(spec)
    gate = evaluate_acceptance_gate(spec)
    return {
        "machine_id": spec.id,
        "name": spec.name,
        "goal": spec.goal,
        "owner": spec.owner,
        "inputs": list(spec.inputs),
        "outputs": list(spec.outputs),
        "kpis": [
            {"name": k.name, "target": k.target, "unit": k.unit, "current": k.current}
            for k in spec.kpis
        ],
        "score": score.to_dict(),
        "definition_of_done": {
            "items_met": dod.items_met,
            "items_total": dod.items_total,
            "pct": dod.pct,
            "blocking_gaps": list(dod.blocking_gaps),
        },
        "acceptance_gate": {
            "passed": gate.passed,
            "criteria": list(gate.criteria),
            "unmet": list(gate.unmet),
        },
        "failure_modes": list(spec.failure_modes),
        "nist": spec.nist,
        "evidence_event_names": list(spec.evidence_event_names),
        "approval_required_actions": list(spec.approval_required_actions),
        "hard_gates": _HARD_GATES,
    }

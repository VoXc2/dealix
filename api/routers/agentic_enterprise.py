"""Agentic Enterprise OS API — maturity, coverage, evaluation, evolution, agents.

واجهة نظام تشغيل المؤسسة الوكيلة — النضج، التغطية، التقييم، التطوّر، الوكلاء.

Read-only aggregates. Capability scores are supplied per request; when they are
absent the maturity index is reported as ``null`` (Article 8 — no fabricated
maturity numbers).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from auto_client_acquisition.agentic_enterprise_os.coverage_registry import (
    coverage_registry,
    coverage_summary,
)
from auto_client_acquisition.agentic_enterprise_os.enterprise_maturity import (
    EnterpriseCapabilityScores,
    compute_emi,
    enterprise_maturity_stage,
)
from auto_client_acquisition.agentic_enterprise_os.evaluation_harness import (
    EvaluationReport,
    run_evaluation_harness,
)
from auto_client_acquisition.agentic_enterprise_os.evolution_loop import (
    EvolutionLoopResult,
    run_evolution_loop,
)
from auto_client_acquisition.agentic_enterprise_os.service_ladder import (
    enterprise_offer_recommendation,
)
from auto_client_acquisition.agentic_enterprise_os.unified_agent_view import (
    list_unified_agent_views,
)
from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision

router = APIRouter(prefix="/api/v1", tags=["agentic-enterprise"])

_CAPABILITY_FIELDS: tuple[str, ...] = (
    "redesign_workflows",
    "execute_workflows",
    "govern_workflows",
    "evaluate_workflows",
    "scale_workflows",
    "supervise_agents",
    "manage_digital_workforce",
    "generate_executive_intelligence",
    "measure_operational_impact",
    "improve_continuously",
)

_Score = float | None


def _governance_envelope(
    *,
    decision: GovernanceDecision = GovernanceDecision.ALLOW,
    matched_rules: tuple[str, ...] = (),
    risk_level: str = "low",
) -> dict[str, Any]:
    return {
        "governance_decision": decision.value,
        "matched_rules": list(matched_rules),
        "risk_level": risk_level,
    }


def _maturity_payload(values: dict[str, _Score]) -> dict[str, Any]:
    """Compute the maturity block, or report missing capabilities (no fabrication)."""
    provided = {k: v for k, v in values.items() if v is not None}
    if len(provided) < len(_CAPABILITY_FIELDS):
        return {
            "emi": None,
            "stage": None,
            "capabilities_provided": sorted(provided),
            "capabilities_missing": sorted(set(_CAPABILITY_FIELDS) - set(provided)),
            "note_ar": "زوّد القدرات العشر كاملة لحساب مؤشر النضج (لا تُختلق الأرقام).",
            "note_en": (
                "Provide all 10 capability scores to compute the maturity index "
                "(numbers are never fabricated)."
            ),
        }
    scores = EnterpriseCapabilityScores(
        **{field: float(values[field]) for field in _CAPABILITY_FIELDS}  # type: ignore[arg-type]
    )
    emi = compute_emi(scores)
    stage = enterprise_maturity_stage(emi)
    return {
        "emi": emi,
        "stage": {"key": stage.key, "ar": stage.label_ar, "en": stage.label_en},
        "capabilities": {field: float(values[field]) for field in _CAPABILITY_FIELDS},  # type: ignore[arg-type]
    }


def _evaluation_payload(report: EvaluationReport) -> dict[str, Any]:
    return {
        "overall_score": report.overall_score,
        "dimensions": [
            {
                "dimension": d.dimension,
                "score_0_100": d.score_0_100,
                "sample_size": d.sample_size,
                "evidence_ref": d.evidence_ref,
            }
            for d in report.dimensions
        ],
        "gaps": list(report.gaps),
    }


def _evolution_payload(result: EvolutionLoopResult) -> dict[str, Any]:
    return {
        "sources_present": result.sources_present,
        "recommendations": [
            {
                "priority": r.priority,
                "area": r.area,
                "rationale_ar": r.rationale_ar,
                "rationale_en": r.rationale_en,
                "source": r.source,
            }
            for r in result.recommendations
        ],
    }


@router.get("/enterprise/maturity")
async def enterprise_maturity(
    redesign_workflows: _Score = Query(None, ge=0, le=100),
    execute_workflows: _Score = Query(None, ge=0, le=100),
    govern_workflows: _Score = Query(None, ge=0, le=100),
    evaluate_workflows: _Score = Query(None, ge=0, le=100),
    scale_workflows: _Score = Query(None, ge=0, le=100),
    supervise_agents: _Score = Query(None, ge=0, le=100),
    manage_digital_workforce: _Score = Query(None, ge=0, le=100),
    generate_executive_intelligence: _Score = Query(None, ge=0, le=100),
    measure_operational_impact: _Score = Query(None, ge=0, le=100),
    improve_continuously: _Score = Query(None, ge=0, le=100),
) -> dict[str, Any]:
    """Enterprise Maturity Index + stage from the 10 capability scores."""
    values: dict[str, _Score] = {
        "redesign_workflows": redesign_workflows,
        "execute_workflows": execute_workflows,
        "govern_workflows": govern_workflows,
        "evaluate_workflows": evaluate_workflows,
        "scale_workflows": scale_workflows,
        "supervise_agents": supervise_agents,
        "manage_digital_workforce": manage_digital_workforce,
        "generate_executive_intelligence": generate_executive_intelligence,
        "measure_operational_impact": measure_operational_impact,
        "improve_continuously": improve_continuously,
    }
    return {**_governance_envelope(), "maturity": _maturity_payload(values)}


@router.get("/enterprise/systems")
async def enterprise_systems() -> dict[str, Any]:
    """Coverage of the 12 core systems, resolved from the codebase."""
    coverage = coverage_registry()
    return {
        **_governance_envelope(),
        "summary": coverage_summary(),
        "systems": [
            {
                "key": c.key,
                "name_ar": c.name_ar,
                "name_en": c.name_en,
                "status": c.status,
                "present_paths": list(c.present_paths),
                "missing_paths": list(c.missing_paths),
            }
            for c in coverage
        ],
    }


@router.get("/enterprise/evaluation")
async def enterprise_evaluation() -> dict[str, Any]:
    """Unified evaluation harness across the six dimensions.

    No evaluation results are recorded at request time, so every dimension is
    reported as a gap with ``overall_score`` ``null`` (Article 8).
    """
    report = run_evaluation_harness(())
    return {
        **_governance_envelope(),
        "evaluation": _evaluation_payload(report),
        "note_ar": "لا توجد نتائج تقييم مسجَّلة بعد — كل الأبعاد ثغرات.",
        "note_en": "No evaluation results recorded yet — every dimension is a gap.",
    }


@router.get("/enterprise/evolution")
async def enterprise_evolution() -> dict[str, Any]:
    """Continuous-evolution recommendations from available feedback sources."""
    result = run_evolution_loop()
    return {**_governance_envelope(), "evolution": _evolution_payload(result)}


@router.get("/enterprise/agents")
async def enterprise_agents() -> dict[str, Any]:
    """Unified Agent OS view over every registered agent."""
    views = list_unified_agent_views()
    return {
        **_governance_envelope(),
        "agents_total": len(views),
        "agents": [
            {
                "agent_id": v.agent_id,
                "name": v.name,
                "owner": v.owner,
                "purpose": v.purpose,
                "autonomy_level": v.autonomy_level,
                "status": v.status,
                "risk_score": v.risk_score,
                "risk_band": v.risk_band,
                "lifecycle_state": v.lifecycle_state,
                "governance_decision": v.governance_decision,
                "matched_rules": list(v.matched_rules),
            }
            for v in views
        ],
    }


@router.get("/enterprise/scorecard")
async def enterprise_scorecard(
    redesign_workflows: _Score = Query(None, ge=0, le=100),
    execute_workflows: _Score = Query(None, ge=0, le=100),
    govern_workflows: _Score = Query(None, ge=0, le=100),
    evaluate_workflows: _Score = Query(None, ge=0, le=100),
    scale_workflows: _Score = Query(None, ge=0, le=100),
    supervise_agents: _Score = Query(None, ge=0, le=100),
    manage_digital_workforce: _Score = Query(None, ge=0, le=100),
    generate_executive_intelligence: _Score = Query(None, ge=0, le=100),
    measure_operational_impact: _Score = Query(None, ge=0, le=100),
    improve_continuously: _Score = Query(None, ge=0, le=100),
) -> dict[str, Any]:
    """Combined capstone scorecard: maturity, coverage, evolution, and offer."""
    values: dict[str, _Score] = {
        "redesign_workflows": redesign_workflows,
        "execute_workflows": execute_workflows,
        "govern_workflows": govern_workflows,
        "evaluate_workflows": evaluate_workflows,
        "scale_workflows": scale_workflows,
        "supervise_agents": supervise_agents,
        "manage_digital_workforce": manage_digital_workforce,
        "generate_executive_intelligence": generate_executive_intelligence,
        "measure_operational_impact": measure_operational_impact,
        "improve_continuously": improve_continuously,
    }
    maturity = _maturity_payload(values)
    evolution = run_evolution_loop()
    scorecard: dict[str, Any] = {
        "maturity": maturity,
        "coverage": coverage_summary(),
        "evolution": _evolution_payload(evolution),
    }
    if maturity["emi"] is not None:
        scorecard["offer"] = enterprise_offer_recommendation(maturity["emi"])
    else:
        scorecard["offer"] = None
    return {**_governance_envelope(), "scorecard": scorecard}

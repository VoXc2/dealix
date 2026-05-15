"""Proof Pack v2 HTTP — generate score + retainer gate (governed, no sends)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.founder_command_summary.engagement_registry import merge_pipeline_stage
from auto_client_acquisition.proof_architecture_os.proof_to_retainer import (
    RetainerGateInput,
    retainer_gate_passes,
    retainer_path_recommendation,
)

router = APIRouter(prefix="/api/v1/proof-pack", tags=["proof-pack"])

PROOF_SECTION_KEYS: tuple[str, ...] = (
    "executive_summary",
    "problem",
    "inputs",
    "source_passports",
    "work_completed",
    "outputs",
    "quality_scores",
    "governance_decisions",
    "blocked_risks",
    "value_metrics",
    "limitations",
    "recommended_next_step",
    "capital_assets_created",
    "appendices",
)

COMPONENT_KEYS: tuple[str, ...] = (
    "source_evidence",
    "ai_run_evidence",
    "policy_evidence",
    "human_review_evidence",
    "approval_evidence",
    "output_evidence",
    "proof_evidence",
    "value_evidence",
)


def _gov(d: GovernanceDecision, *, rules: tuple[str, ...] = ()) -> dict[str, Any]:
    return {
        "governance_decision": d.value,
        "matched_rules": list(rules),
        "risk_level": "low" if d == GovernanceDecision.ALLOW else "medium",
    }


class ProofGenerateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sections: dict[str, Any] = Field(default_factory=dict)
    components: dict[str, Any] = Field(default_factory=dict)


def _nonempty_section(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, tuple, set)):
        return len(v) > 0
    if isinstance(v, dict):
        return len(v) > 0
    return True


@router.post("/{engagement_id}/generate")
def proof_generate(engagement_id: str, body: ProofGenerateBody = Body(default_factory=ProofGenerateBody)) -> dict[str, Any]:
    missing_s = [k for k in PROOF_SECTION_KEYS if k not in body.sections or not _nonempty_section(body.sections.get(k))]
    missing_c = [k for k in COMPONENT_KEYS if k not in body.components or not _nonempty_section(body.components.get(k))]
    if missing_s or missing_c:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": "أقسام أو مكوّنات ناقصة",
                "en": "Missing proof sections or components",
                "missing_sections": missing_s,
                "missing_components": missing_c,
            },
        )
    filled_s = sum(1 for k in PROOF_SECTION_KEYS if body.sections.get(k) not in (None, "", [], {}))
    filled_c = sum(1 for k in COMPONENT_KEYS if body.components.get(k) not in (None, "", [], {}))
    proof_score = round((filled_s / len(PROOF_SECTION_KEYS)) * 70 + (filled_c / len(COMPONENT_KEYS)) * 30)
    tier = "case_candidate" if proof_score >= 85 else ("sales_support" if proof_score >= 70 else ("internal_learning" if proof_score >= 55 else "weak"))
    snap = merge_pipeline_stage(
        engagement_id,
        proof_generated=True,
        proof_score=float(proof_score),
        pipeline_context_update={"proof_tier": tier},
    )
    return {
        **_gov(GovernanceDecision.ALLOW_WITH_REVIEW, rules=("proof_score_computed",)),
        "engagement_id": engagement_id,
        "proof_score": proof_score,
        "tier": tier,
        "sections_validated": list(PROOF_SECTION_KEYS),
        "components_validated": list(COMPONENT_KEYS),
        "founder_snapshot": snap.to_public_dict(),
    }


class RetainerGateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_health: int = Field(ge=0, le=100)
    workflow_recurring: bool = False
    owner_exists: bool = True
    monthly_value_clear: bool = False
    stakeholder_engaged: bool = False
    governance_risk_controlled: bool = True


@router.post("/{engagement_id}/retainer-gate")
def proof_retainer_gate(engagement_id: str, body: RetainerGateBody = Body(...)) -> dict[str, Any]:
    from auto_client_acquisition.founder_command_summary.engagement_registry import get_snapshot

    snap = get_snapshot(engagement_id)
    ps = int(snap.proof_score) if snap and snap.proof_score is not None else 0
    gate = RetainerGateInput(
        proof_score=ps,
        client_health=body.client_health,
        workflow_recurring=body.workflow_recurring,
        owner_exists=body.owner_exists,
        monthly_value_clear=body.monthly_value_clear and body.stakeholder_engaged,
        governance_risk_controlled=body.governance_risk_controlled and body.stakeholder_engaged,
    )
    ok, errs = retainer_gate_passes(gate)
    path = retainer_path_recommendation(retainer_gate_ok=ok, adjacent_capability_ready=body.workflow_recurring and body.monthly_value_clear)
    offer = {
        "continue": "Monthly RevOps OS (draft-first)",
        "expand": "Add Monthly Governance + Company Brain",
        "pause": "Enablement sprint before retainer",
    }[path.value]
    merge_pipeline_stage(
        engagement_id,
        retainer_evaluated=True,
        retainer_decision=path.value.capitalize(),
        client_health=float(body.client_health),
        pipeline_context_update={"retainer_errors": list(errs)},
    )
    return {
        **_gov(GovernanceDecision.ALLOW if ok else GovernanceDecision.REQUIRE_APPROVAL, rules=tuple(errs) or ("retainer_gate_passed",)),
        "engagement_id": engagement_id,
        "retainer_gate_ok": ok,
        "blocking_reasons": list(errs),
        "recommendation": path.value,
        "retainer_offer": offer,
    }

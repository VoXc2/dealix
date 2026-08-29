"""Bounded Company Brain & Governed AI Sprint assessment.

This productization layer reuses the existing Company Brain and governance
owners. It selects one measurable workflow hypothesis and prepares an internal
assessment; it never deploys, sends, quotes, or creates proof by assertion.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


class BrainSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    freshness_or_expiry: str = Field(..., min_length=1)
    permission_ref: str = Field(..., min_length=1)
    provenance: str = Field(..., min_length=1)
    contains_personal_data: bool = False


class WorkflowCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    outcome_hypothesis: str = Field(..., min_length=1)
    baseline_ref: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    accountable_owner: str = ""
    approval_path_ref: str = ""
    acceptance_criteria_ref: str = ""
    risk_class: str = "STANDARD"
    estimated_founder_minutes: float | None = Field(default=None, ge=0)
    estimated_delivery_effort_hours: float | None = Field(default=None, ge=0)


class CompanyBrainSprintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    relationship_ref: str = ""
    discovery_ref: str = ""
    authority_audit_ref: str = ""
    data_boundary_ref: str = ""
    sources: list[BrainSource] = Field(default_factory=list)
    workflow_candidates: list[WorkflowCandidate] = Field(default_factory=list)
    selected_workflow_id: str = ""
    customer_validation_ref: str = ""


class CompanyBrainSprintAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assessment_id: str
    account_id: str
    product: str = "COMPANY_BRAIN_GOVERNED_AI_SPRINT"
    status: str
    selected_workflow: dict[str, Any] | str
    source_registry: list[dict[str, Any]]
    missing_evidence: list[str]
    gates: dict[str, bool]
    deliverables: list[str]
    next_action: str
    authority: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class CompanyBrainSprintPlanner:
    """Prepare one bounded sprint from explicit sources and authority evidence."""

    def assess(self, request: CompanyBrainSprintRequest) -> CompanyBrainSprintAssessment:
        candidates = {item.workflow_id: item for item in request.workflow_candidates}
        selected = candidates.get(request.selected_workflow_id)
        missing: list[str] = []

        if not request.relationship_ref.strip():
            missing.append("verified relationship reference")
        if not request.discovery_ref.strip():
            missing.append("qualified discovery reference")
        if not request.authority_audit_ref.strip():
            missing.append("authority audit reference")
        if not request.data_boundary_ref.strip():
            missing.append("approved data boundary reference")
        if not request.sources:
            missing.append("permissioned source registry")
        if selected is None:
            missing.append("one selected workflow candidate")
        else:
            if not selected.baseline_ref.strip():
                missing.append("selected workflow baseline reference")
            if not selected.evidence_refs:
                missing.append("selected workflow evidence references")
            if not selected.accountable_owner.strip():
                missing.append("selected workflow accountable owner")
            if not selected.approval_path_ref.strip():
                missing.append("selected workflow approval path")
            if not selected.acceptance_criteria_ref.strip():
                missing.append("selected workflow acceptance criteria")
        if not request.customer_validation_ref.strip():
            missing.append("customer validation reference")

        ready = not missing
        source_registry = [
            source.model_dump(mode="json")
            for source in sorted(request.sources, key=lambda item: item.source_id)
        ]
        normalized = request.model_dump(mode="json")
        assessment_id = hashlib.sha256(
            json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:16]

        return CompanyBrainSprintAssessment(
            assessment_id=assessment_id,
            account_id=request.account_id,
            status="READY_FOR_CUSTOMER_SPECIFIC_SCOPE_REVIEW" if ready else "EVIDENCE_GAPS_BLOCK_SCOPE",
            selected_workflow=selected.model_dump(mode="json") if selected else UNKNOWN,
            source_registry=source_registry,
            missing_evidence=sorted(missing),
            gates={
                "relationship_verified": bool(request.relationship_ref.strip()),
                "qualified_discovery_verified": bool(request.discovery_ref.strip()),
                "authority_audit_verified": bool(request.authority_audit_ref.strip()),
                "data_boundary_verified": bool(request.data_boundary_ref.strip()),
                "source_registry_ready": bool(request.sources),
                "single_workflow_selected": selected is not None,
                "customer_validation_verified": bool(request.customer_validation_ref.strip()),
            },
            deliverables=[
                "context_and_authority_audit",
                "permissioned_source_registry",
                "single_bounded_workflow_design",
                "evaluation_and_exception_plan",
                "handover_and_operating_playbook",
                "baseline_to_outcome_proof_method",
            ],
            next_action=(
                "PREPARE_CUSTOMER_SPECIFIC_SCOPE_FOR_APPROVAL"
                if ready
                else "COLLECT_MISSING_EVIDENCE"
            ),
            authority={
                "quote": False,
                "external_send": False,
                "deployment": False,
                "production": False,
                "payment": False,
                "customer_value_claim": False,
            },
        )


__all__ = [
    "BrainSource",
    "CompanyBrainSprintAssessment",
    "CompanyBrainSprintPlanner",
    "CompanyBrainSprintRequest",
    "UNKNOWN",
    "WorkflowCandidate",
]

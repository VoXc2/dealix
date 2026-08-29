"""Bounded Company Brain & Governed AI Sprint assessment.

This productization layer reuses the existing Company Brain and governance
owners. It selects one measurable workflow hypothesis and prepares an internal
assessment; it never deploys, sends, quotes, or creates proof by assertion.

Compatibility fields from the first assessment version remain accepted, but a
Sprint cannot become ready for customer-specific scope review until the richer
source-registry and bounded-workflow evidence required by the canonical
contract is explicit.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


class BrainSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Compatibility identity / evidence refs.
    source_id: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    freshness_or_expiry: str = Field(..., min_length=1)
    permission_ref: str = Field(..., min_length=1)
    provenance: str = Field(..., min_length=1)
    contains_personal_data: bool = False

    # Canonical Company Brain registry evidence. These default empty so older
    # callers do not crash, but readiness fails closed until they are explicit.
    source_type: str = ""
    system_owner: str = ""
    tenant_scope: str = ""
    purpose: str = ""
    authority_or_lawful_basis: str = ""
    access_class: str = ""
    freshness_sla: str = ""
    last_verified_at: str = ""
    provenance_ref: str = ""
    retention_or_expiry: str = ""
    allowed_claims: list[str] | None = None
    prohibited_uses: list[str] | None = None
    pii_or_sensitive_class_if_any: str = ""

    def canonical_registry_entry(self) -> dict[str, Any]:
        """Return the explicit Company Brain source-registry shape.

        Older refs may fill semantically equivalent owner/authority/provenance
        fields for traceability, but they cannot invent freshness SLA, tenant
        scope, access class, claims policy, or verification time.
        """
        return {
            "source_id": self.source_id,
            "source_ref": self.source_ref,
            "source_type": self.source_type.strip() or UNKNOWN,
            "system_owner": self.system_owner.strip() or self.owner.strip() or UNKNOWN,
            "tenant_scope": self.tenant_scope.strip() or UNKNOWN,
            "purpose": self.purpose.strip() or UNKNOWN,
            "authority_or_lawful_basis": (
                self.authority_or_lawful_basis.strip()
                or self.permission_ref.strip()
                or UNKNOWN
            ),
            "access_class": self.access_class.strip() or UNKNOWN,
            "freshness_sla": self.freshness_sla.strip() or UNKNOWN,
            "last_verified_at": self.last_verified_at.strip() or UNKNOWN,
            "provenance_ref": (
                self.provenance_ref.strip() or self.provenance.strip() or UNKNOWN
            ),
            "retention_or_expiry": (
                self.retention_or_expiry.strip()
                or self.freshness_or_expiry.strip()
                or UNKNOWN
            ),
            "allowed_claims": (
                sorted({value.strip() for value in self.allowed_claims if value.strip()})
                if self.allowed_claims is not None
                else UNKNOWN
            ),
            "prohibited_uses": (
                sorted({value.strip() for value in self.prohibited_uses if value.strip()})
                if self.prohibited_uses is not None
                else UNKNOWN
            ),
            "pii_or_sensitive_class_if_any": (
                self.pii_or_sensitive_class_if_any.strip() or UNKNOWN
            ),
            "contains_personal_data": self.contains_personal_data,
            "compatibility_permission_ref": self.permission_ref,
        }

    def evidence_gaps(self) -> list[str]:
        gaps: list[str] = []
        required_strings = {
            "source_type": self.source_type,
            "system_owner": self.system_owner or self.owner,
            "tenant_scope": self.tenant_scope,
            "purpose": self.purpose,
            "authority_or_lawful_basis": self.authority_or_lawful_basis or self.permission_ref,
            "access_class": self.access_class,
            "freshness_sla": self.freshness_sla,
            "last_verified_at": self.last_verified_at,
            "provenance_ref": self.provenance_ref or self.provenance,
            "retention_or_expiry": self.retention_or_expiry or self.freshness_or_expiry,
            "pii_or_sensitive_class_if_any": self.pii_or_sensitive_class_if_any,
        }
        for name, value in required_strings.items():
            if not value.strip():
                gaps.append(f"source:{self.source_id}:{name}")
        if self.allowed_claims is None:
            gaps.append(f"source:{self.source_id}:allowed_claims")
        if self.prohibited_uses is None:
            gaps.append(f"source:{self.source_id}:prohibited_uses")
        return gaps


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

    # Bounded workflow contract. Optional for backward-compatible parsing,
    # mandatory before a selected use case is scope-ready.
    trigger: str = ""
    input_contract: str = ""
    deterministic_steps: list[str] | None = None
    ai_reasoning_steps_if_needed: list[str] | None = None
    tool_allowlist: list[str] | None = None
    authority_class: str = ""
    approval_points: list[str] | None = None
    output_contract: str = ""
    evidence_receipt: str = ""
    idempotency_key: str = ""
    retry_policy: str = ""
    rollback_or_safe_failure: str = ""
    human_handoff: str = ""
    evaluation_cases: list[str] | None = None

    def contract_gaps(self) -> list[str]:
        gaps: list[str] = []
        required_strings = {
            "baseline_ref": self.baseline_ref,
            "accountable_owner": self.accountable_owner,
            "approval_path_ref": self.approval_path_ref,
            "acceptance_criteria_ref": self.acceptance_criteria_ref,
            "trigger": self.trigger,
            "input_contract": self.input_contract,
            "authority_class": self.authority_class,
            "output_contract": self.output_contract,
            "evidence_receipt": self.evidence_receipt,
            "idempotency_key": self.idempotency_key,
            "retry_policy": self.retry_policy,
            "rollback_or_safe_failure": self.rollback_or_safe_failure,
            "human_handoff": self.human_handoff,
        }
        for name, value in required_strings.items():
            if not value.strip():
                gaps.append(f"workflow:{self.workflow_id}:{name}")
        if not self.evidence_refs:
            gaps.append(f"workflow:{self.workflow_id}:evidence_refs")
        for name, value in {
            "deterministic_steps": self.deterministic_steps,
            "ai_reasoning_steps_if_needed": self.ai_reasoning_steps_if_needed,
            "tool_allowlist": self.tool_allowlist,
            "approval_points": self.approval_points,
            "evaluation_cases": self.evaluation_cases,
        }.items():
            if value is None:
                gaps.append(f"workflow:{self.workflow_id}:{name}")
        return gaps


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

    # Explicit assessment context. Empty remains UNKNOWN, never inferred.
    business_objective: str = ""
    named_problem: str = ""
    current_workflow: str = ""
    current_manual_steps: list[str] | None = None
    desired_outcome: str = ""
    proof_method: str = ""
    risk_and_regulatory_class: str = ""
    integration_constraints: list[str] | None = None


class CompanyBrainSprintAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assessment_id: str
    account_id: str
    product: str = "COMPANY_BRAIN_GOVERNED_AI_SPRINT"
    status: str
    selected_workflow: dict[str, Any] | str
    source_registry: list[dict[str, Any]]
    missing_evidence: list[str]
    source_registry_gaps: list[str]
    workflow_contract_gaps: list[str]
    gates: dict[str, bool]
    deliverables: list[str]
    next_action: str
    customer_validation_state: str
    authority: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class CompanyBrainSprintPlanner:
    """Prepare one bounded sprint from explicit sources and authority evidence."""

    def assess(self, request: CompanyBrainSprintRequest) -> CompanyBrainSprintAssessment:
        candidates = {item.workflow_id: item for item in request.workflow_candidates}
        selected = candidates.get(request.selected_workflow_id)
        missing: list[str] = []

        required_request_refs = {
            "verified relationship reference": request.relationship_ref,
            "qualified discovery reference": request.discovery_ref,
            "authority audit reference": request.authority_audit_ref,
            "approved data boundary reference": request.data_boundary_ref,
            "customer validation reference": request.customer_validation_ref,
        }
        for name, value in required_request_refs.items():
            if not value.strip():
                missing.append(name)

        required_context = {
            "business objective": request.business_objective,
            "named business problem": request.named_problem,
            "current workflow state": request.current_workflow,
            "desired outcome": request.desired_outcome,
            "proof method": request.proof_method,
            "risk and regulatory class": request.risk_and_regulatory_class,
        }
        for name, value in required_context.items():
            if not value.strip():
                missing.append(name)
        if request.current_manual_steps is None:
            missing.append("current manual steps explicitly assessed")
        if request.integration_constraints is None:
            missing.append("integration constraints explicitly assessed")

        if not request.sources:
            missing.append("permissioned source registry")
        source_registry = [
            source.canonical_registry_entry()
            for source in sorted(request.sources, key=lambda item: item.source_id)
        ]
        source_gaps = sorted(
            {
                gap
                for source in request.sources
                for gap in source.evidence_gaps()
            }
        )
        missing.extend(source_gaps)

        workflow_gaps: list[str] = []
        if selected is None:
            missing.append("one selected workflow candidate")
        else:
            workflow_gaps = sorted(set(selected.contract_gaps()))
            missing.extend(workflow_gaps)

        # A customer-validation ref means a reference was supplied for scope
        # review. It is not treated as verified customer-value evidence here.
        customer_validation_state = (
            "REFERENCE_PRESENT_NOT_CUSTOMER_VALUE_PROOF"
            if request.customer_validation_ref.strip()
            else UNKNOWN
        )

        missing = sorted(set(missing))
        ready = not missing
        normalized = request.model_dump(mode="json")
        assessment_id = hashlib.sha256(
            json.dumps(
                normalized,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()[:16]

        return CompanyBrainSprintAssessment(
            assessment_id=assessment_id,
            account_id=request.account_id,
            status=(
                "READY_FOR_CUSTOMER_SPECIFIC_SCOPE_REVIEW"
                if ready
                else "EVIDENCE_GAPS_BLOCK_SCOPE"
            ),
            selected_workflow=(
                selected.model_dump(mode="json") if selected else UNKNOWN
            ),
            source_registry=source_registry,
            missing_evidence=missing,
            source_registry_gaps=source_gaps,
            workflow_contract_gaps=workflow_gaps,
            gates={
                "relationship_reference_present": bool(request.relationship_ref.strip()),
                "qualified_discovery_reference_present": bool(request.discovery_ref.strip()),
                "authority_audit_reference_present": bool(request.authority_audit_ref.strip()),
                "data_boundary_reference_present": bool(request.data_boundary_ref.strip()),
                "source_registry_contract_complete": bool(request.sources) and not source_gaps,
                "single_workflow_selected": selected is not None,
                "bounded_workflow_contract_complete": selected is not None and not workflow_gaps,
                "customer_validation_reference_present": bool(request.customer_validation_ref.strip()),
                "customer_validation_verified": False,
                "assessment_context_complete": all(
                    value.strip() for value in required_context.values()
                )
                and request.current_manual_steps is not None
                and request.integration_constraints is not None,
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
            customer_validation_state=customer_validation_state,
            authority={
                "relationship_truth": False,
                "source_write": False,
                "tool_authority_expansion": False,
                "tenant_boundary_bypass": False,
                "quote": False,
                "contract": False,
                "external_send": False,
                "deployment": False,
                "production": False,
                "payment": False,
                "customer_value_claim": False,
                "public_customer_proof": False,
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

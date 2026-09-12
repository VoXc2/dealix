"""Stateless customer-value transition authority for the canonical Proof Ledger.

This module is deliberately persistence-neutral. It does not create another
ledger. It validates whether a caller may append a transition to the existing
canonical Proof Ledger / Company Machine.

Truth law:
WORK_COMPLETED != DELIVERED != CUSTOMER_ACCEPTED != CUSTOMER_VALIDATED_VALUE != PUBLIC_PROOF
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CustomerValueState(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    WORK_COMPLETED = "WORK_COMPLETED"
    DELIVERED = "DELIVERED"
    CUSTOMER_ACCEPTED = "CUSTOMER_ACCEPTED"
    CUSTOMER_VALIDATED_VALUE = "CUSTOMER_VALIDATED_VALUE"
    PUBLIC_PROOF = "PUBLIC_PROOF"


_STATE_ORDER = list(CustomerValueState)


class CustomerValueEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    work_completion_refs: list[str] = Field(default_factory=list)
    delivery_receipt_refs: list[str] = Field(default_factory=list)
    customer_acceptance_refs: list[str] = Field(default_factory=list)
    customer_value_validation_refs: list[str] = Field(default_factory=list)
    public_proof_permission_refs: list[str] = Field(default_factory=list)
    measurement_basis_refs: list[str] = Field(default_factory=list)


class CustomerValueDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    current_state: CustomerValueState
    requested_state: CustomerValueState
    allowed: bool
    missing_evidence: list[str]
    proof_ledger_event_allowed: bool
    public_claim_allowed: bool
    reason: str


def _has(refs: list[str]) -> bool:
    return any(ref.strip() for ref in refs)


def authorize_customer_value_transition(
    current: CustomerValueState,
    requested: CustomerValueState,
    evidence: CustomerValueEvidence,
) -> CustomerValueDecision:
    current_idx = _STATE_ORDER.index(current)
    requested_idx = _STATE_ORDER.index(requested)

    if requested_idx < current_idx:
        return CustomerValueDecision(
            current_state=current,
            requested_state=requested,
            allowed=False,
            missing_evidence=[],
            proof_ledger_event_allowed=False,
            public_claim_allowed=False,
            reason="STATE_REGRESSION_REQUIRES_EXPLICIT_CORRECTION_WORKFLOW",
        )
    if requested_idx > current_idx + 1:
        return CustomerValueDecision(
            current_state=current,
            requested_state=requested,
            allowed=False,
            missing_evidence=["sequential_state_evidence"],
            proof_ledger_event_allowed=False,
            public_claim_allowed=False,
            reason="CANNOT_SKIP_CUSTOMER_VALUE_STATES",
        )
    if requested == current:
        return CustomerValueDecision(
            current_state=current,
            requested_state=requested,
            allowed=True,
            missing_evidence=[],
            proof_ledger_event_allowed=False,
            public_claim_allowed=current == CustomerValueState.PUBLIC_PROOF,
            reason="NO_STATE_CHANGE",
        )

    required: dict[CustomerValueState, tuple[str, bool]] = {
        CustomerValueState.WORK_COMPLETED: ("work_completion_refs", _has(evidence.work_completion_refs)),
        CustomerValueState.DELIVERED: ("delivery_receipt_refs", _has(evidence.delivery_receipt_refs)),
        CustomerValueState.CUSTOMER_ACCEPTED: ("customer_acceptance_refs", _has(evidence.customer_acceptance_refs)),
        CustomerValueState.CUSTOMER_VALIDATED_VALUE: (
            "customer_value_validation_refs+measurement_basis_refs",
            _has(evidence.customer_value_validation_refs) and _has(evidence.measurement_basis_refs),
        ),
        CustomerValueState.PUBLIC_PROOF: (
            "public_proof_permission_refs",
            _has(evidence.public_proof_permission_refs),
        ),
    }
    requirement = required.get(requested)
    if requirement is None:
        return CustomerValueDecision(
            current_state=current,
            requested_state=requested,
            allowed=False,
            missing_evidence=["unsupported_transition"],
            proof_ledger_event_allowed=False,
            public_claim_allowed=False,
            reason="UNSUPPORTED_TRANSITION",
        )

    name, satisfied = requirement
    if not satisfied:
        return CustomerValueDecision(
            current_state=current,
            requested_state=requested,
            allowed=False,
            missing_evidence=[name],
            proof_ledger_event_allowed=False,
            public_claim_allowed=False,
            reason="MISSING_REQUIRED_EVIDENCE",
        )

    return CustomerValueDecision(
        current_state=current,
        requested_state=requested,
        allowed=True,
        missing_evidence=[],
        proof_ledger_event_allowed=True,
        public_claim_allowed=requested == CustomerValueState.PUBLIC_PROOF,
        reason="EVIDENCE_GATE_PASSED",
    )


__all__ = [
    "CustomerValueState",
    "CustomerValueEvidence",
    "CustomerValueDecision",
    "authorize_customer_value_transition",
]

"""System 33 — Human-AI operating model decisions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DelegationRequest:
    task_id: str
    risk_level: str
    requires_external_action: bool
    confidence: float
    explanation_available: bool
    human_owner: str

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id_required")
        if not self.human_owner.strip():
            raise ValueError("human_owner_required")
        if self.risk_level not in {"low", "medium", "high"}:
            raise ValueError("invalid_risk_level")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence_out_of_range")


@dataclass(frozen=True)
class OversightDecision:
    mode: str
    requires_approval: bool
    can_human_override: bool
    can_rollback: bool
    trust_state: str


def evaluate_human_ai_request(request: DelegationRequest) -> OversightDecision:
    requires_approval = (
        request.requires_external_action
        or request.risk_level == "high"
        or request.confidence < 0.7
    )
    mode = "human_supervised" if requires_approval else "delegated_autonomous"
    trusted = request.explanation_available and request.confidence >= 0.8 and request.risk_level != "high"
    trust_state = "trusted" if trusted else "review_required"
    return OversightDecision(
        mode=mode,
        requires_approval=requires_approval,
        can_human_override=True,
        can_rollback=True,
        trust_state=trust_state,
    )

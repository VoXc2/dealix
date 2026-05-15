"""Pydantic request/response models for the Governance Engine API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dealix.engines.governance.explainability import Explanation
from dealix.trust.policy import PolicyDecision


class ActionEvaluation(BaseModel):
    """The governance verdict for a single NextAction."""

    model_config = ConfigDict(extra="forbid")

    action_type: str
    verdict: PolicyDecision
    rule_fired: str
    reason: str
    required_approvers: int = 0
    audit_id: str
    approval_request_id: str | None = None
    explanation: Explanation


class EvaluateResult(BaseModel):
    """The full governance result for a DecisionOutput."""

    model_config = ConfigDict(extra="forbid")

    decision_id: str
    entity_id: str
    objective: str
    evaluations: list[ActionEvaluation] = Field(default_factory=list)
    audit_ids: list[str] = Field(default_factory=list)
    note: str | None = None

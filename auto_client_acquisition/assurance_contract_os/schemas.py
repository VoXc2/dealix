"""Schemas for System 28 — the Assurance Contract Engine."""

from __future__ import annotations

from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ContractType(StrEnum):
    EXECUTION = "execution"
    PERMISSION = "permission"
    ROLLBACK = "rollback"
    EVALUATION = "evaluation"
    GOVERNANCE = "governance"


class ContractDecision(StrEnum):
    """Mirrors the Trust Plane PolicyEvaluator vocabulary."""

    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


class AssuranceContract(BaseModel):
    """What an agent may see / propose / execute, and which checks gate it."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    contract_id: str = Field(default_factory=lambda: f"ctr_{uuid4().hex[:12]}")
    contract_type: ContractType
    agent_id: str
    action_type: str
    may_see: list[str] = Field(default_factory=list)
    may_propose: list[str] = Field(default_factory=list)
    may_execute: list[str] = Field(default_factory=list)
    precondition_checks: list[str] = Field(default_factory=list)
    rollback_plan: str | None = None
    is_external: bool = False
    is_irreversible: bool = False


class ContractCheckResult(BaseModel):
    """Outcome of evaluating an action against its contract."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    contract_id: str | None
    agent_id: str
    action_type: str
    passed: bool
    decision: ContractDecision
    failed_checks: list[str] = Field(default_factory=list)
    reason: str = ""

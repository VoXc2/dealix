"""Typed records for the lead_qualification governed workflow.

Pure dataclasses — no DB, no LLM, no HTTP. ``GovernanceDecision`` strings
come from ``compliance_trust_os.approval_engine``; severity ordering lets
the orchestrator compute a worst-case decision across all steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision

# Worst-case ordering: a higher value is a stricter decision.
GOVERNANCE_SEVERITY: dict[str, int] = {
    GovernanceDecision.ALLOW: 0,
    GovernanceDecision.ALLOW_WITH_REVIEW: 1,
    GovernanceDecision.DRAFT_ONLY: 2,
    GovernanceDecision.REDACT: 3,
    GovernanceDecision.REQUIRE_APPROVAL: 4,
    GovernanceDecision.ESCALATE: 5,
    GovernanceDecision.BLOCK: 6,
}

# Permission required to run a lead-qualification workflow (RBAC, step 3).
REQUIRED_PERMISSION = "leads:write"


def worst_governance(decisions: list[str]) -> str:
    """Return the strictest decision in ``decisions`` (defaults to ALLOW)."""
    if not decisions:
        return str(GovernanceDecision.ALLOW)
    return str(max(decisions, key=lambda d: GOVERNANCE_SEVERITY.get(d, 0)))


@dataclass(frozen=True, slots=True)
class LeadInput:
    """A single inbound lead plus the discovery answers that drive scoring."""

    lead_id: str
    tenant_slug: str
    actor_role: str
    source: str
    company_name: str
    sector: str = "b2b_services"
    region: str = "riyadh"
    notes: str = ""
    # ICP discovery answers (0-100 each).
    icp_b2b_service_fit: int = 60
    icp_data_maturity: int = 55
    icp_governance_posture: int = 60
    icp_budget_signal: int = 55
    icp_decision_velocity: int = 55
    # Client-risk signals.
    wants_scraping_or_spam: bool = False
    wants_guaranteed_sales: bool = False
    unclear_pain: bool = False
    no_owner: bool = False
    data_not_ready: bool = False
    budget_unknown: bool = False
    # Qualification gates.
    accepts_governance: bool = True
    proof_path_possible: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LeadInput:
        fields = set(cls.__dataclass_fields__)
        return cls(**{k: v for k, v in data.items() if k in fields})


@dataclass(slots=True)
class StepResult:
    """Outcome of one workflow step. ``governance_decision`` is mandatory."""

    step_id: str
    artifact_kind: str
    governance_decision: str
    ok: bool = True
    blocked: bool = False
    reason: str = ""
    artifact: dict[str, Any] = field(default_factory=dict)
    latency_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "artifact_kind": self.artifact_kind,
            "governance_decision": self.governance_decision,
            "ok": self.ok,
            "blocked": self.blocked,
            "reason": self.reason,
            "artifact": self.artifact,
            "latency_ms": self.latency_ms,
        }


@dataclass(slots=True)
class WorkflowOutput:
    """Final result of a lead_qualification run."""

    run_id: str
    workflow_id: str
    state: str
    governance_decision: str
    steps: list[dict[str, Any]] = field(default_factory=list)
    audit: list[dict[str, Any]] = field(default_factory=list)
    eval_report: dict[str, Any] = field(default_factory=dict)
    dashboard_card: dict[str, Any] = field(default_factory=dict)
    approval_id: str = ""
    blocked_reason: str = ""

    @property
    def completed(self) -> bool:
        return self.state == "completed"

    @property
    def paused_for_approval(self) -> bool:
        return self.state == "paused_for_approval"


__all__ = [
    "GOVERNANCE_SEVERITY",
    "REQUIRED_PERMISSION",
    "LeadInput",
    "StepResult",
    "WorkflowOutput",
    "worst_governance",
]

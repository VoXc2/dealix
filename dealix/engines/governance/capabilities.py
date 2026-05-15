"""
The six sub-capabilities of the Governance Engine.

Each capability is a thin facade over an existing Dealix subsystem. The
Governance Engine *composes* these facades — it never reimplements policy,
approval, or audit logic.

Reuse vs. new:
  * policy        — 100% reuse of dealix.trust.policy.PolicyEvaluator
  * approval      — 100% reuse of dealix.trust.approval.ApprovalCenter
  * audit         — 100% reuse of dealix.trust.audit.AuditSink
  * compliance    — facade over auto_client_acquisition governance lawful-basis
  * risk          — facade over dealix.engines.governance.risk (composes signals)
  * explainability— NEW production code (dealix.engines.governance.explainability)
"""

from __future__ import annotations

from typing import Any

from dealix.contracts.audit_log import AuditEntry
from dealix.contracts.decision import DecisionOutput, NextAction
from dealix.engines.governance.explainability import (
    Explanation,
    explain_evaluation,
    explain_from_audit,
)
from dealix.engines.governance.risk import RiskSnapshot, build_risk_snapshot
from dealix.trust.approval import ApprovalCenter, ApprovalRequest
from dealix.trust.audit import AuditSink
from dealix.trust.policy import PolicyEvaluator, PolicyResult

CAPABILITY_CATALOG: list[dict[str, str]] = [
    {"name": "policy", "source": "dealix.trust.policy", "kind": "reuse"},
    {"name": "approval", "source": "dealix.trust.approval", "kind": "reuse"},
    {"name": "audit", "source": "dealix.trust.audit", "kind": "reuse"},
    {"name": "compliance", "source": "auto_client_acquisition.governance_os", "kind": "facade"},
    {"name": "risk", "source": "dealix.engines.governance.risk", "kind": "facade"},
    {"name": "explainability", "source": "dealix.engines.governance.explainability", "kind": "new"},
]


class PolicyCapability:
    """Facade over the Trust Plane's PolicyEvaluator."""

    def __init__(self, evaluator: PolicyEvaluator) -> None:
        self._evaluator = evaluator

    def evaluate(self, action: NextAction, decision: DecisionOutput) -> PolicyResult:
        return self._evaluator.evaluate(action, decision)

    def rule_names(self) -> list[str]:
        return [r.name for r in self._evaluator.rules]


class ApprovalCapability:
    """Facade over the Trust Plane's ApprovalCenter."""

    def __init__(self, center: ApprovalCenter) -> None:
        self._center = center

    def submit(
        self, decision: DecisionOutput, action: NextAction, required_approvers: int
    ) -> ApprovalRequest:
        return self._center.submit(
            decision=decision, action=action, required_approvers=required_approvers
        )

    def list_pending(self) -> list[ApprovalRequest]:
        return self._center.list_pending()


class AuditCapability:
    """Facade over the Trust Plane's append-only AuditSink."""

    def __init__(self, sink: AuditSink) -> None:
        self._sink = sink

    def append(self, entry: AuditEntry) -> AuditEntry:
        self._sink.append(entry)
        return entry

    def recent(self, limit: int = 100) -> list[AuditEntry]:
        return self._sink.recent(limit=limit)

    def for_decision(self, decision_id: str) -> list[AuditEntry]:
        return [e for e in self._sink.recent(limit=10_000) if e.decision_id == decision_id]


class ComplianceCapability:
    """Facade over the Saudi governance lawful-basis vocabulary."""

    def lawful_bases(self) -> list[dict[str, str]]:
        from auto_client_acquisition.governance_os.lawful_basis import (
            LawfulBasis,
            describe_basis,
        )

        return [{"basis": b.value, "description": describe_basis(b)} for b in LawfulBasis]


class RiskCapability:
    """Facade over the composed risk snapshot."""

    def snapshot(self) -> RiskSnapshot:
        return build_risk_snapshot()


class ExplainabilityCapability:
    """Facade over the net-new explainability module."""

    def explain_evaluation(
        self,
        action: NextAction,
        decision: DecisionOutput,
        policy_result: PolicyResult,
        audit_refs: list[str] | None = None,
    ) -> Explanation:
        return explain_evaluation(action, decision, policy_result, audit_refs)

    def explain_from_audit(
        self, decision_id: str, audit_entries: list[AuditEntry]
    ) -> list[Explanation]:
        return explain_from_audit(decision_id, audit_entries)


class GovernanceCapabilities:
    """The six capabilities, bundled for the Governance Engine."""

    def __init__(
        self,
        evaluator: PolicyEvaluator,
        approval_center: ApprovalCenter,
        audit_sink: AuditSink,
    ) -> None:
        self.policy = PolicyCapability(evaluator)
        self.approval = ApprovalCapability(approval_center)
        self.audit = AuditCapability(audit_sink)
        self.compliance = ComplianceCapability()
        self.risk = RiskCapability()
        self.explainability = ExplainabilityCapability()

    def catalog(self) -> list[dict[str, Any]]:
        return [dict(item) for item in CAPABILITY_CATALOG]

"""
Governance Engine (Engine 4) — production-depth governance for the platform.

Composes the Trust Plane (policy, approval, audit) with two facades
(compliance, risk) and one net-new capability (explainability) into a single
engine. Every evaluation is appended to the append-only audit log — honoring
the `no_unaudited_changes` non-negotiable.

The engine is read-only and audit-emitting: it never sends or charges.
"""

from __future__ import annotations

from typing import Any

from dealix.contracts.audit_log import AuditAction, AuditEntry
from dealix.contracts.decision import DecisionOutput
from dealix.engines.base import BaseEngine
from dealix.engines.governance.capabilities import GovernanceCapabilities
from dealix.engines.governance.explainability import Explanation
from dealix.engines.governance.models import ActionEvaluation, EvaluateResult
from dealix.engines.governance.risk import RiskSnapshot
from dealix.engines.registry import ENGINE_REGISTRY
from dealix.trust.approval import ApprovalCenter
from dealix.trust.audit import AuditSink, InMemoryAuditSink
from dealix.trust.policy import PolicyDecision, PolicyEvaluator

_POLICY_AUDIT_ACTION: dict[PolicyDecision, AuditAction] = {
    PolicyDecision.ALLOW: AuditAction.POLICY_ALLOWED,
    PolicyDecision.DENY: AuditAction.POLICY_DENIED,
    PolicyDecision.ESCALATE: AuditAction.POLICY_ESCALATED,
}


class GovernanceEngine(BaseEngine):
    """Engine 4 — policy, approval, audit, explainability, compliance, risk."""

    spec = ENGINE_REGISTRY.get("governance")

    def __init__(
        self,
        *,
        policy_evaluator: PolicyEvaluator | None = None,
        approval_center: ApprovalCenter | None = None,
        audit_sink: AuditSink | None = None,
    ) -> None:
        self._audit_sink: AuditSink = audit_sink or InMemoryAuditSink()
        self.capabilities = GovernanceCapabilities(
            evaluator=policy_evaluator or PolicyEvaluator(),
            approval_center=approval_center or ApprovalCenter(),
            audit_sink=self._audit_sink,
        )

    # ── core: evaluate a decision ────────────────────────────────
    def evaluate_decision(
        self, decision: DecisionOutput, *, submit_approvals: bool = False
    ) -> EvaluateResult:
        """Run every NextAction through policy, audit it, and explain it.

        When `submit_approvals` is set, escalated actions also raise an
        approval request through the Approval Center.
        """
        result = EvaluateResult(
            decision_id=decision.decision_id,
            entity_id=decision.entity_id,
            objective=decision.objective,
        )

        if not decision.next_actions:
            result.note = "Decision carried no next_actions — nothing to evaluate."
            return result

        for action in decision.next_actions:
            policy_result = self.capabilities.policy.evaluate(action, decision)

            audit_entry = AuditEntry(
                action=_POLICY_AUDIT_ACTION[policy_result.decision],
                actor_type="system",
                actor_id="governance_engine",
                decision_id=decision.decision_id,
                entity_id=decision.entity_id,
                approval_class=action.approval_class,
                reversibility_class=action.reversibility_class,
                sensitivity_class=action.sensitivity_class,
                outcome=policy_result.decision.value,
                reason=policy_result.reason,
                details={"action_type": action.action_type, "rule": policy_result.rule_name},
            )
            self.capabilities.audit.append(audit_entry)
            result.audit_ids.append(audit_entry.audit_id)

            approval_request_id: str | None = None
            if submit_approvals and policy_result.decision == PolicyDecision.ESCALATE:
                request = self.capabilities.approval.submit(
                    decision=decision,
                    action=action,
                    required_approvers=policy_result.required_approvers or 1,
                )
                approval_request_id = request.request_id
                approval_audit = AuditEntry(
                    action=AuditAction.APPROVAL_REQUESTED,
                    actor_type="system",
                    actor_id="governance_engine",
                    decision_id=decision.decision_id,
                    entity_id=decision.entity_id,
                    approval_class=action.approval_class,
                    reversibility_class=action.reversibility_class,
                    sensitivity_class=action.sensitivity_class,
                    details={
                        "action_type": action.action_type,
                        "approval_request_id": request.request_id,
                        "approvers_needed": request.approvers_needed,
                    },
                )
                self.capabilities.audit.append(approval_audit)
                result.audit_ids.append(approval_audit.audit_id)

            explanation = self.capabilities.explainability.explain_evaluation(
                action, decision, policy_result, audit_refs=[audit_entry.audit_id]
            )
            result.evaluations.append(
                ActionEvaluation(
                    action_type=action.action_type,
                    verdict=policy_result.decision,
                    rule_fired=policy_result.rule_name,
                    reason=policy_result.reason,
                    required_approvers=policy_result.required_approvers,
                    audit_id=audit_entry.audit_id,
                    approval_request_id=approval_request_id,
                    explanation=explanation,
                )
            )

        return result

    # ── explainability replay ────────────────────────────────────
    def explain_decision(self, decision_id: str) -> list[Explanation]:
        """Replay a decision's audit chain into structured explanations."""
        entries = self.capabilities.audit.for_decision(decision_id)
        return self.capabilities.explainability.explain_from_audit(decision_id, entries)

    # ── risk + audit passthroughs ────────────────────────────────
    def risk_snapshot(self) -> RiskSnapshot:
        return self.capabilities.risk.snapshot()

    def recent_audit(self, limit: int = 100) -> list[AuditEntry]:
        return self.capabilities.audit.recent(limit=limit)

    # ── BaseEngine contract ──────────────────────────────────────
    def _domain_report(self) -> dict[str, Any]:
        return {
            "capabilities": self.capabilities.catalog(),
            "policy_rules": self.capabilities.policy.rule_names(),
            "audit_entries": len(self.recent_audit(limit=10_000)),
            "pending_approvals": len(self.capabilities.approval.list_pending()),
        }


# Process-wide engine — audit accumulates across API requests.
GOVERNANCE_ENGINE = GovernanceEngine()

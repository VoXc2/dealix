"""
Explainability — the one genuinely net-new Governance capability.

Dealix already has policy, approval, and audit. What it lacks is a structured,
bilingual account of *why* a decision was governed the way it was. This module
turns a policy evaluation (or a replayed audit chain) into an `Explanation`:
which rule fired, the evidence behind it, and the approval path.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dealix.contracts.audit_log import AuditEntry
from dealix.contracts.decision import DecisionOutput, NextAction
from dealix.trust.policy import PolicyDecision, PolicyResult

_VERDICT_AR: dict[str, str] = {
    PolicyDecision.ALLOW.value: "مسموح",
    PolicyDecision.DENY.value: "مرفوض",
    PolicyDecision.ESCALATE.value: "يتطلب موافقة بشرية",
}


class Explanation(BaseModel):
    """A structured, bilingual account of one governance decision."""

    model_config = ConfigDict(extra="forbid")

    decision_id: str
    action_type: str
    verdict: str  # allow | deny | escalate
    rule_fired: str
    reason: str
    evidence_sources: list[str] = Field(default_factory=list)
    required_approvers: int = 0
    approval_class: str | None = None
    audit_refs: list[str] = Field(default_factory=list)
    human_readable_en: str
    human_readable_ar: str


def _readable_en(action_type: str, verdict: str, rule: str, reason: str, approvers: int) -> str:
    if verdict == PolicyDecision.ALLOW.value:
        return f"Action '{action_type}' was allowed: {reason} (rule: {rule})."
    if verdict == PolicyDecision.DENY.value:
        return f"Action '{action_type}' was denied: {reason} (rule: {rule})."
    return (
        f"Action '{action_type}' requires human approval from {approvers} approver(s): "
        f"{reason} (rule: {rule})."
    )


def _readable_ar(action_type: str, verdict: str, rule: str, approvers: int) -> str:
    verdict_ar = _VERDICT_AR.get(verdict, verdict)
    if verdict == PolicyDecision.ESCALATE.value:
        return (
            f"الإجراء '{action_type}' {verdict_ar} ويحتاج {approvers} معتمد — "
            f"بموجب القاعدة '{rule}'."
        )
    return f"الإجراء '{action_type}' {verdict_ar} بموجب القاعدة '{rule}'."


def explain_evaluation(
    action: NextAction,
    decision: DecisionOutput,
    policy_result: PolicyResult,
    audit_refs: list[str] | None = None,
) -> Explanation:
    """Explain a fresh policy evaluation, with full evidence context."""
    verdict = policy_result.decision.value
    return Explanation(
        decision_id=decision.decision_id,
        action_type=action.action_type,
        verdict=verdict,
        rule_fired=policy_result.rule_name,
        reason=policy_result.reason,
        evidence_sources=[e.source for e in decision.evidence],
        required_approvers=policy_result.required_approvers,
        approval_class=action.approval_class.value,
        audit_refs=audit_refs or [],
        human_readable_en=_readable_en(
            action.action_type,
            verdict,
            policy_result.rule_name,
            policy_result.reason,
            policy_result.required_approvers,
        ),
        human_readable_ar=_readable_ar(
            action.action_type, verdict, policy_result.rule_name, policy_result.required_approvers
        ),
    )


_POLICY_ACTIONS = {"policy.allowed", "policy.denied", "policy.escalated"}


def explain_from_audit(decision_id: str, audit_entries: list[AuditEntry]) -> list[Explanation]:
    """Replay a decision's audit chain into explanations.

    Evidence sources are not stored in the audit log, so a replayed
    explanation carries an empty `evidence_sources` list — this is honest:
    the replay reconstructs the *governance* path, not the original evidence.
    """
    explanations: list[Explanation] = []
    for entry in audit_entries:
        if entry.decision_id != decision_id:
            continue
        if entry.action.value not in _POLICY_ACTIONS:
            continue
        action_type = str(entry.details.get("action_type", "unknown"))
        rule = str(entry.details.get("rule", "unknown"))
        verdict = entry.outcome
        reason = entry.reason or ""
        explanations.append(
            Explanation(
                decision_id=decision_id,
                action_type=action_type,
                verdict=verdict,
                rule_fired=rule,
                reason=reason,
                evidence_sources=[],
                required_approvers=0,
                approval_class=entry.approval_class.value,
                audit_refs=[entry.audit_id],
                human_readable_en=_readable_en(action_type, verdict, rule, reason, 0),
                human_readable_ar=_readable_ar(action_type, verdict, rule, 0),
            )
        )
    return explanations

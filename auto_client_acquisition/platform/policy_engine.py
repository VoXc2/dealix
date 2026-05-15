"""Runtime policy decision engine."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ActionRisk(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class PolicyDecision(StrEnum):
    ALLOW = 'allow'
    APPROVAL_REQUIRED = 'approval_required'
    BLOCK = 'block'


@dataclass(frozen=True, slots=True)
class PolicyEvaluation:
    decision: PolicyDecision
    reasons: tuple[str, ...]
    policy_version: str = 'platform-v1'


def evaluate_policy(
    *,
    action_name: str,
    is_external: bool,
    risk: ActionRisk,
    permissions: tuple[str, ...],
    requires_data_access: bool,
) -> PolicyEvaluation:
    reasons: list[str] = []
    if risk == ActionRisk.CRITICAL:
        reasons.append('critical_risk_blocked')
        return PolicyEvaluation(decision=PolicyDecision.BLOCK, reasons=tuple(reasons))
    if requires_data_access and 'memory:read' not in permissions:
        reasons.append('missing_memory_read_permission')
        return PolicyEvaluation(decision=PolicyDecision.BLOCK, reasons=tuple(reasons))
    if is_external and 'external:execute:approved' not in permissions:
        reasons.append('external_action_requires_approval_permission')
        return PolicyEvaluation(decision=PolicyDecision.APPROVAL_REQUIRED, reasons=tuple(reasons))
    if risk == ActionRisk.HIGH:
        reasons.append('high_risk_requires_approval')
        return PolicyEvaluation(decision=PolicyDecision.APPROVAL_REQUIRED, reasons=tuple(reasons))
    reasons.append(f'action_allowed:{action_name}')
    return PolicyEvaluation(decision=PolicyDecision.ALLOW, reasons=tuple(reasons))


__all__ = ['ActionRisk', 'PolicyDecision', 'PolicyEvaluation', 'evaluate_policy']

"""Risk-policy-approval evaluation for enterprise workflow actions."""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.enterprise_infrastructure.schemas import (
    GovernanceDecision,
    GovernanceOutcome,
    RiskLevel,
)


@dataclass(frozen=True, slots=True)
class PolicyConfig:
    """Governance policy surface used by the runtime."""

    forbidden_actions: tuple[str, ...] = (
        "whatsapp.cold_send",
        "linkedin.auto_dm",
        "gmail.external_send",
        "calendar.external_create",
    )
    approval_required_actions: tuple[str, ...] = (
        "whatsapp.send_message",
        "pricing.commitment",
    )
    risk_threshold_for_approval: int = 65
    risk_threshold_for_block: int = 90
    risk_weights: dict[RiskLevel, int] = field(
        default_factory=lambda: {
            "low": 20,
            "medium": 50,
            "high": 75,
        }
    )


def evaluate_governance(
    *,
    action: str,
    step_risk_level: RiskLevel,
    agent_permission: GovernanceDecision,
    policy: PolicyConfig | None = None,
) -> GovernanceOutcome:
    cfg = policy or PolicyConfig()
    reasons: list[str] = []

    if action in cfg.forbidden_actions:
        reasons.append("forbidden_action")
        return GovernanceOutcome(decision="block", risk_score=100, reasons=tuple(reasons))

    if agent_permission == "block":
        reasons.append("agent_permission_denied")
        return GovernanceOutcome(decision="block", risk_score=100, reasons=tuple(reasons))

    risk_score = cfg.risk_weights[step_risk_level]
    if "send" in action:
        risk_score += 10
        reasons.append("external_send_path")
    if "pricing" in action:
        risk_score += 15
        reasons.append("commercial_commitment")
    risk_score = min(100, risk_score)

    if risk_score >= cfg.risk_threshold_for_block:
        reasons.append("risk_threshold_block")
        return GovernanceOutcome(decision="block", risk_score=risk_score, reasons=tuple(reasons))

    needs_approval = (
        action in cfg.approval_required_actions
        or agent_permission == "require_approval"
        or risk_score >= cfg.risk_threshold_for_approval
    )
    if needs_approval:
        reasons.append("approval_required")
        return GovernanceOutcome(
            decision="require_approval",
            risk_score=risk_score,
            reasons=tuple(reasons),
        )

    return GovernanceOutcome(decision="allow", risk_score=risk_score, reasons=tuple(reasons))

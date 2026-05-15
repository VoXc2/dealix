"""Agent auditability card — maps to auditable agents dimensions (MVP)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentAuditabilityCard:
    agent_id: str
    audit_scope: tuple[str, ...]
    action_recoverability: str
    lifecycle_coverage: str
    policy_checkability: str
    responsibility_attribution: str
    evidence_integrity: str
    external_actions_allowed: bool


def agent_auditability_card_valid(card: AgentAuditabilityCard) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not card.agent_id.strip():
        errors.append("agent_id_required")
    if not card.audit_scope:
        errors.append("audit_scope_required")
    for field in (
        "action_recoverability",
        "lifecycle_coverage",
        "policy_checkability",
        "responsibility_attribution",
        "evidence_integrity",
    ):
        if not getattr(card, field).strip():
            errors.append(f"{field}_required")
    if card.external_actions_allowed:
        errors.append("external_actions_not_allowed_mvp")
    return not errors, tuple(errors)

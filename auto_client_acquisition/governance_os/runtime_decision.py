"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    source_passport_valid_for_ai,
)


def governance_decision_from_policy_check(result: PolicyCheckResult) -> GovernanceDecision:
    if not result.allowed:
        return GovernanceDecision.BLOCK
    if result.verdict == PolicyVerdict.ALLOW_WITH_REVIEW:
        return GovernanceDecision.ALLOW_WITH_REVIEW
    return GovernanceDecision.ALLOW


def governance_decision_from_passport_ai_gate(ok: bool, errors: tuple[str, ...]) -> GovernanceDecision:
    """Align passport validation errors with runtime governance vocabulary."""
    if ok:
        return GovernanceDecision.ALLOW
    if errors == ("pii_external_use_requires_approval_workflow",):
        return GovernanceDecision.REQUIRE_APPROVAL
    return GovernanceDecision.BLOCK


@dataclass(frozen=True, slots=True)
class RuntimeDecision:
    """Runtime governance verdict for a requested action."""

    decision: GovernanceDecision
    reasons: tuple[str, ...] = field(default_factory=tuple)
    safe_alternative: str | None = None


def decide(*, action: str, context: dict[str, Any] | None = None) -> RuntimeDecision:
    """Decide whether ``action`` may run given a Source Passport context.

    Deterministic, dependency-free runtime gate used by Data OS endpoints.
    """
    ctx = context or {}
    passport = ctx.get("source_passport")
    contains_pii = bool(ctx.get("contains_pii", False))
    external_use = bool(ctx.get("external_use", False))

    if passport is None:
        return RuntimeDecision(
            decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=("no_source_passport_provided",),
            safe_alternative="attach a Source Passport before any external use",
        )

    if external_use and not getattr(passport, "external_use_allowed", False):
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=("external_use_not_permitted_by_passport",),
            safe_alternative="keep results internal or update the Source Passport",
        )

    if contains_pii and external_use:
        return RuntimeDecision(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("pii_external_use_requires_approval_workflow",),
            safe_alternative="route through the human approval workflow",
        )

    ok, errors = source_passport_valid_for_ai(passport)
    if not ok:
        return RuntimeDecision(
            decision=GovernanceDecision.BLOCK,
            reasons=tuple(errors),
            safe_alternative="resolve passport errors before running AI scoring",
        )

    return RuntimeDecision(
        decision=GovernanceDecision.ALLOW,
        reasons=(f"{action}_permitted",),
        safe_alternative=None,
    )


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]

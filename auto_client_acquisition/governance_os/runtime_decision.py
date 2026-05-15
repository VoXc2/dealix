"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import (
    PolicyCheckResult,
    PolicyVerdict,
    policy_check_draft,
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
class GovernanceResult:
    """Outcome of a runtime governance decision.

    ``safe_alternative`` is a short, machine-stable hint for the caller when
    the action is not cleanly allowed.
    """

    decision: GovernanceDecision
    reasons: tuple[str, ...]
    safe_alternative: str = ""


def decide(*, action: str, context: dict[str, Any] | None = None) -> GovernanceResult:
    """Single runtime governance entry point for an action + context.

    Two paths:
    - When ``context`` carries draft ``text``, the draft is run through the
      ``policy_check_draft`` gate (forbidden claims / channels).
    - Otherwise the action is treated as a data/AI operation and gated on the
      Source Passport: PII + external use requires approval; a missing passport
      degrades to ALLOW_WITH_REVIEW.

    Never raises; always returns a ``GovernanceResult``.
    """
    ctx = context or {}

    text = str(ctx.get("text", "") or "")
    if text.strip():
        pc = policy_check_draft(text)
        return GovernanceResult(
            decision=governance_decision_from_policy_check(pc),
            reasons=tuple(pc.issues),
            safe_alternative=(
                "" if pc.allowed
                else "revise the draft to remove the flagged language before review"
            ),
        )

    passport = ctx.get("source_passport")
    contains_pii = bool(ctx.get("contains_pii", False))
    external_use = bool(ctx.get("external_use", False))

    if passport is None:
        return GovernanceResult(
            decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=("no_source_passport",),
            safe_alternative="attach a validated Source Passport before AI use",
        )
    if contains_pii and external_use:
        return GovernanceResult(
            decision=GovernanceDecision.REQUIRE_APPROVAL,
            reasons=("pii_external_use_requires_approval_workflow",),
            safe_alternative="route through the approval workflow before any external use of PII",
        )
    return GovernanceResult(decision=GovernanceDecision.ALLOW, reasons=())


__all__ = [
    "GovernanceDecision",
    "GovernanceResult",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]

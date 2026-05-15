"""Runtime governance decisions.

Two layers live here:

  * mapping helpers — translate lightweight policy/passport checks into the
    compliance ``GovernanceDecision`` vocabulary;
  * :func:`decide` — the single runtime entry point callers use to govern an
    action before it executes. It returns a :class:`RuntimeDecision` carrying
    the decision, machine-readable reasons, and a safe alternative.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict

# Actions that always escalate to a human regardless of context — external,
# irreversible, or financially binding.
_HIGH_RISK_ACTIONS = frozenset(
    {
        "send_external_message",
        "whatsapp.send_message",
        "crm.update_deal",
        "pricing_commitment",
        "contract_commitment",
        "refund",
        "delete_customer_data",
    }
)

_DRAFT_ACTIONS = frozenset({"generate_draft", "draft_text", "draft"})
_SCORING_ACTIONS = frozenset({"run_scoring", "score_accounts", "analyze_data"})


@dataclass(frozen=True, slots=True)
class RuntimeDecision:
    """Outcome of a runtime governance evaluation."""

    decision: GovernanceDecision
    reasons: tuple[str, ...] = ()
    safe_alternative: str | None = None
    risk_level: str = "low"
    approval_required: bool = False


def decide(
    *,
    action: str,
    context: dict | None = None,
    actor: str = "system",
) -> RuntimeDecision:
    """Govern ``action`` before it executes.

    ``context`` is a free-form dict; recognised keys per action family:

      * draft actions  — ``text``, ``channel``, ``is_cold``
      * scoring actions — ``source_passport``, ``contains_pii``, ``external_use``

    High-risk actions always escalate. Unknown actions degrade safely to
    ``ALLOW_WITH_REVIEW`` rather than silently allowing.
    """
    context = context or {}

    if action in _DRAFT_ACTIONS:
        issues = audit_draft_text(str(context.get("text", "")))
        if issues:
            return RuntimeDecision(
                decision=GovernanceDecision.BLOCK,
                reasons=tuple(issues),
                safe_alternative="revise_draft_remove_flagged_terms",
                risk_level="high",
            )
        if bool(context.get("is_cold", False)):
            return RuntimeDecision(
                decision=GovernanceDecision.REQUIRE_APPROVAL,
                reasons=("cold_outreach_requires_human_approval",),
                safe_alternative="warm_intro_or_inbound_only",
                risk_level="medium",
                approval_required=True,
            )
        return RuntimeDecision(
            decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            reasons=("draft_clean_human_review_still_required",),
        )

    if action in _SCORING_ACTIONS:
        contains_pii = bool(context.get("contains_pii", False))
        external_use = bool(context.get("external_use", False))
        if context.get("source_passport") is None:
            return RuntimeDecision(
                decision=GovernanceDecision.ALLOW_WITH_REVIEW,
                reasons=("no_source_passport_provided",),
                safe_alternative="request_source_passport",
                risk_level="medium",
            )
        if contains_pii and external_use:
            return RuntimeDecision(
                decision=GovernanceDecision.REQUIRE_APPROVAL,
                reasons=("pii_external_use_requires_approval_workflow",),
                safe_alternative="internal_analysis_only",
                risk_level="high",
                approval_required=True,
            )
        if contains_pii:
            return RuntimeDecision(
                decision=GovernanceDecision.ALLOW_WITH_REVIEW,
                reasons=("contains_pii_internal_review_required",),
                risk_level="medium",
            )
        return RuntimeDecision(
            decision=GovernanceDecision.ALLOW,
            reasons=("source_passport_present",),
        )

    if action in _HIGH_RISK_ACTIONS:
        return RuntimeDecision(
            decision=GovernanceDecision.ESCALATE,
            reasons=(f"high_risk_action:{action}",),
            safe_alternative="draft_only",
            risk_level="high",
            approval_required=True,
        )

    return RuntimeDecision(
        decision=GovernanceDecision.ALLOW_WITH_REVIEW,
        reasons=(f"unclassified_action:{action}",),
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


__all__ = [
    "GovernanceDecision",
    "RuntimeDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]

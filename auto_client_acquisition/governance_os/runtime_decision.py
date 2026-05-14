"""Runtime governance decision — the single authority for every action.

Combines the lightweight policy-check mappers used by the API tests with
the rich ``decide(action, context)`` entry point that the data_os router,
delivery_sprint factory, and monthly_report consumers rely on.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import (
    PolicyCheckResult,
    PolicyVerdict,
)


@dataclass(frozen=True)
class DecisionResult:
    decision: GovernanceDecision
    reasons: tuple[str, ...] = ()
    safe_alternative: str = ""


def governance_decision_from_policy_check(result: PolicyCheckResult) -> GovernanceDecision:
    if not result.allowed:
        return GovernanceDecision.BLOCK
    if result.verdict == PolicyVerdict.ALLOW_WITH_REVIEW:
        return GovernanceDecision.ALLOW_WITH_REVIEW
    return GovernanceDecision.ALLOW


def governance_decision_from_passport_ai_gate(
    ok: bool, errors: tuple[str, ...]
) -> GovernanceDecision:
    """Align passport validation errors with runtime governance vocabulary."""
    if ok:
        return GovernanceDecision.ALLOW
    if errors == ("pii_external_use_requires_approval_workflow",):
        return GovernanceDecision.REQUIRE_APPROVAL
    return GovernanceDecision.BLOCK


_HARD_BLOCKED_ACTIONS = frozenset({
    "scrape_web",
    "scrape_linkedin",
    "scrape_email",
    "bulk_cold_outreach",
    "linkedin_send",
    "linkedin_automate",
})


def _hardest(a: GovernanceDecision, b: GovernanceDecision) -> GovernanceDecision:
    order = {
        GovernanceDecision.ALLOW: 0,
        GovernanceDecision.ALLOW_WITH_REVIEW: 1,
        GovernanceDecision.DRAFT_ONLY: 2,
        GovernanceDecision.REQUIRE_APPROVAL: 3,
        GovernanceDecision.REDACT: 4,
        GovernanceDecision.ESCALATE: 5,
        GovernanceDecision.BLOCK: 6,
    }
    return a if order[a] >= order[b] else b


def decide(*, action: str, context: dict[str, Any] | None = None) -> DecisionResult:
    """Single-authority governance decision.

    Context keys (all optional): ``source_passport``, ``intended_use``,
    ``channel``, ``mode``, ``is_cold``, ``explicit_consent``,
    ``contains_pii``, ``external_use``, ``text``, ``declared_action``.
    """
    # Lazy imports to keep the module light at import time and avoid
    # cycles with data_os/governance_os.
    from auto_client_acquisition.data_os.source_passport import (
        SourcePassport,
        requires_approval,
        validate,
    )
    from auto_client_acquisition.governance_os.channel_policy import is_forbidden
    from auto_client_acquisition.governance_os.claim_safety import contains_unsafe_claim

    ctx = context or {}
    reasons: list[str] = []
    decision = GovernanceDecision.ALLOW
    safe_alt = ""

    if action in _HARD_BLOCKED_ACTIONS:
        return DecisionResult(
            decision=GovernanceDecision.BLOCK,
            reasons=(f"action {action!r} is hard-blocked by Dealix non-negotiables",),
            safe_alternative="draft_only output for human review",
        )

    channel = str(ctx.get("channel", "")).lower()
    mode = str(ctx.get("mode", "")).lower()
    if channel:
        if not mode:
            if ctx.get("is_cold"):
                mode = "cold"
            elif "automate" in action.lower():
                mode = "automate"
            elif "scrape" in action.lower():
                mode = "scrape"
        if mode:
            forbidden, why = is_forbidden(channel=channel, mode=mode)
            if forbidden:
                return DecisionResult(
                    decision=GovernanceDecision.BLOCK,
                    reasons=(why,),
                    safe_alternative="draft_only message for human review",
                )

    if channel == "whatsapp":
        if ctx.get("is_cold") and not ctx.get("explicit_consent"):
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=("cold WhatsApp without explicit_consent is blocked",),
                safe_alternative="draft only; human delivers via warm intro",
            )

    passport = ctx.get("source_passport")
    intended_use = str(ctx.get("intended_use", "internal_analysis"))
    needs_passport_actions = {
        "run_scoring",
        "generate_draft",
        "export_outreach",
        "analyze_records",
        "score_accounts",
    }
    if action in needs_passport_actions or action.startswith(("score_", "draft_", "generate_")):
        if passport is None:
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=("no_source_passport: AI use requires a SourcePassport",),
                safe_alternative="request a SourcePassport from the client before processing",
            )
        result = validate(passport)
        if not result.is_valid:
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=("invalid_source_passport",) + tuple(result.reasons),
                safe_alternative="fix the passport (missing/invalid fields) and retry",
            )
        if isinstance(passport, SourcePassport) and requires_approval(passport, intended_use):
            decision = _hardest(decision, GovernanceDecision.REQUIRE_APPROVAL)
            reasons.append("passport_requires_approval_for_intended_use")

    if ctx.get("contains_pii") and ctx.get("external_use"):
        decision = _hardest(decision, GovernanceDecision.REQUIRE_APPROVAL)
        reasons.append("pii_external_use_requires_approval")
    elif ctx.get("contains_pii"):
        decision = _hardest(decision, GovernanceDecision.ALLOW_WITH_REVIEW)
        reasons.append("pii_internal_use_review_required")

    text = str(ctx.get("text", ""))
    if text:
        unsafe, why_list = contains_unsafe_claim(text)
        if unsafe:
            decision = _hardest(decision, GovernanceDecision.REDACT)
            reasons.extend(f"unsafe_claim:{w}" for w in why_list)
            safe_alt = safe_alt or "remove guarantee/100% language; restate as observed outcome"

    external_send = action.startswith(("send_", "post_", "publish_")) or "_send" in action
    if external_send and channel:
        decision = _hardest(decision, GovernanceDecision.DRAFT_ONLY)
        reasons.append("external_send_default_draft_only")

    if channel and ("draft" in action.lower() or action.startswith(f"{channel}_draft")):
        decision = _hardest(decision, GovernanceDecision.DRAFT_ONLY)
        reasons.append(f"{channel}_draft_human_posts_manually")

    return DecisionResult(
        decision=decision,
        reasons=tuple(reasons),
        safe_alternative=safe_alt,
    )


__all__ = [
    "DecisionResult",
    "GovernanceDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]

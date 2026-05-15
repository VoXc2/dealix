"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict


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


# ── Single-authority runtime decision (consumed by routers + delivery) ──
from dataclasses import dataclass  # noqa: E402
from typing import Any  # noqa: E402


@dataclass(frozen=True)
class DecisionResult:
    decision: GovernanceDecision
    reasons: tuple[str, ...] = ()
    safe_alternative: str = ""


# Hard-blocked actions — always BLOCK regardless of context (non-negotiables).
_HARD_BLOCKED_ACTIONS = frozenset({
    "scrape_web",
    "scrape_linkedin",
    "scrape_email",
    "bulk_cold_outreach",
    "linkedin_send",
    "linkedin_automate",
})

_DECISION_ORDER: dict[GovernanceDecision, int] = {
    GovernanceDecision.ALLOW: 0,
    GovernanceDecision.ALLOW_WITH_REVIEW: 1,
    GovernanceDecision.DRAFT_ONLY: 2,
    GovernanceDecision.REQUIRE_APPROVAL: 3,
    GovernanceDecision.REDACT: 4,
    GovernanceDecision.ESCALATE: 5,
    GovernanceDecision.BLOCK: 6,
}


def _hardest(a: GovernanceDecision, b: GovernanceDecision) -> GovernanceDecision:
    """Return the more-restrictive of two decisions."""
    return a if _DECISION_ORDER[a] >= _DECISION_ORDER[b] else b


def decide(*, action: str, context: dict[str, Any] | None = None) -> DecisionResult:
    """Single-authority governance decision.

    Context keys (all optional): ``source_passport``, ``intended_use``,
    ``channel``, ``is_cold``, ``explicit_consent``, ``contains_pii``,
    ``external_use``.
    """
    ctx = context or {}
    reasons: list[str] = []
    decision = GovernanceDecision.ALLOW

    # 1. Hard-blocked actions — scraping / LinkedIn automation / bulk cold.
    if action in _HARD_BLOCKED_ACTIONS:
        return DecisionResult(
            decision=GovernanceDecision.BLOCK,
            reasons=(f"action {action!r} is hard-blocked by Dealix non-negotiables",),
            safe_alternative="draft_only output for human review",
        )

    # 2. Cold WhatsApp without explicit consent — block.
    if str(ctx.get("channel", "")).lower() == "whatsapp":
        if ctx.get("is_cold") and not ctx.get("explicit_consent"):
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=("cold WhatsApp without explicit_consent is blocked",),
                safe_alternative="draft only; human delivers via warm intro",
            )

    # 3. Source Passport gating for AI processing actions.
    needs_passport = action.startswith(("score_", "draft_", "generate_", "analyze_")) or action in {
        "run_scoring",
        "export_outreach",
        "analyze_records",
    }
    if needs_passport:
        from auto_client_acquisition.data_os.source_passport import requires_approval, validate

        passport = ctx.get("source_passport")
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
        if requires_approval(passport, str(ctx.get("intended_use", "internal_analysis"))):
            decision = _hardest(decision, GovernanceDecision.REQUIRE_APPROVAL)
            reasons.append("passport_requires_approval_for_intended_use")

    # 4. PII handling.
    if ctx.get("contains_pii") and ctx.get("external_use"):
        decision = _hardest(decision, GovernanceDecision.REQUIRE_APPROVAL)
        reasons.append("pii_external_use_requires_approval")
    elif ctx.get("contains_pii"):
        decision = _hardest(decision, GovernanceDecision.ALLOW_WITH_REVIEW)
        reasons.append("pii_internal_use_review_required")

    # 5. External-send actions default to DRAFT_ONLY.
    if action.startswith(("send_", "post_", "publish_")) or "_send" in action:
        decision = _hardest(decision, GovernanceDecision.DRAFT_ONLY)
        reasons.append("external_send_default_draft_only")

    return DecisionResult(decision=decision, reasons=tuple(reasons))


__all__ = [
    "DecisionResult",
    "GovernanceDecision",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]

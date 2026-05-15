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

# Per-action default ``intended_use`` so a caller that omits it is not
# escalated against the wrong passport-use key (e.g. a scoring workload
# checked against ``internal_analysis``). Values are from
# ``source_passport.ALLOWED_USES``.
_ACTION_DEFAULT_USE: dict[str, str] = {
    "run_scoring": "scoring",
    "score_accounts": "scoring",
    "generate_draft": "draft_only",
    "export_outreach": "draft_only",
    "analyze_records": "internal_analysis",
}


def _default_intended_use(action: str) -> str:
    """Best-fit intended_use for an action when the caller omits it."""
    if action in _ACTION_DEFAULT_USE:
        return _ACTION_DEFAULT_USE[action]
    if action.startswith("score_"):
        return "scoring"
    if action.startswith(("draft_", "generate_")):
        return "draft_only"
    return "internal_analysis"


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
    from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety

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
    # Strict boolean — a loose-payload string ("false", "0") must never
    # count as consent; consent is fail-closed.
    explicit_consent = ctx.get("explicit_consent") is True

    # Cold WhatsApp: explicit consent turns it into a consented (warm)
    # contact. Resolve this BEFORE the generic forbidden-mode sweep so a
    # consented request is not hard-blocked by the ("whatsapp","cold")
    # rule — otherwise the consent check below would be unreachable.
    whatsapp_cold_consented = False
    if channel == "whatsapp" and ctx.get("is_cold"):
        if not explicit_consent:
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=("cold WhatsApp without explicit_consent is blocked",),
                safe_alternative="draft only; human delivers via warm intro",
            )
        whatsapp_cold_consented = True

    # Infer mode from is_cold / action when the caller did not set it.
    if not mode:
        if ctx.get("is_cold") and not whatsapp_cold_consented:
            mode = "cold"
        elif "automate" in action.lower():
            mode = "automate"
        elif "scrape" in action.lower():
            mode = "scrape"

    # Forbidden-mode sweep — runs whenever a mode is known, with or without
    # a channel, so mode="scrape" still hits the non-negotiable scraping
    # ban. A consented WhatsApp contact is exempt only from the cold rule.
    if mode and not (whatsapp_cold_consented and mode == "cold"):
        forbidden, why = is_forbidden(channel=channel, mode=mode)
        if forbidden:
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=(why,),
                safe_alternative="draft_only message for human review",
            )

    passport = ctx.get("source_passport")
    intended_use = str(ctx.get("intended_use") or _default_intended_use(action))
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
        claim = audit_claim_safety(text)
        if claim.issues:
            # Preserve claim-safety severity: a forbidden marketing claim
            # (guarantees, fake proof) escalates harder than an operational
            # term (e.g. "scraping") mentioned in a policy/negation context.
            forbidden_claim = any(
                i.startswith("forbidden_claim:") for i in claim.issues
            )
            decision = _hardest(decision, claim.suggested_decision)
            reasons.extend(f"unsafe_claim:{w}" for w in claim.issues)
            if forbidden_claim:
                safe_alt = safe_alt or (
                    "remove guarantee/100% language; restate as observed outcome"
                )
            else:
                safe_alt = safe_alt or (
                    "keep operational terms in a negation/policy context only; "
                    "human review before any external use"
                )

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

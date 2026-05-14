"""Runtime governance decision — the single authority for every action.

decide(action, context) → DecisionResult with one of seven GovernanceDecision
values. Composes existing repo facilities:

- channel_policy_gateway.policy.check_channel_policy for channel + action mix
- channel_policy (this package) for hard-forbidden channel modes
- claim_safety for unsafe claim detection
- data_os.source_passport.validate / requires_approval for passport gating
- safety_v10.output_validator (if present) for declared-action vs content
  mismatches — kept light-weight to avoid a heavy import chain in tests

Every output object across Dealix must carry the resulting decision in a
`governance_decision` field. Enforced by
tests/test_output_requires_governance_status.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from auto_client_acquisition.data_os.source_passport import (
    SourcePassport,
    requires_approval,
    validate,
)
from auto_client_acquisition.governance_os.channel_policy import is_forbidden
from auto_client_acquisition.governance_os.claim_safety import contains_unsafe_claim


class GovernanceDecision(StrEnum):
    ALLOW = "allow"
    ALLOW_WITH_REVIEW = "allow_with_review"
    DRAFT_ONLY = "draft_only"
    REQUIRE_APPROVAL = "require_approval"
    REDACT = "redact"
    BLOCK = "block"
    ESCALATE = "escalate"


@dataclass(frozen=True)
class DecisionResult:
    decision: GovernanceDecision
    reasons: tuple[str, ...] = ()
    safe_alternative: str = ""


# Hard-blocked actions — always BLOCK regardless of context.
_HARD_BLOCKED_ACTIONS = frozenset({
    "scrape_web",
    "scrape_linkedin",
    "scrape_email",
    "bulk_cold_outreach",
    "linkedin_send",
    "linkedin_automate",
})


def _hardest(a: GovernanceDecision, b: GovernanceDecision) -> GovernanceDecision:
    """Take the more-restrictive of two decisions."""
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

    Context keys (all optional):
    - source_passport: SourcePassport | None
    - intended_use: str
    - channel: str ("whatsapp", "email", "linkedin", "web", "any")
    - mode: str ("draft", "send", "automate", "scrape", "bulk", "cold")
    - is_cold: bool
    - explicit_consent: bool
    - contains_pii: bool
    - external_use: bool
    - text: str (the proposed output text — claim-safety scans it)
    - declared_action: str
    """
    ctx = context or {}
    reasons: list[str] = []
    decision = GovernanceDecision.ALLOW
    safe_alt = ""

    # 1. Hard-blocked actions.
    if action in _HARD_BLOCKED_ACTIONS:
        return DecisionResult(
            decision=GovernanceDecision.BLOCK,
            reasons=(f"action {action!r} is hard-blocked by Dealix non-negotiables",),
            safe_alternative="draft_only output for human review",
        )

    # 2. Hard-forbidden channel × mode combinations.
    channel = str(ctx.get("channel", "")).lower()
    mode = str(ctx.get("mode", "")).lower()
    if channel:
        # Derive an implicit mode from common booleans if mode not provided.
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

    # 3. WhatsApp cold-without-consent — block.
    if channel == "whatsapp":
        if ctx.get("is_cold") and not ctx.get("explicit_consent"):
            return DecisionResult(
                decision=GovernanceDecision.BLOCK,
                reasons=("cold WhatsApp without explicit_consent is blocked",),
                safe_alternative="draft only; human delivers via warm intro",
            )

    # 4. Source Passport gating.
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

    # 5. Explicit PII handling.
    if ctx.get("contains_pii") and ctx.get("external_use"):
        decision = _hardest(decision, GovernanceDecision.REQUIRE_APPROVAL)
        reasons.append("pii_external_use_requires_approval")
    elif ctx.get("contains_pii"):
        # PII used internally still requires a reviewer eye even when not
        # going external — never silently ALLOW.
        decision = _hardest(decision, GovernanceDecision.ALLOW_WITH_REVIEW)
        reasons.append("pii_internal_use_review_required")

    # 6. Claim safety on proposed text.
    text = str(ctx.get("text", ""))
    if text:
        unsafe, why_list = contains_unsafe_claim(text)
        if unsafe:
            decision = _hardest(decision, GovernanceDecision.REDACT)
            reasons.extend(f"unsafe_claim:{w}" for w in why_list)
            safe_alt = safe_alt or "remove guarantee/100% language; restate as observed outcome"

    # 7. External-send actions (any non-draft channel action) default to
    #    DRAFT_ONLY unless a higher-restriction decision already applies.
    external_send = action.startswith(("send_", "post_", "publish_")) or "_send" in action
    if external_send and channel:
        decision = _hardest(decision, GovernanceDecision.DRAFT_ONLY)
        reasons.append("external_send_default_draft_only")

    # 8. Channel-scoped draft actions (e.g. linkedin_draft, whatsapp_draft,
    #    email_draft) — humans post manually; Dealix prepares only.
    if channel and ("draft" in action.lower() or action.startswith(f"{channel}_draft")):
        decision = _hardest(decision, GovernanceDecision.DRAFT_ONLY)
        reasons.append(f"{channel}_draft_human_posts_manually")

    return DecisionResult(
        decision=decision,
        reasons=tuple(reasons),
        safe_alternative=safe_alt,
    )


__all__ = ["DecisionResult", "GovernanceDecision", "decide"]

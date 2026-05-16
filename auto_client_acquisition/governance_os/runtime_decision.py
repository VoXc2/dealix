"""Maps lightweight policy checks to compliance ``GovernanceDecision`` vocabulary.

Also exposes ``decide()`` — the single runtime governance call used by the
7-Day Revenue Intelligence Sprint (Day 4 governance review). It scans an
action + context and returns a lowercase-coded ``DecideResult``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.governance_os.forbidden_actions import is_channel_forbidden
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


class RuntimeVerdict(StrEnum):
    """Lowercase runtime governance vocabulary (7-decision matrix)."""

    ALLOW = "allow"
    ALLOW_WITH_REVIEW = "allow_with_review"
    DRAFT_ONLY = "draft_only"
    REQUIRE_APPROVAL = "require_approval"
    REDACT = "redact"
    BLOCK = "block"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class DecideResult:
    """Outcome of a single runtime governance decision."""

    decision: RuntimeVerdict
    reasons: tuple[str, ...] = field(default_factory=tuple)


# Misrepresentation markers broader than draft_gate's phrase list — catches the
# guarantee/fake-proof roots in AR + EN regardless of surrounding wording.
_UNSAFE_CLAIM_MARKERS: tuple[str, ...] = (
    "guarantee",
    "guaranteed",
    "نضمن",
    "مضمون",
    "مضمونة",
    "fake proof",
    "fake testimonial",
    "إثبات مزيف",
    "إثبات مزيّف",
)


def decide(*, action: str, context: dict | None = None) -> DecideResult:
    """Runtime governance decision for a proposed action.

    ``context`` may carry ``text`` (draft/answer body), ``channel``, and
    ``is_cold``. Operational forbidden patterns -> BLOCK; misrepresentation
    claims -> REDACT; cold external channels -> DRAFT_ONLY; otherwise ALLOW.
    """
    ctx = context or {}
    text = str(ctx.get("text", ""))
    blob = text.lower()
    reasons: list[str] = []

    raw = audit_draft_text(text)
    operational_hits = [i for i in raw if i.startswith("forbidden_term:")]
    if operational_hits or is_channel_forbidden(text):
        reasons.extend(operational_hits or ["forbidden_channel_language"])
        return DecideResult(RuntimeVerdict.BLOCK, tuple(dict.fromkeys(reasons)))

    claim_hits = [m for m in _UNSAFE_CLAIM_MARKERS if m in blob]
    claim_hits += [i for i in raw if i.startswith("forbidden_claim:")]
    if claim_hits:
        reasons.extend(f"unsafe_claim:{c}" for c in dict.fromkeys(claim_hits))
        return DecideResult(RuntimeVerdict.REDACT, tuple(reasons))

    if bool(ctx.get("is_cold")):
        return DecideResult(RuntimeVerdict.DRAFT_ONLY, ("cold_channel_requires_draft_only",))

    return DecideResult(RuntimeVerdict.ALLOW, ())


__all__ = [
    "DecideResult",
    "GovernanceDecision",
    "RuntimeVerdict",
    "decide",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
]

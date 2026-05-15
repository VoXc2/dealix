"""Unified governance checks for drafts and intake (single call-site for routers)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from auto_client_acquisition.governance_os.draft_gate import (
    audit_draft_text,
    intake_violations_for_source,
)
from auto_client_acquisition.governance_os.forbidden_actions import is_channel_forbidden


class PolicyVerdict(StrEnum):
    """High-level routing outcome for automated gates."""

    ALLOW = "ALLOW"
    ALLOW_WITH_REVIEW = "ALLOW_WITH_REVIEW"
    BLOCK = "BLOCK"


@dataclass(frozen=True, slots=True)
class PolicyCheckResult:
    allowed: bool
    verdict: PolicyVerdict
    issues: tuple[str, ...]


def policy_check_draft(text: str) -> PolicyCheckResult:
    """
    Block draft text that advertises forbidden patterns or channels.

    Human review is still required for client-facing delivery; this is an automated pre-check.
    """
    issues: list[str] = []
    issues.extend(audit_draft_text(text))
    if is_channel_forbidden(text):
        issues.append("forbidden_channel_language")
    if issues:
        return PolicyCheckResult(False, PolicyVerdict.BLOCK, tuple(dict.fromkeys(issues)))
    return PolicyCheckResult(True, PolicyVerdict.ALLOW, ())


def policy_check_intake_source(lead_source: str) -> PolicyCheckResult:
    """Validate Tier1 / anti-waste posture for a declared lead source string."""
    vio = intake_violations_for_source(lead_source)
    if vio:
        return PolicyCheckResult(False, PolicyVerdict.BLOCK, tuple(vio))
    return PolicyCheckResult(True, PolicyVerdict.ALLOW, ())


def run_policy_check(
    *,
    draft_text: str | None = None,
    lead_source: str | None = None,
) -> PolicyCheckResult:
    """
    Run all provided checks; any failure => BLOCK with merged issues.

    Callers may pass one or both kwargs.
    """
    merged: list[str] = []
    verdict = PolicyVerdict.ALLOW
    allowed = True
    if draft_text is not None:
        r = policy_check_draft(draft_text)
        if not r.allowed:
            allowed = False
            verdict = PolicyVerdict.BLOCK
            merged.extend(r.issues)
    if lead_source is not None:
        r = policy_check_intake_source(lead_source)
        if not r.allowed:
            allowed = False
            verdict = PolicyVerdict.BLOCK
            merged.extend(r.issues)
    uniq = tuple(dict.fromkeys(merged))
    return PolicyCheckResult(allowed, verdict if not allowed else PolicyVerdict.ALLOW, uniq)


__all__ = [
    "PolicyCheckResult",
    "PolicyVerdict",
    "policy_check_draft",
    "policy_check_intake_source",
    "run_policy_check",
]

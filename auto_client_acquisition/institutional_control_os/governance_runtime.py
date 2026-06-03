"""Runtime governance checklist — institutional moat at execution time."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class OutputGovernanceDecision(StrEnum):
    """Output routing before customer / market — institutional control layer."""

    ALLOW = "ALLOW"
    ALLOW_WITH_REVIEW = "ALLOW_WITH_REVIEW"
    DRAFT_ONLY = "DRAFT_ONLY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REDACT = "REDACT"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


RUNTIME_CHECKLIST_KEYS: tuple[str, ...] = (
    "source_status_ok",
    "pii_status_known",
    "allowed_use_ok",
    "claim_risk_assessed",
    "channel_risk_assessed",
    "agent_autonomy_known",
    "approval_requirement_known",
    "audit_event_recorded",
)


def governance_runtime_checklist_passes(
    checks: Mapping[str, bool],
) -> tuple[bool, tuple[str, ...]]:
    """All institutional runtime gates must be explicitly true."""
    missing = [k for k in RUNTIME_CHECKLIST_KEYS if not checks.get(k)]
    return not missing, tuple(missing)


@dataclass(frozen=True, slots=True)
class GovernanceRuntimeSignals:
    """Minimal deterministic signals for output governance (expand at routers)."""

    source_passport_valid: bool
    contains_personal_contact_data: bool
    external_action_requested: bool
    human_approved_external: bool
    unsupported_claim: bool = False
    scraping_or_unauthorized_harvest: bool = False
    cold_outreach_automation: bool = False


def evaluate_output_governance(
    signals: GovernanceRuntimeSignals,
    *,
    audit_event_id: str,
) -> dict[str, Any]:
    """Return an institutional governance decision payload (JSON-serializable).

    Priority-ordered rules — first match wins. This is not legal advice;
    it encodes Dealix product safety defaults.
    """
    matched: list[str] = []
    if signals.scraping_or_unauthorized_harvest:
        matched.append("scraping_forbidden")
        return _payload(
            OutputGovernanceDecision.BLOCK,
            "high",
            "Scraping or unauthorized harvesting is blocked by policy.",
            matched,
            audit_event_id,
            "halt_and_notify_owner",
        )
    if signals.cold_outreach_automation:
        matched.append("cold_outreach_automation_forbidden")
        return _payload(
            OutputGovernanceDecision.BLOCK,
            "high",
            "Cold outreach automation is not permitted.",
            matched,
            audit_event_id,
            "halt_and_notify_owner",
        )
    if not signals.source_passport_valid:
        matched.append("no_source_passport_no_ai_use")
        return _payload(
            OutputGovernanceDecision.BLOCK,
            "high",
            "No valid Source Passport — AI use on this path is blocked.",
            matched,
            audit_event_id,
            "issue_source_passport",
        )
    if signals.unsupported_claim:
        matched.append("claim_requires_proof")
        return _payload(
            OutputGovernanceDecision.ESCALATE,
            "medium",
            "Claim is not supported by recorded proof — escalate for review.",
            matched,
            audit_event_id,
            "human_review_and_proof",
        )
    if signals.external_action_requested and not signals.human_approved_external:
        matched.append("external_action_requires_approval")
        if signals.contains_personal_contact_data:
            return _payload(
                OutputGovernanceDecision.DRAFT_ONLY,
                "medium",
                "Personal contact data exists but external action is not approved.",
                matched,
                audit_event_id,
                "human_review",
            )
        return _payload(
            OutputGovernanceDecision.REQUIRE_APPROVAL,
            "medium",
            "External action requires explicit human approval.",
            matched,
            audit_event_id,
            "route_to_approval_center",
        )
    if signals.contains_personal_contact_data:
        matched.append("pii_present_review_recommended")
        return _payload(
            OutputGovernanceDecision.ALLOW_WITH_REVIEW,
            "low",
            "PII-class data present — allow internal path with human review before external use.",
            matched,
            audit_event_id,
            "human_review_if_external",
        )
    return _payload(
        OutputGovernanceDecision.ALLOW,
        "low",
        "No institutional blockers on this path for the declared signals.",
        matched,
        audit_event_id,
        "continue_with_operating_cadence",
    )


def _payload(
    decision: OutputGovernanceDecision,
    risk_level: str,
    reason: str,
    matched_rules: list[str],
    audit_event_id: str,
    next_action: str,
) -> dict[str, Any]:
    return {
        "decision": decision.value,
        "risk_level": risk_level,
        "reason": reason,
        "matched_rules": matched_rules,
        "audit_event_id": audit_event_id,
        "next_action": next_action,
    }

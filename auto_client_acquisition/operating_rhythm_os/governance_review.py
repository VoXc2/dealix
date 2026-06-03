"""Weekly governance review checklist — binary health for rhythm."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GovernanceWeeklyChecklist:
    ai_runs_logged: bool
    outputs_have_governance_status: bool
    pii_flags_reviewed: bool
    unsupported_claims_rejected: bool
    forbidden_automation_requests_handled: bool
    agent_permission_escalations_reviewed: bool
    incidents_triaged: bool


def governance_weekly_failures(check: GovernanceWeeklyChecklist) -> tuple[str, ...]:
    failures: list[str] = []
    if not check.ai_runs_logged:
        failures.append("ai_runs_not_logged")
    if not check.outputs_have_governance_status:
        failures.append("outputs_missing_governance_status")
    if not check.pii_flags_reviewed:
        failures.append("pii_flags_not_reviewed")
    if not check.unsupported_claims_rejected:
        failures.append("unsupported_claims_not_rejected")
    if not check.forbidden_automation_requests_handled:
        failures.append("forbidden_automation_not_handled")
    if not check.agent_permission_escalations_reviewed:
        failures.append("agent_escalations_not_reviewed")
    if not check.incidents_triaged:
        failures.append("incidents_not_triaged")
    return tuple(failures)


def governance_weekly_healthy(check: GovernanceWeeklyChecklist) -> bool:
    return not governance_weekly_failures(check)

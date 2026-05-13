"""Privacy-by-Runtime — typed checks applied to every AI task."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrivacyRuntimeChecks:
    source_passport_present: bool
    pii_detector_ran: bool
    allowed_use_satisfied: bool
    redaction_applied_if_needed: bool
    policy_decision_recorded: bool
    audit_event_emitted: bool
    approval_required_if_external: bool


@dataclass(frozen=True)
class PrivacyRuntimeResult:
    safe: bool
    failed: tuple[str, ...]


def evaluate_privacy_runtime(c: PrivacyRuntimeChecks) -> PrivacyRuntimeResult:
    failed: list[str] = []
    if not c.source_passport_present:
        failed.append("source_passport_missing")
    if not c.pii_detector_ran:
        failed.append("pii_detector_did_not_run")
    if not c.allowed_use_satisfied:
        failed.append("allowed_use_unsatisfied")
    if not c.redaction_applied_if_needed:
        failed.append("redaction_missing")
    if not c.policy_decision_recorded:
        failed.append("policy_decision_missing")
    if not c.audit_event_emitted:
        failed.append("audit_event_missing")
    if not c.approval_required_if_external:
        failed.append("approval_missing_for_external")
    return PrivacyRuntimeResult(safe=not failed, failed=tuple(failed))

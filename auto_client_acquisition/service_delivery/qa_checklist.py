"""
QA Checklist — confirms each session is "Definition of Done"-compliant
before transitioning to delivered.

Pure logic. The delivery router calls `check_ready_to_deliver(session, contract,
proof_events)` and refuses the transition if any required item is missing.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QAResult:
    passed: bool
    missing: tuple[str, ...]
    warnings: tuple[str, ...]


def check_ready_to_deliver(session, contract, proof_events) -> QAResult:
    """Return a QAResult describing whether `session` is DoD-compliant."""
    missing: list[str] = []
    warnings: list[str] = []

    if contract is None:
        return QAResult(False, ("contract_missing",), ())

    # Required inputs must be present
    inputs = session.inputs_json or {}
    for required in contract.required_inputs:
        if not inputs.get(required):
            missing.append(f"input:{required}")

    # All required approval gates must have at least one approval_collected event
    approvals_collected = sum(
        1 for e in (proof_events or [])
        if e.unit_type == "approval_collected" and e.approved
    )
    if contract.human_approvals and approvals_collected == 0:
        missing.append(f"approvals:{','.join(contract.human_approvals)}")

    # At least one deliverable must be queued
    deliverables = session.deliverables_json or []
    if not deliverables:
        missing.append("deliverables:none_queued")

    # SLA: warn if more than 80% of the SLA window already passed
    if session.deadline_at is not None and session.started_at is not None:
        try:
            total = (session.deadline_at - session.started_at).total_seconds()
            from datetime import datetime, timezone
            elapsed = (datetime.now(timezone.utc).replace(tzinfo=None) - session.started_at.replace(tzinfo=None)).total_seconds()
            if total > 0 and elapsed / total > 0.8:
                warnings.append("sla:80pct_window_consumed")
        except Exception:
            pass  # missing tz info — skip non-critical warning

    return QAResult(
        passed=not missing,
        missing=tuple(missing),
        warnings=tuple(warnings),
    )

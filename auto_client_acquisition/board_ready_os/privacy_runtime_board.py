"""Privacy Runtime Board — snapshot of runtime privacy posture."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrivacyRuntimeBoardSnapshot:
    period: str
    pii_detected: int
    redactions_applied: int
    policy_decisions: int
    blocked_disclosures: int
    external_use_attempts: int
    source_passports_missing: int
    approval_required: int
    approval_completed: int

    def open_approvals(self) -> int:
        return max(0, self.approval_required - self.approval_completed)

    def has_open_risks(self) -> bool:
        return (
            self.source_passports_missing > 0
            or self.open_approvals() > 0
            or self.blocked_disclosures > 0
        )

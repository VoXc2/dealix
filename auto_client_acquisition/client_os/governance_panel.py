"""Client Governance Panel — typed snapshot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernancePanel:
    client_id: str
    period: str
    outputs_allowed: int
    outputs_draft_only: int
    outputs_requiring_approval: int
    redactions_applied: int
    blocked_risks: int
    audit_events: int

    def total_outputs(self) -> int:
        return (
            self.outputs_allowed
            + self.outputs_draft_only
            + self.outputs_requiring_approval
        )

    def safety_ratio(self) -> float:
        """Share of outputs that were not auto-allowed."""

        total = self.total_outputs()
        if total == 0:
            return 0.0
        return (self.outputs_draft_only + self.outputs_requiring_approval) / total

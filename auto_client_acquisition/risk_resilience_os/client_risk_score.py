"""Client risk — high-risk intake signals (operating gates, not legal advice)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClientRiskSignals:
    unclear_data_ownership: bool
    governance_rejects_approval: bool
    wants_guaranteed_outcomes: bool
    open_ended_scope: bool
    no_executive_owner: bool
    requests_unsafe_automation: bool


def client_risk_tier(signals: ClientRiskSignals) -> str:
    """Returns coarse tier for routing (diagnostic vs standard vs high)."""
    if (
        signals.requests_unsafe_automation
        or signals.wants_guaranteed_outcomes
        or signals.governance_rejects_approval
    ):
        return "high_reject_or_reframe"
    if signals.unclear_data_ownership or signals.no_executive_owner or signals.open_ended_scope:
        return "paid_diagnostic_or_shrink"
    return "standard"

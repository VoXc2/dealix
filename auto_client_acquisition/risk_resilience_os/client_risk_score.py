"""Client Risk classification — signals → tier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


CLIENT_RISK_DIMENSIONS: tuple[str, ...] = (
    "data_ownership_unclear",
    "rejects_approval",
    "wants_guaranteed_outcome",
    "open_ended_scope",
    "no_workflow_owner",
    "asks_unsafe_automation",
)


class ClientRiskTier(str, Enum):
    HIGH = "high"        # ≥3 signals or any forbidden trigger
    MEDIUM = "medium"    # 1-2 signals
    LOW = "low"          # 0 signals


@dataclass(frozen=True)
class ClientRiskSignals:
    data_ownership_unclear: bool = False
    rejects_approval: bool = False
    wants_guaranteed_outcome: bool = False
    open_ended_scope: bool = False
    no_workflow_owner: bool = False
    asks_unsafe_automation: bool = False


def classify_client_risk(s: ClientRiskSignals) -> ClientRiskTier:
    forbidden = s.asks_unsafe_automation or s.wants_guaranteed_outcome
    count = sum(
        (
            s.data_ownership_unclear,
            s.rejects_approval,
            s.wants_guaranteed_outcome,
            s.open_ended_scope,
            s.no_workflow_owner,
            s.asks_unsafe_automation,
        )
    )
    if forbidden or count >= 3:
        return ClientRiskTier.HIGH
    if count >= 1:
        return ClientRiskTier.MEDIUM
    return ClientRiskTier.LOW

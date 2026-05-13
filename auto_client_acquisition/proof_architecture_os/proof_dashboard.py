"""Proof Dashboard — aggregated proof state."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProofDashboardSnapshot:
    period: str
    proof_packs_delivered: int
    average_proof_score: float
    proof_by_type: dict[str, int]
    proof_to_retainer_conversion: float
    case_candidate_count: int
    weak_proof_count: int
    risk_events_blocked: int
    value_events_recorded: int
    client_confirmed_value: float
    estimated_vs_verified_ratio: float

"""Weekly proof review — combine proof score with adoption for retainer path."""

from __future__ import annotations

from enum import StrEnum


class WeeklyProofDecision(StrEnum):
    CASE_SAFE_SUMMARY_CANDIDATE = "case_safe_summary_candidate"
    RETAINER_RECOMMENDATION = "retainer_recommendation"
    DELIVERY_IMPROVEMENT_REQUIRED = "delivery_improvement_required"
    BENCHMARK_CANDIDATE = "benchmark_candidate"
    CONTINUE_MONITOR = "continue_monitor"


def weekly_proof_decision(
    *,
    proof_score: int,
    adoption_score: int,
    repeated_proof_pattern: bool = False,
) -> WeeklyProofDecision:
    if repeated_proof_pattern and proof_score >= 70:
        return WeeklyProofDecision.BENCHMARK_CANDIDATE
    if proof_score >= 85:
        return WeeklyProofDecision.CASE_SAFE_SUMMARY_CANDIDATE
    if proof_score >= 80 and adoption_score >= 70:
        return WeeklyProofDecision.RETAINER_RECOMMENDATION
    if proof_score < 70:
        return WeeklyProofDecision.DELIVERY_IMPROVEMENT_REQUIRED
    return WeeklyProofDecision.CONTINUE_MONITOR

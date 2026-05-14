"""Data Readiness score bands — gating AI workflows on unclear data."""

from __future__ import annotations


def data_readiness_score_band(score: int) -> str:
    if score >= 85:
        return "ready_for_ai_workflow"
    if score >= 70:
        return "usable_with_cleanup"
    if score >= 50:
        return "diagnostic_only"
    return "data_readiness_sprint_first"

"""Governance control metrics — thresholds before aggressive enterprise scale."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ControlMetricsSnapshot:
    """Percentages are 0–100 unless noted."""

    pct_sources_with_passport: float
    pct_ai_runs_logged: float
    pct_outputs_with_governance_status: float
    client_facing_qa_avg: float
    pct_external_actions_with_approval: float
    proof_pack_completion_rate: float
    capital_assets_per_project_min: float


def enterprise_control_blockers(metrics: ControlMetricsSnapshot) -> tuple[str, ...]:
    """Strict directional gates — missing any blocks institutional scaling narrative."""
    m = metrics
    blockers: list[str] = []
    if m.pct_sources_with_passport < 100.0:
        blockers.append("source_passport_coverage_incomplete")
    if m.pct_ai_runs_logged < 100.0:
        blockers.append("ai_run_logging_incomplete")
    if m.pct_outputs_with_governance_status < 100.0:
        blockers.append("output_governance_coverage_incomplete")
    if m.client_facing_qa_avg < 85.0:
        blockers.append("qa_below_scale_threshold")
    if m.pct_external_actions_with_approval < 100.0:
        blockers.append("external_action_approval_gap")
    if m.proof_pack_completion_rate < 100.0:
        blockers.append("proof_pack_rate_insufficient_for_cases")
    if m.capital_assets_per_project_min < 1.0:
        blockers.append("capital_asset_per_project_required")
    return tuple(blockers)

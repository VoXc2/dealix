"""AI cost accounting — aggregate run costs for an engagement or sprint."""

from __future__ import annotations


def total_ai_run_cost_usd(*per_run_usd: float) -> float:
    return round(sum(per_run_usd), 4)


def ai_cost_per_proof_pack_usd(draft_runs_usd: float, narrative_runs_usd: float, qa_runs_usd: float) -> float:
    return round(draft_runs_usd + narrative_runs_usd + qa_runs_usd, 4)


__all__ = ["ai_cost_per_proof_pack_usd", "total_ai_run_cost_usd"]

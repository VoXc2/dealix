"""ROI aggregator — joins the four OS ledgers into one ROI snapshot.

Reads (all tenant-scoped, all append-only):
  - agent loop ledger   → runs completed, successful runs
  - knowledge ledger    → grounded answers, grounding rate
  - eval ledger         → latest quality pass rate
  - LLM router usage    → verified LLM cost

Doctrine: verified figures carry a non-empty ``evidence_ref``; projected
value is labelled ``estimated``; cost is always shown (``no_hidden_pricing``).
"""
from __future__ import annotations

from auto_client_acquisition.agent_loop_os.agent_loop_ledger import list_loops
from auto_client_acquisition.evals_os.eval_ledger import list_eval_runs
from auto_client_acquisition.knowledge_os.knowledge_ledger import list_knowledge_events
from auto_client_acquisition.roi_os.cost_model import (
    estimated_value_from_activity,
    llm_cost_sar_from_usage,
)
from auto_client_acquisition.roi_os.roi_ledger import emit_roi_snapshot
from auto_client_acquisition.roi_os.schemas import ROILine, ROISnapshot

__all__ = ["compute_roi"]


def compute_roi(customer_id: str, *, window_days: int = 30) -> ROISnapshot:
    """Compute and ledger a ROI snapshot for ``customer_id``."""
    if not customer_id.strip():
        raise ValueError("customer_id is required")

    # ── Agent runtime activity ────────────────────────────────────────
    loops = list_loops(customer_id=customer_id, since_days=window_days, limit=5000)
    agent_runs = len(loops)
    successful_runs = sum(
        1
        for loop in loops
        if loop.get("terminated_reason") == "goal_met"
        and not loop.get("insufficient_evidence", False)
    )

    # ── Knowledge activity ────────────────────────────────────────────
    kevents = list_knowledge_events(
        customer_handle=customer_id, since_days=window_days, limit=10_000
    )
    answered = sum(1 for e in kevents if e.kind == "query_answered")
    empty = sum(1 for e in kevents if e.kind == "retrieval_empty")
    grounding_rate = round(answered / (answered + empty), 4) if (answered + empty) else 0.0

    # ── Quality ───────────────────────────────────────────────────────
    eval_runs = list_eval_runs(customer_id=customer_id, since_days=window_days, limit=1000)
    eval_pass_rate = float(eval_runs[-1].get("pass_rate", 0.0)) if eval_runs else 0.0

    # ── Cost (verified) + value (estimated) ───────────────────────────
    llm_cost = llm_cost_sar_from_usage()
    _hours, estimated_value = estimated_value_from_activity(answered, successful_runs)
    verified_value = 0.0  # No verified revenue events wired yet — honest zero.
    net_roi = round(verified_value + estimated_value - llm_cost, 2)

    lines = (
        ROILine("agent_runs_completed", float(agent_runs), "verified", "ledger:agent_loop"),
        ROILine("grounded_answers", float(answered), "verified", "ledger:knowledge"),
        ROILine("eval_pass_rate", round(eval_pass_rate, 4), "verified", "ledger:eval"),
        ROILine("llm_cost_sar", -round(llm_cost, 2), "verified", "core.llm.router.usage_summary"),
        ROILine(
            "estimated_operational_value_sar",
            estimated_value,
            "estimated",
            "model:roi_os.cost_model",
        ),
    )

    snapshot = ROISnapshot(
        customer_id=customer_id,
        window_days=window_days,
        agent_runs=agent_runs,
        grounded_answers=answered,
        eval_pass_rate=round(eval_pass_rate, 4),
        knowledge_grounding_rate=grounding_rate,
        verified_value_sar=verified_value,
        estimated_value_sar=estimated_value,
        llm_cost_sar=round(llm_cost, 2),
        net_roi_sar=net_roi,
        lines=lines,
    )
    emit_roi_snapshot(snapshot)
    return snapshot

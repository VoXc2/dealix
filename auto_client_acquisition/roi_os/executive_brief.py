"""Executive brief — a board-readable narrative built from a ROISnapshot.

Deterministic Markdown (an LLM-written narrative is the upgrade path).
Every figure is sourced; the Limitations section states plainly that
estimated value is not verified value (``no_unverified_outcomes``).
"""
from __future__ import annotations

from auto_client_acquisition.roi_os.roi_aggregator import compute_roi
from auto_client_acquisition.roi_os.schemas import ExecutiveBrief, ROISnapshot

__all__ = ["build_brief", "render_markdown"]


def render_markdown(snapshot: ROISnapshot) -> str:
    s = snapshot
    lines = [
        f"# Executive Brief — {s.customer_id}",
        "",
        f"_Window: last {s.window_days} days · snapshot `{s.snapshot_id}`_",
        "",
        "## Operating Signals",
        "",
        f"- Agent runs completed: **{s.agent_runs}**",
        f"- Grounded answers delivered: **{s.grounded_answers}**",
        f"- Knowledge grounding rate: **{s.knowledge_grounding_rate * 100:.0f}%**",
        f"- AI quality (eval pass rate): **{s.eval_pass_rate * 100:.0f}%**",
        "",
        "## Value & Cost",
        "",
        f"- Estimated operational value: **{s.estimated_value_sar:,.0f} SAR** _(estimated)_",
        f"- Verified value: **{s.verified_value_sar:,.0f} SAR** _(verified)_",
        f"- LLM cost: **{s.llm_cost_sar:,.2f} SAR** _(verified)_",
        f"- Net ROI: **{s.net_roi_sar:,.0f} SAR**",
        "",
        "## ROI Lines",
        "",
        "| Line | Value (SAR) | Confidence | Evidence |",
        "| --- | ---: | --- | --- |",
    ]
    for line in s.lines:
        lines.append(
            f"| {line.label} | {line.value_sar:,.2f} | {line.confidence} | `{line.evidence_ref}` |"
        )
    lines += [
        "",
        "## Limitations",
        "",
        "- Estimated value is not Verified value — it is a projection from "
        "documented activity assumptions, not a measured business outcome.",
        "- Cost figures are computed from recorded LLM token usage.",
        "- This brief reflects only activity recorded in the Dealix ledgers "
        "for the stated window.",
    ]
    return "\n".join(lines)


def build_brief(customer_id: str, *, window_days: int = 30) -> ExecutiveBrief:
    """Compute a ROI snapshot and render the executive brief."""
    snapshot = compute_roi(customer_id, window_days=window_days)
    headline = (
        f"{snapshot.agent_runs} agent runs · "
        f"{snapshot.grounded_answers} grounded answers · "
        f"net ROI {snapshot.net_roi_sar:,.0f} SAR (window {window_days}d)"
    )
    return ExecutiveBrief(
        customer_id=customer_id,
        window_days=window_days,
        headline=headline,
        markdown=render_markdown(snapshot),
        snapshot=snapshot,
    )

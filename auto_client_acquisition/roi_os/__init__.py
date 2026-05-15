"""ROI OS — executive intelligence + ROI.

Joins the Knowledge, Agent Runtime, and Evals ledgers with verified LLM
cost into one ROI snapshot, and renders a board-readable executive brief.
"""

from auto_client_acquisition.roi_os.cost_model import (
    estimated_value_from_activity,
    llm_cost_sar_from_usage,
)
from auto_client_acquisition.roi_os.executive_brief import build_brief, render_markdown
from auto_client_acquisition.roi_os.roi_aggregator import compute_roi
from auto_client_acquisition.roi_os.roi_ledger import (
    clear_for_test,
    emit_roi_snapshot,
    list_roi_snapshots,
)
from auto_client_acquisition.roi_os.schemas import (
    ExecutiveBrief,
    ROILine,
    ROISnapshot,
    roi_snapshot_valid,
)

__all__ = [
    "ExecutiveBrief",
    "ROILine",
    "ROISnapshot",
    "build_brief",
    "clear_for_test",
    "compute_roi",
    "emit_roi_snapshot",
    "estimated_value_from_activity",
    "list_roi_snapshots",
    "llm_cost_sar_from_usage",
    "render_markdown",
    "roi_snapshot_valid",
]

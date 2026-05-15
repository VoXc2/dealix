"""Board-Ready Execution Architecture — deterministic checks for investor-grade narrative."""

from __future__ import annotations

from auto_client_acquisition.board_ready_os.agent_risk_board import agent_autonomy_board_allowed
from auto_client_acquisition.board_ready_os.board_dashboard import (
    BOARD_DASHBOARD_METRICS,
    board_dashboard_coverage_score,
)
from auto_client_acquisition.board_ready_os.board_memo import (
    BOARD_MEMO_SECTIONS,
    board_memo_sections_complete,
    build_board_memo_markdown_skeleton,
)
from auto_client_acquisition.board_ready_os.due_diligence_pack import (
    DUE_DILIGENCE_ARTIFACTS,
    due_diligence_pack_coverage_score,
)
from auto_client_acquisition.board_ready_os.financial_model import (
    MIN_GROSS_MARGIN_PCT_FOR_SCALE,
    RevenueLine,
    revenue_line_ok_for_scale,
    unit_economics_scale_ok,
)
from auto_client_acquisition.board_ready_os.privacy_runtime_board import (
    PRIVACY_RUNTIME_BOARD_SIGNALS,
    privacy_runtime_board_checklist_passes,
)
from auto_client_acquisition.board_ready_os.risk_register import (
    BoardRiskEntry,
    BoardRiskId,
    board_risk_entry_valid,
)
from auto_client_acquisition.board_ready_os.roadmap import (
    BOARD_ROADMAP_PHASES,
    board_roadmap_milestone_count,
    board_roadmap_phase_name,
)

__all__ = (
    "BOARD_DASHBOARD_METRICS",
    "BOARD_MEMO_SECTIONS",
    "BOARD_ROADMAP_PHASES",
    "DUE_DILIGENCE_ARTIFACTS",
    "MIN_GROSS_MARGIN_PCT_FOR_SCALE",
    "PRIVACY_RUNTIME_BOARD_SIGNALS",
    "BoardRiskEntry",
    "BoardRiskId",
    "RevenueLine",
    "agent_autonomy_board_allowed",
    "board_dashboard_coverage_score",
    "board_memo_sections_complete",
    "board_risk_entry_valid",
    "board_roadmap_milestone_count",
    "board_roadmap_phase_name",
    "build_board_memo_markdown_skeleton",
    "due_diligence_pack_coverage_score",
    "privacy_runtime_board_checklist_passes",
    "revenue_line_ok_for_scale",
    "unit_economics_scale_ok",
)

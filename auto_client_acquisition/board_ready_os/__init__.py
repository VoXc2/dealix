"""Dealix Board-Ready Execution OS.

Companion doc: ``docs/board_ready/BOARD_READY_DOCTRINE.md``. Typed
surfaces: board dashboard (12 metrics), 12-section board memo, due
diligence pack checklist, agent risk board row, privacy runtime board
snapshot, financial model unit economics, pricing power triggers,
and roadmap phases.
"""

from __future__ import annotations

from auto_client_acquisition.board_ready_os.agent_risk_board import (
    AgentRiskBoardRow,
    agent_risk_band,
)
from auto_client_acquisition.board_ready_os.board_dashboard import (
    BOARD_DASHBOARD_METRICS,
    BoardDashboardSnapshot,
)
from auto_client_acquisition.board_ready_os.board_memo import (
    BOARD_MEMO_V12_SECTIONS,
    BoardMemoV12,
    BoardMemoV12Section,
    render_board_memo_v12,
)
from auto_client_acquisition.board_ready_os.due_diligence_pack import (
    DUE_DILIGENCE_SECTIONS,
    DueDiligencePack,
    evaluate_due_diligence_pack,
)
from auto_client_acquisition.board_ready_os.financial_model import (
    OfferUnitEconomics,
    is_offer_healthy,
)
from auto_client_acquisition.board_ready_os.pricing_power import (
    PRICE_INCREASE_TRIGGERS,
    PricingPowerEvidence,
    should_raise_price,
)
from auto_client_acquisition.board_ready_os.privacy_runtime_board import (
    PrivacyRuntimeBoardSnapshot,
)
from auto_client_acquisition.board_ready_os.roadmap import (
    BOARD_READY_PHASES,
    BoardReadyPhase,
    BoardReadyRoadmap,
)

__all__ = [
    "AgentRiskBoardRow",
    "agent_risk_band",
    "BOARD_DASHBOARD_METRICS",
    "BoardDashboardSnapshot",
    "BOARD_MEMO_V12_SECTIONS",
    "BoardMemoV12",
    "BoardMemoV12Section",
    "render_board_memo_v12",
    "DUE_DILIGENCE_SECTIONS",
    "DueDiligencePack",
    "evaluate_due_diligence_pack",
    "OfferUnitEconomics",
    "is_offer_healthy",
    "PRICE_INCREASE_TRIGGERS",
    "PricingPowerEvidence",
    "should_raise_price",
    "PrivacyRuntimeBoardSnapshot",
    "BOARD_READY_PHASES",
    "BoardReadyPhase",
    "BoardReadyRoadmap",
]

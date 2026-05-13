"""Dealix Customer Operating System.

Companion doc: ``docs/client_os/CLIENT_OS_DOCTRINE.md``.
"""

from __future__ import annotations

from auto_client_acquisition.client_os.agent_transparency import (
    AgentTransparencyCard,
)
from auto_client_acquisition.client_os.client_health_score import (
    CLIENT_HEALTH_WEIGHTS,
    ClientHealthComponents,
    ClientHealthTier,
    classify_client_health,
    compute_client_health_score,
)
from auto_client_acquisition.client_os.client_os_stage import (
    CLIENT_OS_STAGES,
    ClientOsStage,
    next_stage_after,
)
from auto_client_acquisition.client_os.expansion_signal import (
    EXPANSION_SIGNALS,
    expansion_offer_for,
)
from auto_client_acquisition.client_os.monthly_value_report import (
    MONTHLY_VALUE_REPORT_SECTIONS,
    MonthlyValueReport,
    render_monthly_value_report,
)

__all__ = [
    "AgentTransparencyCard",
    "CLIENT_HEALTH_WEIGHTS",
    "ClientHealthComponents",
    "ClientHealthTier",
    "classify_client_health",
    "compute_client_health_score",
    "CLIENT_OS_STAGES",
    "ClientOsStage",
    "next_stage_after",
    "EXPANSION_SIGNALS",
    "expansion_offer_for",
    "MONTHLY_VALUE_REPORT_SECTIONS",
    "MonthlyValueReport",
    "render_monthly_value_report",
]

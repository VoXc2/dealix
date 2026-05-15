"""Dealix Customer Operating System — deterministic client-surface contracts."""

from __future__ import annotations

from auto_client_acquisition.client_os.agent_transparency import (
    AgentTransparencyCard,
    agent_transparency_card_valid,
)
from auto_client_acquisition.client_os.capability_dashboard import (
    CAPABILITY_DOMAINS,
    CAPABILITY_LEVEL_MAX,
    capability_level_valid,
)
from auto_client_acquisition.client_os.client_health_score import (
    ClientHealthDimensions,
    client_health_band,
    client_health_score,
)
from auto_client_acquisition.client_os.data_readiness_panel import (
    DATA_READINESS_PANEL_SIGNALS,
    data_readiness_panel_coverage_score,
)
from auto_client_acquisition.client_os.expansion_engine import (
    ClientExpansionSignal,
    client_expansion_recommendation,
)
from auto_client_acquisition.client_os.governance_panel import (
    GOVERNANCE_PANEL_SIGNALS,
    TRUST_OUTPUT_STRIP_SIGNALS,
    governance_panel_coverage_score,
    trust_output_strip_coverage_score,
)
from auto_client_acquisition.client_os.monthly_governance_report import (
    MONTHLY_GOVERNANCE_REPORT_SECTIONS,
    build_empty_monthly_governance_report,
    monthly_governance_report_sections_complete,
)
from auto_client_acquisition.client_os.monthly_value_report import (
    MONTHLY_VALUE_REPORT_SECTIONS,
    build_empty_monthly_value_report,
    monthly_value_report_from_sprint_kpis,
    monthly_value_report_sections_complete,
)
from auto_client_acquisition.client_os.proof_timeline import (
    PROOF_TIMELINE_SIGNALS,
    proof_timeline_coverage_score,
)
from auto_client_acquisition.client_os.workspace import (
    CLIENT_OS_USAGE_SIGNALS,
    client_os_usage_coverage_score,
)

__all__ = (
    "CAPABILITY_DOMAINS",
    "CAPABILITY_LEVEL_MAX",
    "CLIENT_OS_USAGE_SIGNALS",
    "DATA_READINESS_PANEL_SIGNALS",
    "GOVERNANCE_PANEL_SIGNALS",
    "MONTHLY_GOVERNANCE_REPORT_SECTIONS",
    "MONTHLY_VALUE_REPORT_SECTIONS",
    "PROOF_TIMELINE_SIGNALS",
    "TRUST_OUTPUT_STRIP_SIGNALS",
    "AgentTransparencyCard",
    "ClientExpansionSignal",
    "ClientHealthDimensions",
    "agent_transparency_card_valid",
    "build_empty_monthly_governance_report",
    "build_empty_monthly_value_report",
    "capability_level_valid",
    "client_expansion_recommendation",
    "client_health_band",
    "client_health_score",
    "client_os_usage_coverage_score",
    "data_readiness_panel_coverage_score",
    "governance_panel_coverage_score",
    "monthly_governance_report_sections_complete",
    "monthly_value_report_from_sprint_kpis",
    "monthly_value_report_sections_complete",
    "proof_timeline_coverage_score",
    "trust_output_strip_coverage_score",
)

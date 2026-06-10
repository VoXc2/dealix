"""Hermes — Anthropic-native multi-agent system for Saudi B2B revenue intelligence."""

from __future__ import annotations

from dealix.hermes.agents.company_brain import CompanyBrainAgent
from dealix.hermes.agents.customer_acquisition import CustomerAcquisitionAgent
from dealix.hermes.agents.data_architect import DataArchitectAgent
from dealix.hermes.agents.diagnostic_agent import DiagnosticAgent
from dealix.hermes.agents.governance import GovernanceAgent
from dealix.hermes.agents.lead_intelligence import LeadIntelligenceAgent
from dealix.hermes.agents.managed_ops import ManagedOpsAgent
from dealix.hermes.agents.market_intel import MarketIntelAgent
from dealix.hermes.agents.revenue_intelligence import RevenueIntelligenceAgent
from dealix.hermes.agents.sales_intelligence import SalesIntelligenceAgent
from dealix.hermes.agents.sprint_orchestrator import SprintOrchestratorAgent
from dealix.hermes.api.router import HermesResponse, hermes_router
from dealix.hermes.base import HermesAgent
from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.engine import HermesEngine, build_tool_schema
from dealix.hermes.loops.daily_outreach_loop import DailyOutreachLoop
from dealix.hermes.loops.lead_loop import LeadLoop
from dealix.hermes.loops.revenue_loop import RevenueLoop
from dealix.hermes.loops.sprint_loop import SprintLoop
from dealix.hermes.loops.watchdog_loop import WatchdogLoop
from dealix.hermes.memory import HermesMemory, SharedContext
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.outreach_queue import OutreachDraft, OutreachQueue
from dealix.hermes.registry import HermesRegistry

__all__ = [
    "CompanyBrainAgent",
    "CustomerAcquisitionAgent",
    "DailyOutreachLoop",
    "DataArchitectAgent",
    "DiagnosticAgent",
    "GovernanceAgent",
    "HermesAgent",
    "HermesConfig",
    # Core
    "HermesEngine",
    # Memory + Registry
    "HermesMemory",
    # Orchestrator
    "HermesOrchestrator",
    "HermesRegistry",
    "HermesResponse",
    # Agents
    "LeadIntelligenceAgent",
    "LeadLoop",
    "ManagedOpsAgent",
    "MarketIntelAgent",
    "OutreachDraft",
    # Outreach queue
    "OutreachQueue",
    "RevenueIntelligenceAgent",
    # Loops
    "RevenueLoop",
    "SalesIntelligenceAgent",
    "SharedContext",
    "SprintLoop",
    "SprintOrchestratorAgent",
    "WatchdogLoop",
    "build_tool_schema",
    "get_hermes_config",
    # API
    "hermes_router",
]

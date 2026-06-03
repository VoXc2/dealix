"""HermesRegistry — global registry of all HermesAgent instances."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config

if TYPE_CHECKING:
    from dealix.hermes.base import HermesAgent

logger = structlog.get_logger(__name__)


class HermesRegistry:
    """Singleton registry of instantiated HermesAgent objects.

    Usage::

        registry = HermesRegistry.instance()
        registry.register(my_agent)
        agent = registry.get("lead_intelligence")
        names = registry.list_agents()
    """

    _instance: HermesRegistry | None = None

    def __init__(self) -> None:
        self._agents: dict[str, HermesAgent] = {}

    # ------------------------------------------------------------------
    # Singleton access
    # ------------------------------------------------------------------

    @classmethod
    def instance(cls) -> HermesRegistry:
        """Return the global singleton registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, agent: HermesAgent) -> None:
        """Register an agent instance under its ``name``."""
        self._agents[agent.name] = agent
        logger.debug("hermes_agent_registered", name=agent.name)

    def get(self, name: str) -> HermesAgent:
        """Return the agent registered under *name*.

        Raises
        ------
        KeyError
            If no agent with that name has been registered.
        """
        if name not in self._agents:
            raise KeyError(
                f"HermesAgent {name!r} not found. "
                f"Available: {sorted(self._agents.keys())}"
            )
        return self._agents[name]

    def list_agents(self) -> list[str]:
        """Return a sorted list of all registered agent names."""
        return sorted(self._agents.keys())

    def info(self, name: str) -> dict[str, Any]:
        """Return metadata for a registered agent."""
        agent = self.get(name)
        return {
            "name": agent.name,
            "description": agent.description,
            "tools": agent.list_agents() if hasattr(agent, "list_agents") else [],
            "tool_names": list(agent._tools.keys()),
        }

    def all_info(self) -> list[dict[str, Any]]:
        """Return metadata for every registered agent."""
        return [
            {"name": a.name, "description": a.description, "tool_names": list(a._tools.keys())}
            for a in self._agents.values()
        ]

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def build_all_agents(cls, config: HermesConfig | None = None) -> dict[str, HermesAgent]:
        """Instantiate all Hermes agents and return them keyed by name.

        Also registers each agent with the singleton registry.
        """
        cfg = config or get_hermes_config()
        registry = cls.instance()

        # Import lazily to avoid circular imports at module load time
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

        agent_classes = [
            LeadIntelligenceAgent,
            RevenueIntelligenceAgent,
            SprintOrchestratorAgent,
            DiagnosticAgent,
            DataArchitectAgent,
            ManagedOpsAgent,
            SalesIntelligenceAgent,
            MarketIntelAgent,
            CompanyBrainAgent,
            GovernanceAgent,
            CustomerAcquisitionAgent,
        ]

        built: dict[str, HermesAgent] = {}
        for AgentClass in agent_classes:
            agent = AgentClass(config=cfg)
            registry.register(agent)
            built[agent.name] = agent
            logger.info("hermes_agent_built", name=agent.name)

        return built


__all__ = ["HermesRegistry"]

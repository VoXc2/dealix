"""Decide which agents to run for a given WorkforceGoal.

Pure deterministic routing. Always starts with CompanyBrainAgent +
MarketRadarAgent (they produce the context every other agent needs)
and ALWAYS ends with ComplianceGuardAgent (veto power last).
"""
from __future__ import annotations

from auto_client_acquisition.ai_workforce.schemas import WorkforceGoal

# The middle band — everything between the opening (CompanyBrain +
# MarketRadar) and the closing (ComplianceGuard).
_MIDDLE_AGENTS: tuple[str, ...] = (
    "SalesStrategistAgent",
    "SaudiCopyAgent",
    "PartnershipAgent",
    "DeliveryAgent",
    "ProofAgent",
    "ExecutiveBriefAgent",
    "FinanceAgent",
    "CustomerSuccessAgent",
)


def route_for_goal(goal: WorkforceGoal) -> list[str]:
    """Return the ordered list of agent_ids to run for this goal.

    Hard invariants:
      - First entry is always ``CompanyBrainAgent``.
      - Second entry is always ``MarketRadarAgent``.
      - Last entry is always ``ComplianceGuardAgent``.
      - The OrchestratorAgent is implicit — it IS the orchestrator.
    """
    plan: list[str] = ["CompanyBrainAgent", "MarketRadarAgent"]
    plan.extend(_MIDDLE_AGENTS)
    plan.append("ComplianceGuardAgent")
    return plan

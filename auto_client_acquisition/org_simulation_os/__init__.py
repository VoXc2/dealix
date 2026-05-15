"""System 32 — Organizational Simulation Engine.

Simulate workflows, failures, approval load, scale and incidents pre-deployment.
"""

from auto_client_acquisition.org_simulation_os.core import (
    OrgSimulator,
    SimulationError,
    get_org_simulator,
    reset_org_simulator,
)
from auto_client_acquisition.org_simulation_os.schemas import (
    ScenarioKind,
    SimulationResult,
    SimulationScenario,
)

__all__ = [
    "OrgSimulator",
    "ScenarioKind",
    "SimulationError",
    "SimulationResult",
    "SimulationScenario",
    "get_org_simulator",
    "reset_org_simulator",
]

"""Company OS — Dealix as an AI Company Operating System.

The machine-readable spine that names the 7 internal systems Dealix runs
on, scores their maturity, gates the 4-phase roadmap, and maps the 11
non-negotiables to the systems that enforce them.
"""

from __future__ import annotations

from auto_client_acquisition.company_os.doctrine_map import (
    NON_NEGOTIABLES,
    doctrine_coverage,
    gates_for_system,
    systems_for_gate,
)
from auto_client_acquisition.company_os.maturity import (
    band_from_score,
    maturity_report,
    score_system,
)
from auto_client_acquisition.company_os.roadmap import (
    get_phase_gate,
    is_phase_active,
    phase_gates,
    roadmap_digest,
)
from auto_client_acquisition.company_os.schemas import (
    MaturityBand,
    PhaseGate,
    RoadmapPhase,
    SystemEntry,
)
from auto_client_acquisition.company_os.system_registry import (
    SYSTEM_IDS,
    get_system,
    list_systems,
    registry_digest,
    systems_for_phase,
)

__all__ = [
    "NON_NEGOTIABLES",
    "SYSTEM_IDS",
    "MaturityBand",
    "PhaseGate",
    "RoadmapPhase",
    "SystemEntry",
    "band_from_score",
    "doctrine_coverage",
    "gates_for_system",
    "get_phase_gate",
    "get_system",
    "is_phase_active",
    "list_systems",
    "maturity_report",
    "phase_gates",
    "registry_digest",
    "roadmap_digest",
    "score_system",
    "systems_for_gate",
    "systems_for_phase",
]

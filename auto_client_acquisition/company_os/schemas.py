"""Schemas for the Company OS — the machine-readable spine of Dealix.

Company OS names the 7 internal systems Dealix runs on, scores their
maturity, and gates the 4-phase roadmap. Everything here is a frozen
dataclass: deterministic, no I/O, no tenant data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class MaturityBand(StrEnum):
    """How proven a system is, lowest to highest."""

    SEED = "seed"
    WORKING = "working"
    PROVEN = "proven"
    SCALED = "scaled"


class RoadmapPhase(StrEnum):
    """The 4 phases of the AI Company Operating System roadmap."""

    FOUNDATION = "phase_1_foundation"
    DELIVERY_MATURITY = "phase_2_delivery_maturity"
    AGENTIC_PLATFORM = "phase_3_agentic_platform"
    ENTERPRISE_READINESS = "phase_4_enterprise_readiness"


@dataclass(frozen=True, slots=True)
class SystemEntry:
    """One of the 7 internal systems Dealix operates as a company."""

    system_id: str
    name_en: str
    name_ar: str
    backing_modules: tuple[str, ...]
    maturity_band: MaturityBand
    doctrine_gates: tuple[str, ...]
    constitution_articles: tuple[str, ...]
    roadmap_phase: RoadmapPhase
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "system_id": self.system_id,
            "name_en": self.name_en,
            "name_ar": self.name_ar,
            "backing_modules": list(self.backing_modules),
            "maturity_band": str(self.maturity_band),
            "doctrine_gates": list(self.doctrine_gates),
            "constitution_articles": list(self.constitution_articles),
            "roadmap_phase": str(self.roadmap_phase),
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class PhaseGate:
    """Entry/exit criteria for one roadmap phase.

    ``deferred_gated`` is True for phases that the Operating Constitution
    forbids activating before commercial proof (Article 13). Such phases
    are scaffolded, never activated, until ``activation_condition`` holds.
    """

    phase: RoadmapPhase
    name_en: str
    name_ar: str
    entry_criteria: tuple[str, ...]
    exit_criteria: tuple[str, ...]
    deferred_gated: bool
    activation_condition: str

    def to_dict(self) -> dict[str, object]:
        return {
            "phase": str(self.phase),
            "name_en": self.name_en,
            "name_ar": self.name_ar,
            "entry_criteria": list(self.entry_criteria),
            "exit_criteria": list(self.exit_criteria),
            "deferred_gated": self.deferred_gated,
            "activation_condition": self.activation_condition,
        }

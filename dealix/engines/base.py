"""
Engine-layer base contracts — the Agentic Enterprise Platform.

Dealix's 12-engine model. Every engine is a *governed facade* over existing
Dealix capabilities — it composes, it does not reimplement. This module
defines the shared spec, status vocabulary, and base class so all 12 engines
are discoverable, governed, and honest about their build status.

See docs/agentic_operations/AGENTIC_ENTERPRISE_PLATFORM.md.
"""

from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class EngineStatus(StrEnum):
    """Build status — mirrors the no-overclaim register vocabulary."""

    PLANNED = "planned"
    PILOT = "pilot"
    PARTIAL = "partial"
    PRODUCTION = "production"


@dataclass(frozen=True)
class EngineSpec:
    """Immutable description of one engine in the 12-engine platform."""

    engine_id: str
    number: int
    name_en: str
    name_ar: str
    responsibility: str
    capabilities: tuple[str, ...]
    status: EngineStatus
    wraps: tuple[str, ...]  # importable module paths this engine composes
    governance_hooks: tuple[str, ...]  # Governance Engine capabilities it routes through
    roadmap_phase: int

    def __post_init__(self) -> None:
        # no_unbounded_agents — every engine must be reachable by governance.
        if not self.governance_hooks:
            raise ValueError(
                f"Engine '{self.engine_id}' must declare at least one governance hook "
                "(no_unbounded_agents doctrine)"
            )
        if not 1 <= self.number <= 12:
            raise ValueError(f"Engine '{self.engine_id}' number must be 1..12, got {self.number}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "number": self.number,
            "name_en": self.name_en,
            "name_ar": self.name_ar,
            "responsibility": self.responsibility,
            "capabilities": list(self.capabilities),
            "status": self.status.value,
            "wraps": list(self.wraps),
            "governance_hooks": list(self.governance_hooks),
            "roadmap_phase": self.roadmap_phase,
        }


class PlannedCapabilityError(NotImplementedError):
    """Raised when a registered capability is not yet built.

    Fails loudly rather than returning a fabricated result — honors the
    `no_silent_failures` doctrine non-negotiable.
    """

    def __init__(self, engine_id: str, capability: str, phase: int) -> None:
        super().__init__(
            f"{engine_id}.{capability} is Planned — scheduled for roadmap phase {phase}. "
            "It is registered and discoverable but not yet implemented."
        )
        self.engine_id = engine_id
        self.capability = capability
        self.phase = phase


class BaseEngine(ABC):
    """Base class for all 12 engines.

    Subclasses bind a class-level `spec` and implement `_domain_report()`.
    `status_report()` is concrete and additionally verifies that every module
    in `spec.wraps` imports — that check is the engine's real, working
    integration with the rest of the codebase.
    """

    spec: EngineSpec

    @abstractmethod
    def _domain_report(self) -> dict[str, Any]:
        """Engine-specific facts (capability build state, wired surfaces)."""
        ...

    def status_report(self) -> dict[str, Any]:
        """Discoverability + foundation-health snapshot for this engine."""
        return {
            "engine": self.spec.to_dict(),
            "wraps_available": self._check_wraps(),
            "domain": self._domain_report(),
        }

    def _check_wraps(self) -> dict[str, bool]:
        """Verify each wrapped module imports. Honest: a failure is reported,
        not swallowed."""
        result: dict[str, bool] = {}
        for module_path in self.spec.wraps:
            try:
                importlib.import_module(module_path)
                result[module_path] = True
            except Exception:
                result[module_path] = False
        return result

    def _planned(self, capability: str) -> PlannedCapabilityError:
        """Build a PlannedCapabilityError for an unbuilt capability."""
        return PlannedCapabilityError(self.spec.engine_id, capability, self.spec.roadmap_phase)

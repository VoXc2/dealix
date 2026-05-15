"""The 7 internal systems Dealix runs on as an AI Company Operating System.

Truth registry. Each entry maps a named system to the canonical modules
that back it, the doctrine gates it must honor, and the roadmap phase it
belongs to. Pure data — no I/O.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_os.schemas import (
    MaturityBand,
    RoadmapPhase,
    SystemEntry,
)

_SYSTEMS: tuple[SystemEntry, ...] = (
    SystemEntry(
        system_id="delivery_system",
        name_en="Delivery System",
        name_ar="نظام التسليم",
        backing_modules=(
            "auto_client_acquisition.delivery_factory",
            "auto_client_acquisition.diagnostic_workflow",
            "auto_client_acquisition.service_catalog",
            "auto_client_acquisition.workflow_os_v10",
        ),
        maturity_band=MaturityBand.PROVEN,
        doctrine_gates=("no_silent_failures", "no_unverified_outcomes"),
        constitution_articles=("Article 2", "Article 12"),
        roadmap_phase=RoadmapPhase.FOUNDATION,
        evidence_refs=("docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md",),
    ),
    SystemEntry(
        system_id="agent_factory",
        name_en="Agent Factory",
        name_ar="مصنع الوكلاء",
        backing_modules=(
            "auto_client_acquisition.agent_factory",
            "auto_client_acquisition.ai_workforce",
            "auto_client_acquisition.ai_workforce_v10",
        ),
        maturity_band=MaturityBand.WORKING,
        doctrine_gates=("no_unbounded_agents", "no_silent_failures"),
        constitution_articles=("Article 4", "Article 5"),
        roadmap_phase=RoadmapPhase.AGENTIC_PLATFORM,
        evidence_refs=("auto_client_acquisition/ai_workforce/agent_registry.py",),
    ),
    SystemEntry(
        system_id="governance_system",
        name_en="Governance System",
        name_ar="نظام الحوكمة",
        backing_modules=(
            "auto_client_acquisition.governance_os",
            "auto_client_acquisition.trust_os",
            "auto_client_acquisition.responsible_ai_os",
        ),
        maturity_band=MaturityBand.PROVEN,
        doctrine_gates=(
            "no_unaudited_changes",
            "no_unconsented_data",
            "no_unbounded_agents",
            "no_fake_proof",
        ),
        constitution_articles=("Article 4", "Article 5"),
        roadmap_phase=RoadmapPhase.FOUNDATION,
        evidence_refs=("docs/DEALIX_OPERATING_CONSTITUTION.md",),
    ),
    SystemEntry(
        system_id="knowledge_os",
        name_en="Knowledge Operating System",
        name_ar="نظام المعرفة",
        backing_modules=(
            "auto_client_acquisition.knowledge_os",
            "auto_client_acquisition.knowledge_v10",
            "core.memory.revenue_memory",
        ),
        maturity_band=MaturityBand.WORKING,
        doctrine_gates=("no_unconsented_data", "no_fake_proof"),
        constitution_articles=("Article 2",),
        roadmap_phase=RoadmapPhase.FOUNDATION,
        evidence_refs=("auto_client_acquisition/knowledge_os/answer_with_citations.py",),
    ),
    SystemEntry(
        system_id="executive_system",
        name_en="Executive System",
        name_ar="النظام التنفيذي",
        backing_modules=(
            "auto_client_acquisition.executive_command_center",
            "auto_client_acquisition.founder_v10",
            "auto_client_acquisition.executive_reporting",
        ),
        maturity_band=MaturityBand.PROVEN,
        doctrine_gates=("no_hidden_pricing", "no_unverified_outcomes"),
        constitution_articles=("Article 2",),
        roadmap_phase=RoadmapPhase.FOUNDATION,
        evidence_refs=("api/routers/executive_command_center.py",),
    ),
    SystemEntry(
        system_id="evaluation_system",
        name_en="Evaluation System",
        name_ar="نظام التقييم",
        backing_modules=(
            "auto_client_acquisition.eval_os",
            "auto_client_acquisition.agent_observability",
        ),
        maturity_band=MaturityBand.WORKING,
        doctrine_gates=("no_unverified_outcomes", "no_fake_proof"),
        constitution_articles=("Article 11",),
        roadmap_phase=RoadmapPhase.FOUNDATION,
        evidence_refs=("evals/README.md",),
    ),
    SystemEntry(
        system_id="transformation_system",
        name_en="Transformation System",
        name_ar="نظام التحوّل",
        backing_modules=(
            "auto_client_acquisition.transformation_os",
            "auto_client_acquisition.service_catalog",
        ),
        maturity_band=MaturityBand.SEED,
        doctrine_gates=("no_unverified_outcomes", "no_hidden_pricing"),
        constitution_articles=("Article 2", "Article 13"),
        roadmap_phase=RoadmapPhase.DELIVERY_MATURITY,
        evidence_refs=("docs/OFFER_LADDER_AND_PRICING.md",),
    ),
)


SYSTEM_IDS: frozenset[str] = frozenset(s.system_id for s in _SYSTEMS)


def list_systems() -> list[SystemEntry]:
    """The 7 internal systems in canonical declaration order."""
    return list(_SYSTEMS)


def get_system(system_id: str) -> SystemEntry:
    """Return one system by id. Raises KeyError if unknown."""
    for s in _SYSTEMS:
        if s.system_id == system_id:
            return s
    raise KeyError(f"unknown system_id: {system_id}")


def systems_for_phase(phase: RoadmapPhase) -> list[SystemEntry]:
    """All systems whose home roadmap phase is ``phase``."""
    return [s for s in _SYSTEMS if s.roadmap_phase == phase]


def registry_digest() -> dict[str, Any]:
    """Machine-readable snapshot of the whole 7-system spine."""
    return {
        "system_count": len(_SYSTEMS),
        "systems": [s.to_dict() for s in _SYSTEMS],
    }

"""12-System Coverage Registry — a code-derived map of the agentic enterprise.

سجل تغطية الأنظمة الـ12 — يحسب حالة كل نظام (EXISTS/PARTIAL/MISSING) من الكود.

The 12 core systems of the agentic-enterprise vision each map to existing
backing modules. Coverage is resolved with ``importlib.util.find_spec`` ONLY,
which locates a module spec WITHOUT executing the module body — so this
registry triggers no router registration, DB connections, or global mutation.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from typing import Literal

CoverageStatus = Literal["EXISTS", "PARTIAL", "MISSING"]

_BASE = "auto_client_acquisition"


@dataclass(frozen=True, slots=True)
class CoreSystemSpec:
    """One core system and the backing module paths that implement it."""

    key: str
    name_en: str
    name_ar: str
    module_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SystemCoverage:
    """Resolved coverage verdict for one core system."""

    key: str
    name_en: str
    name_ar: str
    status: CoverageStatus
    present_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]


CORE_SYSTEMS: tuple[CoreSystemSpec, ...] = (
    CoreSystemSpec(
        "agent_operating_system",
        "Agent Operating System",
        "نظام تشغيل الوكلاء",
        (
            f"{_BASE}.agent_os.agent_registry",
            f"{_BASE}.agent_os.agent_card",
            f"{_BASE}.agentic_operations_os.agent_governance",
        ),
    ),
    CoreSystemSpec(
        "workflow_orchestration",
        "Workflow Orchestration System",
        "نظام تنسيق سير العمل",
        (
            f"{_BASE}.workflow_os.workflow_model",
            f"{_BASE}.workflow_os.workflow_mapper",
            f"{_BASE}.workflow_os.approval_flow",
        ),
    ),
    CoreSystemSpec(
        "organizational_memory",
        "Organizational Memory System",
        "نظام الذاكرة المؤسسية",
        (
            f"{_BASE}.revenue_memory.event_store",
            f"{_BASE}.revenue_memory.projections",
            f"{_BASE}.intelligence_os.strategic_memory",
        ),
    ),
    CoreSystemSpec(
        "governance_operating_system",
        "Governance Operating System",
        "نظام تشغيل الحوكمة",
        (
            f"{_BASE}.governance_os",
            f"{_BASE}.governance_os.policy_check",
            f"{_BASE}.compliance_trust_os.approval_engine",
        ),
    ),
    CoreSystemSpec(
        "executive_intelligence",
        "Executive Intelligence System",
        "نظام الذكاء التنفيذي",
        (
            f"{_BASE}.intelligence_os.decision_engine",
            f"{_BASE}.intelligence_os.metrics_engine",
            f"{_BASE}.founder_command_summary",
        ),
    ),
    CoreSystemSpec(
        "organizational_graph",
        "Organizational Graph System",
        "نظام الرسم البياني المؤسسي",
        (
            f"{_BASE}.unified_operating_graph.builder",
            f"{_BASE}.unified_operating_graph.schemas",
        ),
    ),
    CoreSystemSpec(
        "execution_system",
        "Execution System",
        "نظام التنفيذ",
        (
            f"{_BASE}.execution_os.event_to_decision",
            f"{_BASE}.execution_os.gates",
        ),
    ),
    CoreSystemSpec(
        "evaluation_system",
        "Evaluation System",
        "نظام التقييم",
        (
            f"{_BASE}.benchmark_os.benchmark_engine",
            f"{_BASE}.benchmark_os.methodology",
            f"{_BASE}.agentic_enterprise_os.evaluation_harness",
        ),
    ),
    CoreSystemSpec(
        "observability_system",
        "Observability System",
        "نظام المراقبة",
        (
            f"{_BASE}.observability_v10.trace_schema",
            f"{_BASE}.observability_v10.buffer",
        ),
    ),
    CoreSystemSpec(
        "transformation_system",
        "Transformation System",
        "نظام التحوّل المؤسسي",
        (
            f"{_BASE}.client_maturity_os.maturity_engine",
            f"{_BASE}.intelligence_os.transformation_gap",
        ),
    ),
    CoreSystemSpec(
        "digital_workforce",
        "Digital Workforce System",
        "نظام القوى العاملة الرقمية",
        (
            f"{_BASE}.ai_workforce.agent_registry",
            f"{_BASE}.ai_workforce.orchestrator",
            f"{_BASE}.ai_workforce.workforce_policy",
        ),
    ),
    CoreSystemSpec(
        "continuous_evolution",
        "Continuous Evolution System",
        "نظام التطوّر المستمر",
        (
            f"{_BASE}.learning_flywheel.aggregator",
            f"{_BASE}.agentic_enterprise_os.evolution_loop",
        ),
    ),
)


def _path_present(path: str) -> bool:
    """True when a module spec can be resolved without executing the module."""
    try:
        return importlib.util.find_spec(path) is not None
    except (ModuleNotFoundError, ValueError, ImportError):
        return False


def module_coverage(spec: CoreSystemSpec) -> SystemCoverage:
    """Resolve EXISTS/PARTIAL/MISSING coverage for one core system."""
    present = tuple(p for p in spec.module_paths if _path_present(p))
    missing = tuple(p for p in spec.module_paths if p not in present)
    if not present:
        status: CoverageStatus = "MISSING"
    elif missing:
        status = "PARTIAL"
    else:
        status = "EXISTS"
    return SystemCoverage(
        key=spec.key,
        name_en=spec.name_en,
        name_ar=spec.name_ar,
        status=status,
        present_paths=present,
        missing_paths=missing,
    )


def coverage_registry() -> tuple[SystemCoverage, ...]:
    """Coverage verdict for all 12 core systems."""
    return tuple(module_coverage(spec) for spec in CORE_SYSTEMS)


def coverage_summary() -> dict:
    """Aggregate counts and a coverage percentage across the 12 systems."""
    coverage = coverage_registry()
    counts = {"EXISTS": 0, "PARTIAL": 0, "MISSING": 0}
    for entry in coverage:
        counts[entry.status] += 1
    total = len(coverage)
    pct = (counts["EXISTS"] + 0.5 * counts["PARTIAL"]) / total * 100 if total else 0.0
    return {
        "systems_total": total,
        "exists": counts["EXISTS"],
        "partial": counts["PARTIAL"],
        "missing": counts["MISSING"],
        "coverage_pct": round(pct, 1),
    }


__all__ = [
    "CORE_SYSTEMS",
    "CoreSystemSpec",
    "CoverageStatus",
    "SystemCoverage",
    "coverage_registry",
    "coverage_summary",
    "module_coverage",
]

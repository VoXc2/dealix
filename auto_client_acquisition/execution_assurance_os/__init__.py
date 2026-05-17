"""Dealix Execution Assurance System.

A declarative, evidence-attested governance layer over every operational
machine. Nothing is "done" because it ran once — a machine is done when
it sells, serves, obeys governance, records evidence, and surfaces its
own failures before a customer does.

Format: Strategy -> System -> Scorecard -> Tests -> Audit -> Weekly CEO
Review -> Improvement Loop.

The registry (dealix/registers/machine_registry.yaml) is the source of
truth. This package reads it; it never invents green status.
"""
from auto_client_acquisition.execution_assurance_os.ceo_review import (
    WEEKLY_DECISIONS,
    CeoReviewReport,
    QualityAuditReport,
    generate_monthly_quality_audit,
    generate_weekly_ceo_review,
    render_audit_markdown,
    render_ceo_review_markdown,
)
from auto_client_acquisition.execution_assurance_os.definition_of_done import (
    DodResult,
    GateResult,
    evaluate_acceptance_gate,
    evaluate_dod,
)
from auto_client_acquisition.execution_assurance_os.health_dashboard import (
    CRITICAL_KPI,
    FULL_OPS_HEALTH_KPIS,
    FullOpsHealth,
    build_full_ops_health,
)
from auto_client_acquisition.execution_assurance_os.registry import (
    CANONICAL_EVIDENCE_EVENTS,
    EXPECTED_MACHINE_IDS,
    DodItem,
    Kpi,
    MachineRegistry,
    MachineSpec,
    load_machine_registry,
    validate_registry,
)
from auto_client_acquisition.execution_assurance_os.scorecard import (
    MATURITY_LEVELS,
    MachineScore,
    PortfolioScore,
    aggregate_score,
    readiness_label,
    score_machine,
)

__all__ = [
    "CANONICAL_EVIDENCE_EVENTS",
    "CRITICAL_KPI",
    "EXPECTED_MACHINE_IDS",
    "FULL_OPS_HEALTH_KPIS",
    "MATURITY_LEVELS",
    "WEEKLY_DECISIONS",
    "CeoReviewReport",
    "DodItem",
    "DodResult",
    "FullOpsHealth",
    "GateResult",
    "Kpi",
    "MachineRegistry",
    "MachineScore",
    "MachineSpec",
    "PortfolioScore",
    "QualityAuditReport",
    "aggregate_score",
    "build_full_ops_health",
    "evaluate_acceptance_gate",
    "evaluate_dod",
    "generate_monthly_quality_audit",
    "generate_weekly_ceo_review",
    "load_machine_registry",
    "readiness_label",
    "render_audit_markdown",
    "render_ceo_review_markdown",
    "score_machine",
    "validate_registry",
]

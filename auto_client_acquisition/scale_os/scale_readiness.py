"""Scale Dominance readiness — introspects the repo to score the 10 scale systems.

Operational scale (agent/workflow sprawl, memory, resilience, observability,
runtime governance, org intelligence, self-evolving workflows, executive OS,
self-evolving core) is distinct from the business scale ladder in
``scale_gates.py``. This module proves — by filesystem introspection only, no
network or DB — whether each scale system is implemented, and evaluates the
10-point "Final Scale Test". It is the machine half of
``docs/scale/SCALE_READINESS.md`` and Gate 9 in ``DEALIX_READINESS.md``.

The scale-system → package map is kept consistent with the layer index in
``auto_client_acquisition/dealix_master_layers/registry.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SystemStatus = str  # "pass" | "partial" | "fail"
Verdict = str  # "PASS" | "PARTIAL" | "BLOCKED"


@dataclass(frozen=True, slots=True)
class ScaleSystem:
    """One operational scale system and the artifacts that prove it is real."""

    system_id: int
    name: str
    name_ar: str
    primary_packages: tuple[str, ...]
    router: str | None
    capability_probes: tuple[str, ...]
    test_probes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FinalScaleCheck:
    """One item of the 10-point Final Scale Test, bound to a capability file."""

    item_id: int
    name: str
    name_ar: str
    probe: str


@dataclass(frozen=True, slots=True)
class ScaleSystemResult:
    """Evaluation outcome for a single scale system."""

    system_id: int
    name: str
    name_ar: str
    status: SystemStatus
    missing_packages: tuple[str, ...]
    missing_probes: tuple[str, ...]
    missing_router: bool
    missing_tests: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ScaleReadinessReport:
    """Aggregate scale-readiness report with a single verdict."""

    systems: tuple[ScaleSystemResult, ...]
    final_scale: tuple[tuple[FinalScaleCheck, bool], ...]
    systems_passed: int
    systems_partial: int
    systems_failed: int
    final_scale_score: int
    verdict: Verdict


# The 10 scale systems. Packages/probes are repo-relative paths verified to
# exist where the capability is implemented; a probe that points at a missing
# file is a genuine gap (it pulls the system down to "partial").
SCALE_SYSTEMS: tuple[ScaleSystem, ...] = (
    ScaleSystem(
        system_id=1,
        name="Agent Sprawl Control",
        name_ar="ضبط تكاثر الوكلاء",
        primary_packages=(
            "auto_client_acquisition/agent_governance",
            "auto_client_acquisition/agent_os",
            "auto_client_acquisition/agent_identity_access_os",
            "auto_client_acquisition/secure_agent_runtime_os",
            "auto_client_acquisition/agentic_operations_os",
        ),
        router="api/routers/agent_governance.py",
        capability_probes=(
            "auto_client_acquisition/agent_governance/agent_registry.py",
            "auto_client_acquisition/agent_os/agent_lifecycle.py",
            "auto_client_acquisition/secure_agent_runtime_os/kill_switch.py",
            "auto_client_acquisition/agent_observability/trace.py",
            "auto_client_acquisition/agent_identity_access_os/permission_review.py",
        ),
        test_probes=(
            "tests/test_agent_os.py",
            "tests/test_secure_agent_runtime.py",
        ),
    ),
    ScaleSystem(
        system_id=2,
        name="Workflow Sprawl Control",
        name_ar="ضبط تكاثر التدفقات",
        primary_packages=(
            "auto_client_acquisition/workflow_os",
            "auto_client_acquisition/workflow_os_v10",
        ),
        router="api/routers/workflow_os_v10.py",
        capability_probes=(
            "auto_client_acquisition/workflow_os_v10/state_machine.py",
            "auto_client_acquisition/workflow_os_v10/retry_policy.py",
            "auto_client_acquisition/workflow_os_v10/checkpoint.py",
            "auto_client_acquisition/workflow_os/workflow_metrics.py",
            # Gap: no versioned per-workflow registry with owner/SLA.
            "auto_client_acquisition/workflow_os_v10/workflow_registry.py",
        ),
        test_probes=("tests/test_workflow_os_v10.py",),
    ),
    ScaleSystem(
        system_id=3,
        name="Memory Governance Fabric",
        name_ar="نسيج حوكمة الذاكرة",
        primary_packages=(
            "auto_client_acquisition/revenue_memory",
            "auto_client_acquisition/knowledge_os",
            "auto_client_acquisition/knowledge_v10",
        ),
        router=None,
        capability_probes=(
            "auto_client_acquisition/revenue_memory/isolated_pg_event_store.py",
            "auto_client_acquisition/revenue_memory/retention.py",
            "auto_client_acquisition/revenue_memory/audit.py",
            "auto_client_acquisition/knowledge_v10/source_policy.py",
            "auto_client_acquisition/knowledge_v10/retrieval_contract.py",
            # Gap: no freshness scoring / permission-scoped retrieval.
            "auto_client_acquisition/revenue_memory/freshness.py",
        ),
        test_probes=("tests/test_personal_operator_memory.py",),
    ),
    ScaleSystem(
        system_id=4,
        name="Operational Resilience Engine",
        name_ar="محرك الصمود التشغيلي",
        primary_packages=(
            "auto_client_acquisition/reliability_os",
            "auto_client_acquisition/risk_resilience_os",
        ),
        router="api/routers/reliability_os.py",
        capability_probes=(
            "dealix/reliability/retry.py",
            "dealix/reliability/dlq.py",
            "dealix/reliability/idempotency.py",
            "auto_client_acquisition/risk_resilience_os/incident_response.py",
            "auto_client_acquisition/risk_resilience_os/resilience_playbooks.py",
            # Gap: no circuit breaker.
            "dealix/reliability/circuit_breaker.py",
        ),
        test_probes=("tests/test_backend_reliability_hardening.py",),
    ),
    ScaleSystem(
        system_id=5,
        name="Enterprise Observability Mesh",
        name_ar="شبكة الرصد المؤسسية",
        primary_packages=(
            "auto_client_acquisition/observability_v6",
            "auto_client_acquisition/observability_v10",
            "auto_client_acquisition/observability_adapters",
        ),
        router="api/routers/observability_v10.py",
        capability_probes=(
            "auto_client_acquisition/observability_v10/trace_schema.py",
            "auto_client_acquisition/observability_v6/incident.py",
            "auto_client_acquisition/observability_v6/correlation.py",
            "auto_client_acquisition/observability_adapters/otel_adapter.py",
            "dealix/observability/cost_tracker.py",
            # Gap: no centralized alert routing.
            "auto_client_acquisition/observability_v10/alerts.py",
        ),
        test_probes=(
            "tests/test_observability_v10.py",
            "tests/test_observability_v6.py",
        ),
    ),
    ScaleSystem(
        system_id=6,
        name="Governance Runtime Fabric",
        name_ar="نسيج الحوكمة وقت التشغيل",
        primary_packages=(
            "auto_client_acquisition/governance_os",
            "auto_client_acquisition/approval_center",
            "auto_client_acquisition/auditability_os",
        ),
        router="api/routers/approval_center.py",
        capability_probes=(
            "auto_client_acquisition/governance_os/runtime_decision.py",
            "auto_client_acquisition/governance_os/policy_check.py",
            "auto_client_acquisition/approval_center/approval_store.py",
            "auto_client_acquisition/auditability_os/evidence_chain.py",
            "auto_client_acquisition/auditability_os/responsibility_attribution.py",
        ),
        test_probes=(
            "tests/test_governance_runtime_decision.py",
            "tests/test_approval_center.py",
        ),
    ),
    ScaleSystem(
        system_id=7,
        name="Organizational Intelligence Engine",
        name_ar="محرك الذكاء التنظيمي",
        primary_packages=(
            "auto_client_acquisition/intelligence_os",
            "auto_client_acquisition/bottleneck_radar",
        ),
        router="api/routers/bottleneck_radar.py",
        capability_probes=(
            "auto_client_acquisition/bottleneck_radar/computer.py",
            "auto_client_acquisition/intelligence_os/metrics_engine.py",
            "auto_client_acquisition/intelligence_os/transformation_gap.py",
            "auto_client_acquisition/intelligence_os/decision_engine.py",
            # Gap: no risk forecasting.
            "auto_client_acquisition/intelligence_os/risk_forecast.py",
        ),
        test_probes=(
            "tests/test_bottleneck_radar.py",
            "tests/test_intelligence_os_scores.py",
        ),
    ),
    ScaleSystem(
        system_id=8,
        name="Self-Evolving Workflow System",
        name_ar="نظام التدفقات المتطورة ذاتيًا",
        primary_packages=(
            "auto_client_acquisition/learning_flywheel",
            "auto_client_acquisition/self_growth_os",
            "auto_client_acquisition/meta_os",
        ),
        router=None,
        capability_probes=(
            "auto_client_acquisition/learning_flywheel/aggregator.py",
            "auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py",
            "auto_client_acquisition/self_growth_os/tool_registry.py",
            "auto_client_acquisition/meta_os/flywheel.py",
            # Gap: no adaptive workflow optimizer.
            "auto_client_acquisition/meta_os/workflow_optimizer.py",
        ),
        test_probes=(
            "tests/test_meta_os.py",
            "tests/test_self_growth_os_package.py",
        ),
    ),
    ScaleSystem(
        system_id=9,
        name="Executive Operating System",
        name_ar="نظام التشغيل التنفيذي",
        primary_packages=(
            "auto_client_acquisition/executive_command_center",
            "auto_client_acquisition/executive_reporting",
            "auto_client_acquisition/board_decision_os",
        ),
        router="api/routers/executive_command_center.py",
        capability_probes=(
            "auto_client_acquisition/executive_command_center/builder.py",
            "auto_client_acquisition/executive_reporting/weekly_report_builder.py",
            "auto_client_acquisition/executive_reporting/next_week_plan.py",
            "auto_client_acquisition/board_decision_os/decision_engine.py",
            "auto_client_acquisition/board_decision_os/board_scorecards.py",
        ),
        test_probes=(
            "tests/test_executive_reporting.py",
            "tests/test_executive_command_center_final.py",
        ),
    ),
    ScaleSystem(
        system_id=10,
        name="Self-Evolving Enterprise Core",
        name_ar="النواة المؤسسية المتطورة ذاتيًا",
        primary_packages=(
            "auto_client_acquisition/meta_os",
            "auto_client_acquisition/self_growth_os",
            "auto_client_acquisition/endgame_os",
            "auto_client_acquisition/dealix_master_layers",
        ),
        router=None,
        capability_probes=(
            "auto_client_acquisition/meta_os/subsystems.py",
            "auto_client_acquisition/endgame_os/operating_chain.py",
            "auto_client_acquisition/endgame_os/agent_control.py",
            "auto_client_acquisition/self_growth_os/daily_growth_loop.py",
            "auto_client_acquisition/dealix_master_layers/registry.py",
            # Gap: no meta-governance loop.
            "auto_client_acquisition/meta_os/meta_governance.py",
        ),
        test_probes=("tests/test_meta_os.py",),
    ),
)


# The 10-point Final Scale Test — each item bound to the file that proves it.
FINAL_SCALE_TEST: tuple[FinalScaleCheck, ...] = (
    FinalScaleCheck(
        1,
        "Run 10+ workflows without chaos",
        "تشغيل 10+ تدفقات بلا فوضى",
        "auto_client_acquisition/workflow_os_v10/state_machine.py",
    ),
    FinalScaleCheck(
        2,
        "Run 20+ agents under full governance",
        "تشغيل 20+ وكيلًا بحوكمة كاملة",
        "auto_client_acquisition/agent_governance/agent_registry.py",
    ),
    FinalScaleCheck(
        3,
        "Manage 3+ clients without memory contamination",
        "إدارة 3+ عملاء بلا تلوّث ذاكرة",
        "auto_client_acquisition/revenue_memory/isolated_pg_event_store.py",
    ),
    FinalScaleCheck(
        4,
        "Roll back any release in minutes",
        "التراجع عن أي إصدار خلال دقائق",
        "auto_client_acquisition/secure_agent_runtime_os/deployment_rings.py",
    ),
    FinalScaleCheck(
        5,
        "Detect failures before the customer",
        "اكتشاف الأعطال قبل العميل",
        "auto_client_acquisition/observability_v6/incident.py",
    ),
    FinalScaleCheck(
        6,
        "Stop dangerous agents instantly",
        "إيقاف الوكلاء الخطرين فورًا",
        "auto_client_acquisition/secure_agent_runtime_os/kill_switch.py",
    ),
    FinalScaleCheck(
        7,
        "Explain any decision via audit + explainability",
        "شرح أي قرار عبر التدقيق والتفسير",
        "auto_client_acquisition/auditability_os/evidence_chain.py",
    ),
    FinalScaleCheck(
        8,
        "Issue executive insights weekly, automatically",
        "إصدار رؤى تنفيذية أسبوعيًا تلقائيًا",
        "auto_client_acquisition/executive_reporting/weekly_report_builder.py",
    ),
    FinalScaleCheck(
        9,
        "Improve workflows over time",
        "تحسين التدفقات مع الوقت",
        "auto_client_acquisition/meta_os/workflow_optimizer.py",
    ),
    FinalScaleCheck(
        10,
        "Measure business impact precisely",
        "قياس الأثر التجاري بدقة",
        "auto_client_acquisition/intelligence_os/events_to_metrics.py",
    ),
)


def _dir_has_python(repo_root: Path, rel: str) -> bool:
    path = repo_root / rel
    return path.is_dir() and any(path.glob("*.py"))


def _file_exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).is_file()


def evaluate_scale_system(system: ScaleSystem, repo_root: Path) -> ScaleSystemResult:
    """Score one scale system by probing the repo for its artifacts."""
    missing_packages = tuple(
        pkg for pkg in system.primary_packages if not _dir_has_python(repo_root, pkg)
    )
    missing_probes = tuple(
        probe for probe in system.capability_probes if not _file_exists(repo_root, probe)
    )
    missing_router = bool(system.router) and not _file_exists(repo_root, system.router)
    missing_tests = tuple(test for test in system.test_probes if not _file_exists(repo_root, test))

    if missing_packages:
        status: SystemStatus = "fail"
    elif missing_probes or missing_router or missing_tests:
        status = "partial"
    else:
        status = "pass"

    return ScaleSystemResult(
        system_id=system.system_id,
        name=system.name,
        name_ar=system.name_ar,
        status=status,
        missing_packages=missing_packages,
        missing_probes=missing_probes,
        missing_router=missing_router,
        missing_tests=missing_tests,
    )


def evaluate_final_scale_test(
    repo_root: Path,
) -> tuple[tuple[FinalScaleCheck, bool], ...]:
    """Evaluate each of the 10 Final Scale Test items against the repo."""
    return tuple((check, _file_exists(repo_root, check.probe)) for check in FINAL_SCALE_TEST)


def _verdict(systems_passed: int, systems_failed: int, final_scale_score: int) -> Verdict:
    if systems_failed > 0 or final_scale_score < 5:
        return "BLOCKED"
    if systems_passed == len(SCALE_SYSTEMS) and final_scale_score >= 8:
        return "PASS"
    return "PARTIAL"


def compute_scale_readiness(repo_root: Path) -> ScaleReadinessReport:
    """Run the full scale-readiness introspection and return one report."""
    systems = tuple(evaluate_scale_system(system, repo_root) for system in SCALE_SYSTEMS)
    final_scale = evaluate_final_scale_test(repo_root)

    systems_passed = sum(1 for s in systems if s.status == "pass")
    systems_partial = sum(1 for s in systems if s.status == "partial")
    systems_failed = sum(1 for s in systems if s.status == "fail")
    final_scale_score = sum(1 for _, ok in final_scale if ok)

    return ScaleReadinessReport(
        systems=systems,
        final_scale=final_scale,
        systems_passed=systems_passed,
        systems_partial=systems_partial,
        systems_failed=systems_failed,
        final_scale_score=final_scale_score,
        verdict=_verdict(systems_passed, systems_failed, final_scale_score),
    )

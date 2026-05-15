"""AI Operating Fabric — the 12-layer index for the agentic enterprise.

This module is the unifying nervous-system layer: it does not re-implement
agent, workflow, memory, governance, etc. — those already exist as packages.
It declares the 12 canonical layers of the agentic enterprise, maps each one
to the packages that implement it, and resolves a *real* health signal by
checking whether those packages exist on disk (no fake proof).

Source vision: docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md.
Numbered constitution map: auto_client_acquisition/dealix_master_layers/registry.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FabricLayer:
    """One of the 12 layers of the agentic-enterprise operating fabric."""

    number: int
    key: str
    title_ar: str
    title_en: str
    mandate_ar: str
    mandate_en: str
    primary_packages: tuple[str, ...]
    capabilities: tuple[str, ...]


# The 12 layers, in vision order. Every layer is governed: humans stay
# over the loop (governance fabric is layer 5), nothing here is autonomous
# without a policy + audit trail.
FABRIC_LAYERS: tuple[FabricLayer, ...] = (
    FabricLayer(
        number=1,
        key="agent_operating_system",
        title_ar="نظام تشغيل الوكلاء",
        title_en="Agent Operating System",
        mandate_ar="دورة حياة الوكيل: الهوية، الصلاحيات، الذاكرة، الأدوات، التفويض، التقييم.",
        mandate_en="Agent lifecycle: identity, permissions, memory, tools, delegation, evaluation.",
        primary_packages=(
            "agent_os",
            "agent_identity_access_os",
            "agent_governance",
            "secure_agent_runtime_os",
        ),
        capabilities=(
            "agent_lifecycle",
            "identity_and_permissions",
            "tool_boundaries",
            "kill_switch",
        ),
    ),
    FabricLayer(
        number=2,
        key="workflow_intelligence",
        title_ar="نظام ذكاء سير العمل",
        title_en="Workflow Intelligence System",
        mandate_ar="الأحداث، القرارات، الموافقات، سلاسل التنفيذ، الاستثناءات، إعادة المحاولة.",
        mandate_en="Events, decisions, approvals, execution chains, exceptions, retries.",
        primary_packages=("workflow_os", "delivery_os", "orchestrator"),
        capabilities=(
            "event_routing",
            "approval_flow",
            "execution_chains",
            "exception_handling",
        ),
    ),
    FabricLayer(
        number=3,
        key="organizational_memory",
        title_ar="نظام الذاكرة المؤسسية",
        title_en="Organizational Memory System",
        mandate_ar="ذاكرة المعرفة، سير العمل، العملاء، التنفيذ، السياسات — تتحول إلى ذكاء مؤسسي.",
        mandate_en="Knowledge, workflow, customer, operational and policy memory — institutional intelligence.",
        primary_packages=("knowledge_os", "revenue_memory", "company_brain"),
        capabilities=(
            "knowledge_memory",
            "workflow_memory",
            "customer_memory",
            "operational_memory",
        ),
    ),
    FabricLayer(
        number=4,
        key="execution_engine",
        title_ar="محرك التنفيذ",
        title_en="Execution Engine",
        mandate_ar="تنفيذ عمليات الأعمال فعليًا: تحديث CRM، إرسال محكوم، إنشاء عروض، تشغيل سير العمل.",
        mandate_en="Executes real business operations: CRM updates, governed sends, proposals, workflow triggers.",
        primary_packages=("execution_os", "agentic_operations_os", "safe_send_gateway"),
        capabilities=(
            "operation_execution",
            "governed_outbound",
            "workflow_triggers",
            "failure_escalation",
        ),
    ),
    FabricLayer(
        number=5,
        key="governance_fabric",
        title_ar="نسيج الحوكمة",
        title_en="Governance Fabric",
        mandate_ar="أنظمة مستقلة محكومة: سياسات، موافقات، تدقيق، قابلية تفسير، امتثال، مخاطر.",
        mandate_en="Governed autonomous systems: policy, approval, audit, explainability, compliance, risk.",
        primary_packages=(
            "governance_os",
            "compliance_os",
            "auditability_os",
            "responsible_ai_os",
        ),
        capabilities=(
            "policy_engine",
            "approval_engine",
            "audit_engine",
            "explainability_engine",
        ),
    ),
    FabricLayer(
        number=6,
        key="executive_intelligence",
        title_ar="محرك الذكاء التنفيذي",
        title_en="Executive Intelligence Engine",
        mandate_ar="AI COO: إشارات الإيراد، المخاطر التشغيلية، اختناقات سير العمل، الموجزات التنفيذية.",
        mandate_en="AI COO: revenue signals, operational risk, workflow bottlenecks, executive briefs.",
        primary_packages=(
            "executive_command_center",
            "intelligence_os",
            "executive_reporting",
        ),
        capabilities=(
            "revenue_signals",
            "operational_risk",
            "executive_briefs",
            "strategic_recommendations",
        ),
    ),
    FabricLayer(
        number=7,
        key="evaluation_quality",
        title_ar="محرك التقييم والجودة",
        title_en="Evaluation & Quality Engine",
        mandate_ar="قياس الهلوسة، جودة الإسناد، نجاح سير العمل، صحة التصعيد، الأثر التجاري.",
        mandate_en="Measures hallucination, grounding quality, workflow success, escalation correctness, business impact.",
        primary_packages=("service_quality", "benchmark_os"),
        capabilities=(
            "hallucination_rate",
            "grounding_quality",
            "workflow_success",
            "business_impact",
        ),
    ),
    FabricLayer(
        number=8,
        key="observability_engine",
        title_ar="محرك القابلية للرصد",
        title_en="Observability Engine",
        mandate_ar="آثار التنفيذ، الأعطال، إعادة المحاولة، الكمون، استهلاك التوكنز، صحة الوكلاء.",
        mandate_en="Traces, failures, retries, latency, token usage, policy violations, agent health.",
        primary_packages=("agent_observability", "observability_v10", "reliability_os"),
        capabilities=(
            "traces",
            "failure_tracking",
            "latency_and_cost",
            "agent_health",
        ),
    ),
    FabricLayer(
        number=9,
        key="transformation_engine",
        title_ar="محرك التحول",
        title_en="Transformation Engine",
        mandate_ar="أطر التحول، نماذج النضج، إعادة تصميم نموذج التشغيل، خرائط طريق الحوكمة.",
        mandate_en="Transformation frameworks, maturity models, operating-model redesign, governance roadmaps.",
        primary_packages=("client_maturity_os", "adoption_os", "standards_os"),
        capabilities=(
            "maturity_models",
            "operating_model_redesign",
            "ai_adoption_systems",
            "governance_roadmaps",
        ),
    ),
    FabricLayer(
        number=10,
        key="digital_workforce",
        title_ar="محرك القوى العاملة الرقمية",
        title_en="Digital Workforce Engine",
        mandate_ar="أقسام AI، موظفو AI، مشرفو AI، تقارير AI — نظام تشغيل للعمل الرقمي.",
        mandate_en="AI departments, AI employees, AI supervisors, AI reporting — an OS for digital labor.",
        primary_packages=("ai_workforce", "ai_workforce_v10", "role_command_os"),
        capabilities=(
            "ai_departments",
            "ai_supervisors",
            "hybrid_human_agent_org",
            "workforce_reporting",
        ),
    ),
    FabricLayer(
        number=11,
        key="organizational_graph",
        title_ar="محرك الرسم البياني المؤسسي",
        title_en="Organizational Graph Engine",
        mandate_ar="فهم العلاقات بين الناس، سير العمل، الموافقات، العملاء، القرارات، المخاطر، المعرفة.",
        mandate_en="Relationships between people, workflows, approvals, customers, decisions, risks, knowledge.",
        primary_packages=("unified_operating_graph", "revenue_graph"),
        capabilities=(
            "entity_graph",
            "relationship_intelligence",
            "graph_summarization",
        ),
    ),
    FabricLayer(
        number=12,
        key="continuous_evolution",
        title_ar="محرك التطور المستمر",
        title_en="Continuous Evolution Engine",
        mandate_ar="حلقات تغذية راجعة، سير عمل ذاتي التحسين، تحسين مدفوع بالتقييم، تطور الذاكرة.",
        mandate_en="Feedback loops, self-improving workflows, evaluation-driven optimization, memory evolution.",
        primary_packages=(
            "learning_flywheel",
            "self_growth_os",
            "intelligence_compounding_os",
        ),
        capabilities=(
            "feedback_loops",
            "self_improving_workflows",
            "evaluation_driven_optimization",
            "operational_learning",
        ),
    ),
)


def _repo_root() -> Path:
    # fabric.py → agentic_enterprise_os → auto_client_acquisition → repo root
    return Path(__file__).resolve().parents[2]


def layer_by_number(number: int) -> FabricLayer | None:
    """Return the layer with this 1-based number, or None."""
    for layer in FABRIC_LAYERS:
        if layer.number == number:
            return layer
    return None


def layer_by_key(key: str) -> FabricLayer | None:
    """Return the layer with this slug key, or None."""
    for layer in FABRIC_LAYERS:
        if layer.key == key:
            return layer
    return None


def package_exists(package: str, repo_root: Path | None = None) -> bool:
    """True if `auto_client_acquisition/<package>/` is a real package on disk."""
    root = repo_root or _repo_root()
    pkg_dir = root / "auto_client_acquisition" / package
    return pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file()


def _status_for(coverage: float) -> str:
    if coverage >= 1.0:
        return "operational"
    if coverage >= 0.5:
        return "partial"
    if coverage > 0.0:
        return "scaffold"
    return "missing"


def resolve_layer_health(
    layer: FabricLayer, repo_root: Path | None = None
) -> dict[str, object]:
    """Resolve a layer's real health by checking its packages exist on disk."""
    root = repo_root or _repo_root()
    packages = {
        pkg: package_exists(pkg, root) for pkg in layer.primary_packages
    }
    present = sum(1 for ok in packages.values() if ok)
    total = len(packages)
    coverage = (present / total) if total else 0.0
    return {
        "number": layer.number,
        "key": layer.key,
        "title_ar": layer.title_ar,
        "title_en": layer.title_en,
        "packages": packages,
        "packages_present": present,
        "packages_total": total,
        "coverage": round(coverage, 4),
        "status": _status_for(coverage),
    }


def layer_to_dict(layer: FabricLayer) -> dict[str, object]:
    """Static descriptor for a layer (no disk check)."""
    return {
        "number": layer.number,
        "key": layer.key,
        "title_ar": layer.title_ar,
        "title_en": layer.title_en,
        "mandate_ar": layer.mandate_ar,
        "mandate_en": layer.mandate_en,
        "primary_packages": list(layer.primary_packages),
        "capabilities": list(layer.capabilities),
    }


def maturity_score(repo_root: Path | None = None) -> float:
    """Overall fabric maturity: mean coverage across the 12 layers, 0.0–1.0."""
    root = repo_root or _repo_root()
    if not FABRIC_LAYERS:
        return 0.0
    total = sum(
        float(resolve_layer_health(layer, root)["coverage"])
        for layer in FABRIC_LAYERS
    )
    return round(total / len(FABRIC_LAYERS), 4)


def fabric_status(repo_root: Path | None = None) -> dict[str, object]:
    """Full 12-layer rollup — the organizational nervous-system snapshot."""
    root = repo_root or _repo_root()
    layers = [resolve_layer_health(layer, root) for layer in FABRIC_LAYERS]
    operational = sum(1 for ly in layers if ly["status"] == "operational")
    score = maturity_score(root)
    if score >= 0.9:
        grade = "agentic_operating_company"
    elif score >= 0.6:
        grade = "agentic_transition"
    elif score >= 0.3:
        grade = "ai_augmented"
    else:
        grade = "ai_curious"
    return {
        "fabric": "ai_operating_fabric",
        "layer_count": len(FABRIC_LAYERS),
        "layers_operational": operational,
        "maturity_score": score,
        "maturity_grade": grade,
        "human_over_the_loop": True,
        "layers": layers,
        "source_of_truth": "auto_client_acquisition/agentic_enterprise_os/fabric.py",
        "governance_decision": "allow",
    }

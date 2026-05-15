"""Machine-readable index for docs/NN_* master layers ↔ implementation paths.

See docs/DEALIX_MASTER_LAYERS_MAP.md and docs/enterprise_architecture/SYSTEM_MAP.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DealixLayer:
    """One numbered layer in the Dealix constitution map."""

    folder: str
    title_ar: str
    primary_packages: tuple[str, ...]


@dataclass(frozen=True)
class OrganizationalIntelligenceLayer:
    """One layer in the Organizational Intelligence Dominance map."""

    layer_id: int
    slug: str
    title: str
    objective: str
    target_paths: tuple[str, ...]
    mapped_paths: tuple[str, ...]
    success_checks: tuple[str, ...]


# Order matches docs/00 … docs/36 README sequence.
MASTER_LAYERS: tuple[DealixLayer, ...] = (
    DealixLayer("00_constitution", "الأطروحة والدستور", ("revenue_memory", "institutional_control_os")),
    DealixLayer("01_category_creation", "صناعة الفئة", ("category_os",)),
    DealixLayer("02_strategy", "الهوية الاستراتيجية", ("strategy_os", "gtm_os")),
    DealixLayer("03_saudi_positioning", "التموضع السعودي", ("market_intelligence", "revenue_os")),
    DealixLayer("04_product_strategy", "استراتيجية المنتج", ("service_catalog", "commercial_engagements")),
    DealixLayer("05_client_os", "نظام تشغيل العميل", ("client_os",)),
    DealixLayer("06_data_os", "طبقة البيانات", ("data_os", "customer_data_plane")),
    DealixLayer("07_governance", "الحوكمة", ("governance_os", "compliance_trust_os")),
    DealixLayer("08_responsible_ai", "AI المسؤول", ("responsible_ai_os",)),
    DealixLayer("09_llm_gateway", "بوابة النماذج", ("llm_gateway_v10",)),
    DealixLayer("10_agents", "الوكلاء المحكومون", ("agentic_operations_os", "ai_workforce", "agent_governance")),
    DealixLayer("11_secure_runtime", "تشغيل آمن", ("tool_guardrail_gateway", "safe_send_gateway")),
    DealixLayer("12_auditability", "التدقيق والمساءلة", ("compliance_trust_os", "evidence_control_plane_os")),
    DealixLayer("13_evidence_control_plane", "سيطرة الأدلة", ("evidence_control_plane_os",)),
    DealixLayer("14_proof", "Proof OS", ("proof_architecture_os", "proof_ledger")),
    DealixLayer("15_value", "Value OS", ("value_capture_os", "proof_architecture_os")),
    DealixLayer("16_capital", "Capital OS", ("operating_finance_os", "board_decision_os")),
    DealixLayer("17_revenue_os", "Revenue OS", ("revenue_os", "revenue_pipeline")),
    DealixLayer("18_brain_os", "Company Brain", ("knowledge_os", "company_brain")),
    DealixLayer("19_workflow_os", "Workflow OS", ("delivery_os",)),
    DealixLayer("20_adoption", "التبني", ("adoption_os", "customer_success")),
    DealixLayer("21_operating_rhythm", "إيقاع التشغيل", ("operating_rhythm_os",)),
    DealixLayer("22_board_decision", "قرارات المجلس", ("board_decision_os",)),
    DealixLayer("23_intelligence", "الذكاء المركّب", ("intelligence_os", "intelligence_compounding_os")),
    DealixLayer("24_risk_resilience", "المخاطر والمرونة", ("risk_resilience_os",)),
    DealixLayer("25_compliance_trust", "الامتثال والثقة", ("compliance_trust_os", "compliance_os")),
    DealixLayer("26_human_amplified", "المنظمة المضخّمة بالبشر", ("personal_operator", "executive_command_center")),
    DealixLayer("27_value_capture", "التقاط القيمة", ("value_capture_os",)),
    DealixLayer("28_operating_finance", "المالية التشغيلية", ("operating_finance_os", "finance_os")),
    DealixLayer("29_enterprise_rollout", "دخول المؤسسات", ("enterprise_rollout_os", "enterprise_os")),
    DealixLayer("30_standards", "المعايير", ("standards_os",)),
    DealixLayer("31_certification", "الشهادات", ("ecosystem_os",)),
    DealixLayer("32_ecosystem", "النظام البيئي", ("ecosystem_os", "partnership_os")),
    DealixLayer("33_ventures", "مصنع المشاريع", ("endgame_os", "holding_os")),
    DealixLayer("34_market_power", "قوة السوق", ("market_power_os", "dominance_os")),
    DealixLayer("35_tests", "الاختبارات والحواجز", ("tests",)),
    DealixLayer("36_architecture", "المعمارية", ("api",)),
)

# Optional hints for cross-cutting concerns not tied to a single layer folder.
IMPLEMENTATION_HINTS: dict[str, tuple[str, ...]] = {
    "saudi_layer": ("revenue_os", "market_intelligence", "pipelines"),
    "revenue_memory": ("revenue_memory",),
}

# Coarser 10-layer dominance map over existing repository capabilities.
OI_DOMINANCE_LAYERS: tuple[OrganizationalIntelligenceLayer, ...] = (
    OrganizationalIntelligenceLayer(
        layer_id=1,
        slug="enterprise_operating_fabric",
        title="Enterprise Operating Fabric",
        objective="Unify operating context, events, workflow state, and governance context.",
        target_paths=(
            "/platform/operating_fabric",
            "/platform/context_engine",
            "/platform/event_mesh",
            "/platform/state_management",
            "/platform/organizational_context",
        ),
        mapped_paths=(
            "auto_client_acquisition/platform_v10",
            "auto_client_acquisition/orchestrator",
            "auto_client_acquisition/unified_operating_graph",
            "auto_client_acquisition/operating_rhythm_os",
            "api/routers/domains",
        ),
        success_checks=(
            "All workflows resolve organization context before execution.",
            "Runtime can explain policy and approval ancestry for each transition.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=2,
        slug="digital_workforce_infrastructure",
        title="Digital Workforce Infrastructure",
        objective="Operate agents as governed workforce units with identity and lifecycle.",
        target_paths=(
            "/platform/digital_workforce",
            "/platform/agent_runtime",
            "/platform/agent_registry",
            "/platform/agent_supervision",
            "/platform/agent_coordination",
            "/agents",
        ),
        mapped_paths=(
            "auto_client_acquisition/ai_workforce",
            "auto_client_acquisition/ai_workforce_v10",
            "auto_client_acquisition/agents",
            "auto_client_acquisition/agent_governance",
            "auto_client_acquisition/agent_identity_access_os",
            "auto_client_acquisition/agent_observability",
            "auto_client_acquisition/revenue_graph/agent_registry.py",
        ),
        success_checks=(
            "Every production agent has owner, role, permissions, and KPI contract.",
            "Agent onboarding and offboarding produce auditable lifecycle records.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=3,
        slug="agentic_bpm_engine",
        title="Agentic BPM Engine",
        objective="Deliver adaptive process execution while preserving business boundaries.",
        target_paths=(
            "/platform/agentic_bpm",
            "/platform/process_engine",
            "/platform/workflow_reasoning",
            "/platform/adaptive_orchestration",
        ),
        mapped_paths=(
            "auto_client_acquisition/workflow_os_v10",
            "auto_client_acquisition/workflow_os",
            "auto_client_acquisition/delivery_factory",
            "auto_client_acquisition/service_sessions",
            "auto_client_acquisition/customer_loop",
        ),
        success_checks=(
            "Workflow routing adapts to runtime signals without bypassing approvals.",
            "Process transitions remain deterministic and replayable from events.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=4,
        slug="organizational_memory_fabric",
        title="Organizational Memory Fabric",
        objective="Persist customer, workflow, governance, and incident memory with lineage.",
        target_paths=(
            "/memory",
            "/platform/memory_fabric",
            "/platform/lineage",
            "/platform/citations",
            "/platform/retrieval",
            "/platform/reranking",
        ),
        mapped_paths=(
            "auto_client_acquisition/revenue_memory",
            "auto_client_acquisition/knowledge_os",
            "auto_client_acquisition/company_brain",
            "auto_client_acquisition/radar_events",
            "dealix/caching/semantic_cache.py",
        ),
        success_checks=(
            "Every executive decision can be traced to evidence and policy lineage.",
            "Retrieval responses include citations and freshness provenance.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=5,
        slug="governed_autonomy_engine",
        title="Governed Autonomy Engine",
        objective="Allow autonomous action only inside policy fences and approval checkpoints.",
        target_paths=(
            "/platform/runtime_governance",
            "/platform/tool_fencing",
            "/platform/escalation",
            "/platform/reversibility",
            "/platform/approval_engine",
        ),
        mapped_paths=(
            "auto_client_acquisition/governance_os",
            "auto_client_acquisition/approval_center",
            "auto_client_acquisition/tool_guardrail_gateway",
            "auto_client_acquisition/safe_send_gateway",
            "auto_client_acquisition/secure_agent_runtime_os",
            "dealix/trust",
        ),
        success_checks=(
            "Every external action is draft-first or approval-gated.",
            "Every mutation path supports rollback or compensating action.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=6,
        slug="execution_dominance_engine",
        title="Execution Dominance Engine",
        objective="Guarantee reliable, recoverable, and observable workflow execution.",
        target_paths=(
            "/platform/execution_engine",
            "/platform/orchestration",
            "/platform/recovery_engine",
            "/platform/queues",
            "/platform/compensation_logic",
        ),
        mapped_paths=(
            "dealix/execution",
            "dealix/reliability",
            "auto_client_acquisition/execution_os",
            "auto_client_acquisition/revenue_pipeline",
            "auto_client_acquisition/reliability_os",
            "auto_client_acquisition/pipeline.py",
        ),
        success_checks=(
            "Core workflows are idempotent, retry-safe, and dead-letter observable.",
            "Recovery playbooks restore operation without data corruption.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=7,
        slug="executive_intelligence_engine",
        title="Executive Intelligence Engine",
        objective="Convert operational telemetry into decision-ready strategic intelligence.",
        target_paths=(
            "/executive",
            "/intelligence",
            "/platform/forecasting",
            "/platform/organizational_insights",
            "/platform/risk_forecasting",
        ),
        mapped_paths=(
            "auto_client_acquisition/executive_command_center",
            "auto_client_acquisition/board_decision_os",
            "auto_client_acquisition/executive_reporting",
            "auto_client_acquisition/reporting_os",
            "auto_client_acquisition/intelligence_os",
            "auto_client_acquisition/revenue_science",
        ),
        success_checks=(
            "Leadership dashboards expose ROI, bottlenecks, and forecast confidence.",
            "Strategic briefs reference governed evidence and confidence intervals.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=8,
        slug="trust_and_explainability_engine",
        title="Trust and Explainability Engine",
        objective="Make every high-impact decision auditable, explainable, and accountable.",
        target_paths=(
            "/platform/trust_engine",
            "/platform/explainability",
            "/platform/accountability",
            "/platform/auditability",
        ),
        mapped_paths=(
            "dealix/trust",
            "auto_client_acquisition/auditability_os",
            "auto_client_acquisition/responsible_ai_os",
            "auto_client_acquisition/compliance_trust_os",
            "auto_client_acquisition/revenue_graph/why_now.py",
        ),
        success_checks=(
            "Decision outputs include machine-readable explanation payloads.",
            "Audit trails support human oversight and incident reconstruction.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=9,
        slug="evaluation_dominance",
        title="Evaluation Dominance",
        objective="Gate releases by workflow quality, governance quality, and business impact.",
        target_paths=(
            "/evals/hallucination",
            "/evals/retrieval",
            "/evals/workflow_execution",
            "/evals/governance",
            "/evals/operational_efficiency",
            "/evals/business_impact",
        ),
        mapped_paths=(
            "evals",
            "docs/product/EVALUATION_REGISTRY.md",
            "tests/test_output_quality_gate.py",
            "tests/test_v5_layers.py",
            "tests/test_safe_action_gateway.py",
        ),
        success_checks=(
            "No release passes without governance and workflow eval gates.",
            "Evaluation scores are linked to business and operational outcomes.",
        ),
    ),
    OrganizationalIntelligenceLayer(
        layer_id=10,
        slug="self_evolving_enterprise_engine",
        title="Self-Evolving Enterprise Engine",
        objective="Continuously improve workflows, governance, and coordination safely.",
        target_paths=(
            "/platform/self_improvement",
            "/platform/feedback_loops",
            "/platform/optimization",
            "/platform/adaptive_orchestration",
            "/platform/learning_systems",
        ),
        mapped_paths=(
            "auto_client_acquisition/self_growth_os",
            "auto_client_acquisition/learning_flywheel",
            "auto_client_acquisition/intelligence_compounding_os",
            "auto_client_acquisition/bottleneck_radar",
            "auto_client_acquisition/revenue_os/learning_weekly.py",
        ),
        success_checks=(
            "Improvement loops promote only after governance and impact verification.",
            "Optimization history preserves reversibility and reasoning lineage.",
        ),
    ),
)


def readme_path(repo_root: Path, folder: str) -> Path:
    return repo_root / "docs" / folder / "README.md"


def layer_by_folder(folder: str) -> DealixLayer | None:
    for layer in MASTER_LAYERS:
        if layer.folder == folder:
            return layer
    return None


def dominance_layer_by_slug(slug: str) -> OrganizationalIntelligenceLayer | None:
    for layer in OI_DOMINANCE_LAYERS:
        if layer.slug == slug:
            return layer
    return None


def dominance_layer_by_id(layer_id: int) -> OrganizationalIntelligenceLayer | None:
    for layer in OI_DOMINANCE_LAYERS:
        if layer.layer_id == layer_id:
            return layer
    return None

"""Platform maturity stages — the 5-stage ladder for Dealix itself.

Measures the *platform's* organizational capability maturity, not a customer's.
A stage is a claim about what Dealix can reliably operate, not a feature count.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MaturityStage:
    stage_id: str
    level: int
    name_en: str
    name_ar: str
    description_ar: str
    entry_signals: tuple[str, ...]


STAGES: tuple[MaturityStage, ...] = (
    MaturityStage(
        stage_id="ai_tool",
        level=1,
        name_en="AI Tool",
        name_ar="أداة ذكاء اصطناعي",
        description_ar="prompts و APIs و chatbot و workflows بسيطة. AI يجاوب فقط.",
        entry_signals=(
            "ai_responds_to_prompts",
            "apis_exposed",
        ),
    ),
    MaturityStage(
        stage_id="ai_saas_platform",
        level=2,
        name_en="AI SaaS Platform",
        name_ar="منصة SaaS بالذكاء الاصطناعي",
        description_ar="auth و dashboards و billing و workspaces و usage tracking. العملاء يستخدمون النظام.",
        entry_signals=(
            "auth_and_workspaces",
            "billing_active",
            "onboarding_exists",
            "usage_tracking",
        ),
    ),
    MaturityStage(
        stage_id="enterprise_ai_platform",
        level=3,
        name_en="Enterprise AI Platform",
        name_ar="منصة ذكاء اصطناعي للمؤسسات",
        description_ar="tenant isolation و governance و knowledge layer و workflow execution و evaluation.",
        entry_signals=(
            "tenant_isolation",
            "governance_with_approvals",
            "permission_aware_retrieval",
            "workflows_executed",
            "evaluation_in_place",
        ),
    ),
    MaturityStage(
        stage_id="agentic_operating_platform",
        level=4,
        name_en="Agentic Operating Platform",
        name_ar="منصة تشغيل وكيلية",
        description_ar="agents تنفذ workflows مع orchestration و humans فوق الحلقة و organizational memory.",
        entry_signals=(
            "agents_run_full_workflows",
            "agent_lifecycle_managed",
            "approval_routing_and_escalation",
            "organizational_memory",
            "operational_intelligence_measured",
        ),
    ),
    MaturityStage(
        stage_id="agentic_enterprise_infrastructure",
        level=5,
        name_en="Agentic Enterprise Infrastructure",
        name_ar="بنية تحتية وكيلية للمؤسسات",
        description_ar="Dealix يصبح operating layer للمؤسسة — mission critical infrastructure.",
        entry_signals=(
            "companies_depend_on_dealix_to_operate",
            "multi_agent_coordination_at_scale",
            "governed_autonomy",
            "continuous_learning",
            "mission_critical_reliability",
        ),
    ),
)

_BY_LEVEL: dict[int, MaturityStage] = {s.level: s for s in STAGES}
_BY_ID: dict[str, MaturityStage] = {s.stage_id: s for s in STAGES}

MIN_LEVEL: int = 1
MAX_LEVEL: int = len(STAGES)


def stage_for_level(level: int) -> MaturityStage:
    """Return the stage at `level`, clamped to the 1..5 range."""
    clamped = max(MIN_LEVEL, min(MAX_LEVEL, level))
    return _BY_LEVEL[clamped]


def stage_by_id(stage_id: str) -> MaturityStage | None:
    return _BY_ID.get(stage_id)


def next_stage(level: int) -> MaturityStage | None:
    """The stage above `level`, or None if already at the top."""
    if level >= MAX_LEVEL:
        return None
    return _BY_LEVEL[max(MIN_LEVEL, level) + 1]


__all__ = [
    "MAX_LEVEL",
    "MIN_LEVEL",
    "STAGES",
    "MaturityStage",
    "next_stage",
    "stage_by_id",
    "stage_for_level",
]

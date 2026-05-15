"""The 6 canonical agent templates and their compilation to AgentSpec.

Templates are design-time definitions. ``to_agent_spec`` compiles a
template into the runtime contract consumed by ``ai_workforce``.
"""

from __future__ import annotations

from auto_client_acquisition.agent_factory.template_schema import (
    AgentTemplate,
    EscalationRule,
    MemoryPolicy,
)
from auto_client_acquisition.ai_workforce.schemas import (
    AgentSpec,
    AutonomyLevel,
    RiskLevel,
)

_TENANT_MEMORY = MemoryPolicy(
    episodic=True, semantic=True, cross_customer=False, ttl_hours=720
)
_LIGHT_MEMORY = MemoryPolicy(
    episodic=True, semantic=False, cross_customer=False, ttl_hours=168
)


_TEMPLATES: tuple[AgentTemplate, ...] = (
    AgentTemplate(
        template_id="sales_agent",
        role_en="Sales drafting agent",
        role_ar="وكيل صياغة المبيعات",
        goals=("draft qualified outreach", "rank opportunities"),
        allowed_tools=("sales_os.qualify_opportunity", "draft_arabic_copy"),
        forbidden_tools=("cold_whatsapp", "linkedin_automation", "send_whatsapp_live"),
        permissions=("sales_rep", "sales_manager", "tenant_admin"),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=_TENANT_MEMORY,
        escalation_rules=(
            EscalationRule("low_confidence", "sales_manager", "approval_required"),
            EscalationRule("external_send_requested", "sales_manager", "approval_required"),
        ),
        eval_metrics=("response_groundedness", "workflow_task_success"),
        risk_class=RiskLevel.MEDIUM,
        cost_budget_usd=0.50,
    ),
    AgentTemplate(
        template_id="support_agent",
        role_en="Support triage agent",
        role_ar="وكيل فرز الدعم",
        goals=("classify tickets", "draft suggested replies"),
        allowed_tools=("customer_loop.next_actions_for_state",),
        forbidden_tools=("send_email_live", "send_whatsapp_live"),
        permissions=("sales_rep", "sales_manager", "tenant_admin"),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=_LIGHT_MEMORY,
        escalation_rules=(
            EscalationRule("sla_breach", "sales_manager", "approval_required"),
            EscalationRule("sentiment_negative", "sales_manager", "approval_required"),
        ),
        eval_metrics=("response_groundedness", "business_resolution_rate"),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.30,
    ),
    AgentTemplate(
        template_id="ops_agent",
        role_en="Operations planning agent",
        role_ar="وكيل تخطيط العمليات",
        goals=("plan delivery steps", "flag bottlenecks"),
        allowed_tools=("delivery_factory.build_delivery_plan",),
        forbidden_tools=("charge_payment_live",),
        permissions=("sales_manager", "tenant_admin"),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=_LIGHT_MEMORY,
        escalation_rules=(
            EscalationRule("cost_budget_exceeded", "tenant_admin", "approval_required"),
        ),
        eval_metrics=("workflow_task_success", "workflow_retry_rate"),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.40,
    ),
    AgentTemplate(
        template_id="research_agent",
        role_en="Market research agent",
        role_ar="وكيل بحث السوق",
        goals=("summarize sector signals", "surface benchmarks"),
        allowed_tools=("knowledge_os.grounded_answer",),
        forbidden_tools=("scrape_web",),
        permissions=("sales_rep", "sales_manager", "tenant_admin"),
        autonomy_level=AutonomyLevel.ANALYZE_ONLY,
        memory_policy=_LIGHT_MEMORY,
        escalation_rules=(
            EscalationRule("insufficient_evidence", "sales_manager", "approval_required"),
        ),
        eval_metrics=("retrieval_relevance", "response_groundedness"),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.35,
    ),
    AgentTemplate(
        template_id="executive_agent",
        role_en="Executive briefing agent",
        role_ar="وكيل الموجز التنفيذي",
        goals=("compose executive briefs", "rank next actions"),
        allowed_tools=("executive_reporting.build_weekly_report",),
        forbidden_tools=("send_email_live",),
        permissions=("tenant_admin", "super_admin"),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=_TENANT_MEMORY,
        escalation_rules=(
            EscalationRule("risk_high", "tenant_admin", "approval_required"),
        ),
        eval_metrics=("response_groundedness", "business_roi_evidence"),
        risk_class=RiskLevel.MEDIUM,
        cost_budget_usd=0.60,
    ),
    AgentTemplate(
        template_id="governance_agent",
        role_en="Governance guard agent",
        role_ar="وكيل حارس الحوكمة",
        goals=("apply policy checks", "veto unsafe actions"),
        allowed_tools=("governance_os.policy_check",),
        forbidden_tools=(),
        permissions=("tenant_admin", "super_admin"),
        autonomy_level=AutonomyLevel.APPROVAL_REQUIRED,
        memory_policy=_LIGHT_MEMORY,
        escalation_rules=(
            EscalationRule("policy_violation", "super_admin", "blocked"),
        ),
        eval_metrics=("workflow_escalation_correctness",),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.20,
    ),
)


TEMPLATE_IDS: frozenset[str] = frozenset(t.template_id for t in _TEMPLATES)


def list_templates() -> list[AgentTemplate]:
    """The 6 agent templates in declaration order."""
    return list(_TEMPLATES)


def get_template(template_id: str) -> AgentTemplate:
    """Return one template by id. Raises KeyError if unknown."""
    for t in _TEMPLATES:
        if t.template_id == template_id:
            return t
    raise KeyError(f"unknown template_id: {template_id}")


def to_agent_spec(template: AgentTemplate, agent_id: str) -> AgentSpec:
    """Compile a design-time template into a runtime ``AgentSpec``."""
    if not agent_id:
        raise ValueError("agent_id is required")
    return AgentSpec(
        agent_id=agent_id,
        role_ar=template.role_ar,
        role_en=template.role_en,
        allowed_inputs=["WorkforceGoal", "prior_outputs"],
        allowed_outputs=["AgentTask"],
        allowed_tools=list(template.allowed_tools),
        forbidden_tools=list(template.forbidden_tools),
        autonomy_level=template.autonomy_level,
        default_action_mode=template.default_action_mode,
        risk_level=template.risk_class,
        requires_approval=True,
        cost_budget_usd=template.cost_budget_usd,
        evidence_required=template.evidence_required,
    )

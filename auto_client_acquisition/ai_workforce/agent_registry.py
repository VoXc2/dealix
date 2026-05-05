"""Static registry of the 12 specialized AI Workforce agents.

Each AgentSpec records the agent's role, allowed tools, forbidden
tools, autonomy level, risk and cost budget. The orchestrator reads
this registry — agents themselves are pure-function wrappers in
``agent_contracts.py``.

Hard rules baked into the registry:
  - SaudiCopyAgent forbids the 5 cold-outreach / scrape tools.
  - FinanceAgent forbids ``charge_payment_live``.
  - ComplianceGuardAgent uses ``approval_required`` autonomy (veto).
  - No agent's ``default_action_mode`` is a live-send/charge token.
"""
from __future__ import annotations

from auto_client_acquisition.ai_workforce.schemas import (
    AgentSpec,
    AutonomyLevel,
    RiskLevel,
)


# Hard-rule forbidden tool names — these tokens are NEVER live-callable
# by any agent. SaudiCopyAgent and FinanceAgent require the relevant
# subset to appear explicitly in their forbidden_tools list.
SAUDI_COPY_FORBIDDEN: tuple[str, ...] = (
    "cold_whatsapp",
    "linkedin_automation",
    "scrape_web",
    "send_email_live",
    "send_whatsapp_live",
)

FINANCE_FORBIDDEN: tuple[str, ...] = (
    "charge_payment_live",
)


def _spec(
    agent_id: str,
    role_ar: str,
    role_en: str,
    autonomy: AutonomyLevel,
    risk: RiskLevel,
    *,
    allowed_tools: list[str] | None = None,
    forbidden_tools: list[str] | None = None,
    allowed_inputs: list[str] | None = None,
    allowed_outputs: list[str] | None = None,
    default_action_mode: str = "draft_only",
    requires_approval: bool = True,
    cost_budget_usd: float = 0.50,
    evidence_required: bool = True,
) -> AgentSpec:
    return AgentSpec(
        agent_id=agent_id,
        role_ar=role_ar,
        role_en=role_en,
        allowed_inputs=list(allowed_inputs or ["WorkforceGoal", "prior_outputs"]),
        allowed_outputs=list(allowed_outputs or ["AgentTask"]),
        allowed_tools=list(allowed_tools or []),
        forbidden_tools=list(forbidden_tools or []),
        autonomy_level=autonomy,
        default_action_mode=default_action_mode,
        risk_level=risk,
        requires_approval=requires_approval,
        cost_budget_usd=cost_budget_usd,
        evidence_required=evidence_required,
    )


_AGENTS: tuple[AgentSpec, ...] = (
    _spec(
        "OrchestratorAgent",
        "منسّق سير العمل",
        "Workforce orchestrator",
        AutonomyLevel.ANALYZE_ONLY,
        RiskLevel.LOW,
        allowed_tools=["task_router", "language_router"],
        default_action_mode="analyze_only",
    ),
    _spec(
        "CompanyBrainAgent",
        "دماغ الشركة",
        "Company brain composer",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.LOW,
        allowed_tools=["company_brain_v6.build_company_brain_v6"],
    ),
    _spec(
        "MarketRadarAgent",
        "رادار السوق",
        "Market radar analyst",
        AutonomyLevel.ANALYZE_ONLY,
        RiskLevel.LOW,
        allowed_tools=["self_growth_os.search_radar", "self_growth_os.geo_aio_radar"],
        default_action_mode="analyze_only",
    ),
    _spec(
        "SalesStrategistAgent",
        "استراتيجي المبيعات",
        "Sales strategist",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.MEDIUM,
        allowed_tools=["company_brain_v6.recommend_service"],
    ),
    _spec(
        "SaudiCopyAgent",
        "محرّر النصوص العربيّة",
        "Saudi copy editor",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.MEDIUM,
        allowed_tools=["draft_arabic_copy"],
        forbidden_tools=list(SAUDI_COPY_FORBIDDEN),
    ),
    _spec(
        "PartnershipAgent",
        "وكيل الشراكات",
        "Partnership scout",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.MEDIUM,
        allowed_tools=["partner_distribution_radar"],
    ),
    _spec(
        "DeliveryAgent",
        "وكيل التسليم",
        "Delivery planner",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.LOW,
        allowed_tools=["delivery_factory.build_delivery_plan"],
    ),
    _spec(
        "ProofAgent",
        "وكيل البرهان",
        "Proof analyst",
        AutonomyLevel.ANALYZE_ONLY,
        RiskLevel.LOW,
        allowed_tools=["proof_ledger.export_redacted"],
        default_action_mode="analyze_only",
    ),
    _spec(
        "ComplianceGuardAgent",
        "حارس الامتثال",
        "Compliance guard (veto)",
        AutonomyLevel.APPROVAL_REQUIRED,
        RiskLevel.LOW,
        allowed_tools=["workforce_policy.apply_policy"],
        default_action_mode="approval_required",
    ),
    _spec(
        "ExecutiveBriefAgent",
        "وكيل الموجز التنفيذي",
        "Executive brief composer",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.LOW,
        allowed_tools=["executive_reporting.build_weekly_report"],
    ),
    _spec(
        "FinanceAgent",
        "وكيل المالية",
        "Finance draft agent",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.MEDIUM,
        allowed_tools=["finance_os.draft_invoice"],
        forbidden_tools=list(FINANCE_FORBIDDEN),
    ),
    _spec(
        "CustomerSuccessAgent",
        "وكيل نجاح العميل",
        "Customer success suggester",
        AutonomyLevel.DRAFT_ONLY,
        RiskLevel.LOW,
        allowed_tools=["customer_loop.next_actions_for_state"],
    ),
)


AGENT_REGISTRY: dict[str, AgentSpec] = {a.agent_id: a for a in _AGENTS}


def list_agents() -> list[AgentSpec]:
    """Return the 12 registered agents in declaration order."""
    return list(_AGENTS)


def get_agent(agent_id: str) -> AgentSpec:
    """Return the spec for ``agent_id``. KeyError if unknown."""
    if agent_id not in AGENT_REGISTRY:
        raise KeyError(f"unknown agent_id: {agent_id}")
    return AGENT_REGISTRY[agent_id]

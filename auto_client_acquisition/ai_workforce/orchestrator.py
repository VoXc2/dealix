"""AI Workforce orchestrator over bounded specialist roles.

Pure local composition. No LLM, no external HTTP. Historical role ids remain
compatibility names only; every task is owned by one of the five canonical
Dealix agents. ComplianceGuardAgent runs last with veto authority.
"""
from __future__ import annotations

from auto_client_acquisition.ai_workforce import (
    agent_contracts,
    cost_guard,
    evidence_writer,
    language_router,
    risk_guard,
    task_router,
    workforce_policy,
)
from auto_client_acquisition.ai_workforce.agent_registry import get_agent
from auto_client_acquisition.ai_workforce.canonical_delegation import (
    CANONICAL_AGENTS,
    SPECIALIST_ROLE_SEMANTICS,
    canonical_owner_for,
)
from auto_client_acquisition.ai_workforce.schemas import (
    AgentTask,
    RiskLevel,
    WorkforceGoal,
    WorkforceRun,
)

CANONICAL_ENTRY_OFFER = "free_mini_diagnostic"

_GUARDRAILS: dict[str, bool] = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "no_autonomous_pricing": True,
    "no_autonomous_payment": True,
    "approval_required_for_external_actions": True,
    "no_self_granted_l5": True,
    "specialist_roles_are_bounded_workloads": True,
    "no_llm_calls": True,
}


def _compliance_veto(tasks: list[AgentTask]) -> list[AgentTask]:
    reviewed: list[AgentTask] = []
    for task in tasks:
        if task.agent_id == "ComplianceGuardAgent":
            reviewed.append(task)
            continue
        reviewed.append(workforce_policy.apply_policy(task))
    return reviewed


def _recommended_service(tasks: list[AgentTask]) -> str:
    """Only the public entry offer may be recommended by this legacy runtime."""
    for task in tasks:
        if task.agent_id == "SalesStrategistAgent" and isinstance(task.output, dict):
            if task.output.get("recommended_service") == CANONICAL_ENTRY_OFFER:
                return CANONICAL_ENTRY_OFFER
    return CANONICAL_ENTRY_OFFER


def _next_best_action(tasks: list[AgentTask], language: str) -> str:
    blocked = [task for task in tasks if task.action_mode == "blocked"]
    if blocked:
        return (
            "راجع المهام المحظورة قبل أي خطوة خارجية."
            if language == "ar"
            else "Review blocked tasks before any external action."
        )
    if language == "ar":
        return (
            "حضّر Free Mini Diagnostic مبنياً على الدليل. لا ترسل خارجياً إلا بعد "
            "إثبات أهلية القناة/العلاقة. إذا تأهلت المشكلة: Qualified Discovery ثم "
            "Customer-Specific Quote؛ لا سعر ثابت ولا فاتورة أو دفع ذاتي."
        )
    return (
        "Prepare an evidence-backed Free Mini Diagnostic. Do not dispatch externally until "
        "channel/relationship eligibility is proven. If the problem qualifies, proceed to "
        "Qualified Discovery then a Customer-Specific Quote; no fixed price, autonomous invoice, or payment."
    )


def run_workforce_goal(goal: WorkforceGoal) -> WorkforceRun:
    """Execute specialist workloads under canonical five-agent ownership."""
    plan = task_router.route_for_goal(goal)
    language = language_router.pick_language(goal)

    prior_outputs: dict[str, dict] = {}
    tasks: list[AgentTask] = []
    evidence: list[str] = []

    for agent_id in plan:
        try:
            task = agent_contracts.run_agent(agent_id, goal, prior_outputs)
        except Exception as exc:
            spec = get_agent(agent_id)
            task = AgentTask(
                agent_id=agent_id,
                canonical_owner=canonical_owner_for(agent_id),
                role_ar=spec.role_ar,
                role_en=spec.role_en,
                action_summary_ar="فشل تنفيذ الدور التخصصي.",
                action_summary_en=f"specialist role execution failed: {type(exc).__name__}",
                output={"error": type(exc).__name__},
                action_mode="blocked",
                approval_status="blocked",
                risk_level=RiskLevel.BLOCKED.value,
                cost_estimate_usd=spec.cost_budget_usd,
            )

        task = workforce_policy.apply_policy(task)
        tasks.append(task)
        evidence.append(evidence_writer.record_evidence(task))
        prior_outputs[agent_id] = dict(task.output)

    tasks = _compliance_veto(tasks)
    risk = risk_guard.summarize_risks(tasks)
    total_cost = sum(cost_guard.estimate_cost(task.agent_id) for task in tasks)
    recommended = _recommended_service(tasks)
    canonical_used = sorted({task.canonical_owner for task in tasks})

    if not set(canonical_used) <= set(CANONICAL_AGENTS):
        raise RuntimeError("specialist workload escaped canonical agent ownership")

    approval_requests = [
        {
            "specialist_role": task.agent_id,
            "canonical_owner": task.canonical_owner,
            "summary_en": task.action_summary_en,
            "approval_status": task.approval_status,
        }
        for task in tasks
        if task.approval_status == "approval_required" and task.action_mode != "blocked"
    ]

    if language == "ar":
        summary_ar = (
            f"تم تشغيل {len(tasks)} دوراً تخصصياً لـ {goal.company_handle} تحت "
            f"{len(canonical_used)} من الوكلاء الخمسة المعتمدين. التنفيذ الخارجي يبقى محكوماً بالصلاحية والدليل."
        )
        summary_en = (
            f"Ran {len(tasks)} specialist roles for {goal.company_handle} under "
            f"{len(canonical_used)} of the five canonical agents; external effects remain authority/evidence gated."
        )
    else:
        summary_en = (
            f"Ran {len(tasks)} specialist roles for {goal.company_handle} under "
            f"{len(canonical_used)} of the five canonical agents; external effects remain authority/evidence gated."
        )
        summary_ar = (
            f"تم تشغيل {len(tasks)} دوراً تخصصياً لـ {goal.company_handle} تحت "
            f"{len(canonical_used)} من الوكلاء الخمسة المعتمدين."
        )

    return WorkforceRun(
        summary_ar=summary_ar,
        summary_en=summary_en,
        assigned_agents=list(plan),
        specialist_roles_used=list(plan),
        canonical_agents_used=canonical_used,
        task_plan=tasks,
        recommended_service=recommended,
        approval_requests=approval_requests,
        blocked_actions=list(risk["blocked_actions"]),
        evidence=evidence,
        next_best_action=_next_best_action(tasks, language),
        cost_estimate_usd=float(total_cost),
        risk_summary={**risk, "specialist_role_semantics": SPECIALIST_ROLE_SEMANTICS},
        guardrails=dict(_GUARDRAILS),
    )

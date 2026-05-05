"""Workforce orchestrator — wires the 12 agents over v5/v6 layers.

Pure local composition. No LLM, no external HTTP. Each agent runs
defensively (errors become blocked tasks) and ComplianceGuardAgent
runs LAST with the power to flip any prior task to blocked.
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
from auto_client_acquisition.ai_workforce.schemas import (
    AgentTask,
    RiskLevel,
    WorkforceGoal,
    WorkforceRun,
)
from auto_client_acquisition.company_brain_v6.service_matcher import (
    CUSTOMER_FACING_BUNDLES,
)


_GUARDRAILS: dict[str, bool] = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "approval_required_for_external_actions": True,
    "no_llm_calls": True,
}


def _compliance_veto(tasks: list[AgentTask]) -> list[AgentTask]:
    """Final sweep — re-apply policy in case anything slipped through.

    The orchestrator already calls ``apply_policy`` per task, but the
    ComplianceGuardAgent runs LAST so we re-iterate to make the veto
    contract explicit. Returns a new list — the originals are not
    mutated.
    """
    reviewed: list[AgentTask] = []
    for t in tasks:
        if t.agent_id == "ComplianceGuardAgent":
            reviewed.append(t)
            continue
        reviewed.append(workforce_policy.apply_policy(t))
    return reviewed


def _recommended_service(tasks: list[AgentTask]) -> str:
    for t in tasks:
        if t.agent_id == "SalesStrategistAgent":
            svc = t.output.get("recommended_service") if isinstance(t.output, dict) else None
            if svc in CUSTOMER_FACING_BUNDLES:
                return svc
    # Fallback to CompanyBrain output.
    for t in tasks:
        if t.agent_id == "CompanyBrainAgent":
            svc = t.output.get("service_recommendation") if isinstance(t.output, dict) else None
            if svc in CUSTOMER_FACING_BUNDLES:
                return svc
    return "growth_starter"


def _next_best_action(tasks: list[AgentTask], language: str) -> str:
    blocked = [t for t in tasks if t.action_mode == "blocked"]
    if blocked:
        if language == "ar":
            return "راجع المهام المحظورة قبل أيّ خطوة خارجيّة."
        return "Review blocked tasks before any external action."
    if language == "ar":
        return "اعتمد المسوّدات يدوياً، ثم أرسل عرض Pilot 499 ريال."
    return "Approve drafts manually, then issue the 499 SAR Pilot offer."


def run_workforce_goal(goal: WorkforceGoal) -> WorkforceRun:
    """Execute a full workforce run for ``goal``.

    Pipeline:
      1. ``task_router.route_for_goal`` chooses the agent order.
      2. Each agent runs via ``agent_contracts.run_agent`` and
         immediately passes through ``workforce_policy.apply_policy``.
      3. ComplianceGuardAgent runs last and re-vetoes.
      4. Risk + cost summaries compose; ``next_best_action`` is
         derived deterministically.
    """
    plan = task_router.route_for_goal(goal)
    language = language_router.pick_language(goal)

    prior_outputs: dict[str, dict] = {}
    tasks: list[AgentTask] = []
    evidence: list[str] = []

    for agent_id in plan:
        try:
            task = agent_contracts.run_agent(agent_id, goal, prior_outputs)
        except Exception as exc:  # noqa: BLE001 — last-resort safety net
            spec = get_agent(agent_id)
            task = AgentTask(
                agent_id=agent_id,
                role_ar=spec.role_ar,
                role_en=spec.role_en,
                action_summary_ar="فشل تنفيذ الوكيل.",
                action_summary_en=f"agent execution failed: {type(exc).__name__}",
                output={"error": type(exc).__name__},
                action_mode="blocked",
                approval_status="blocked",
                risk_level=RiskLevel.BLOCKED.value,
                cost_estimate_usd=spec.cost_budget_usd,
            )

        # Per-agent policy sweep BEFORE recording into prior_outputs so a
        # blocked output doesn't poison the chain.
        task = workforce_policy.apply_policy(task)
        tasks.append(task)
        evidence.append(evidence_writer.record_evidence(task))
        prior_outputs[agent_id] = dict(task.output)

    # Final compliance veto pass (ComplianceGuardAgent ran last).
    tasks = _compliance_veto(tasks)

    risk = risk_guard.summarize_risks(tasks)
    total_cost = sum(cost_guard.estimate_cost(t.agent_id) for t in tasks)
    recommended = _recommended_service(tasks)

    approval_requests = [
        {
            "agent_id": t.agent_id,
            "summary_en": t.action_summary_en,
            "approval_status": t.approval_status,
        }
        for t in tasks
        if t.approval_status == "approval_required" and t.action_mode != "blocked"
    ]
    blocked_actions = list(risk["blocked_actions"])

    if language == "ar":
        summary_ar = (
            f"تم تشغيل {len(tasks)} وكيل لـ {goal.company_handle}. "
            "كل المخرجات مسوّدات تحتاج موافقة المؤسس."
        )
        summary_en = (
            f"Ran {len(tasks)} agents for {goal.company_handle}. "
            "All outputs are drafts pending founder approval."
        )
    else:
        summary_en = (
            f"Ran {len(tasks)} agents for {goal.company_handle}. "
            "All outputs are drafts pending founder approval."
        )
        summary_ar = (
            f"تم تشغيل {len(tasks)} وكيل لـ {goal.company_handle}. "
            "جميع المخرجات مسوّدات بانتظار موافقة المؤسس."
        )

    return WorkforceRun(
        summary_ar=summary_ar,
        summary_en=summary_en,
        assigned_agents=list(plan),
        task_plan=tasks,
        recommended_service=recommended,
        approval_requests=approval_requests,
        blocked_actions=blocked_actions,
        evidence=evidence,
        next_best_action=_next_best_action(tasks, language),
        cost_estimate_usd=float(total_cost),
        risk_summary=risk,
        guardrails=dict(_GUARDRAILS),
    )

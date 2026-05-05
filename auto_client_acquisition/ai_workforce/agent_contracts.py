"""Per-agent dispatcher.

Each agent body is a small pure function that wraps an existing v5/v6
module. All bodies are wrapped in try/except — a single failure in an
upstream layer becomes a blocked AgentTask, never a crash.

No LLM, no external HTTP, no live send.
"""
from __future__ import annotations

from typing import Any, Callable

from auto_client_acquisition.ai_workforce.agent_registry import get_agent
from auto_client_acquisition.ai_workforce.schemas import (
    AgentSpec,
    AgentTask,
    RiskLevel,
    WorkforceGoal,
)


def _make_task(
    spec: AgentSpec,
    *,
    action_mode: str,
    summary_ar: str,
    summary_en: str,
    output: dict[str, Any],
    risk: RiskLevel | str,
    approval_status: str = "approval_required",
    evidence_pointers: list[str] | None = None,
) -> AgentTask:
    risk_value = risk.value if isinstance(risk, RiskLevel) else str(risk)
    return AgentTask(
        agent_id=spec.agent_id,
        role_ar=spec.role_ar,
        role_en=spec.role_en,
        action_summary_ar=summary_ar,
        action_summary_en=summary_en,
        output=output,
        action_mode=action_mode,
        approval_status=approval_status,
        risk_level=risk_value,
        cost_estimate_usd=spec.cost_budget_usd,
        evidence_pointers=list(evidence_pointers or []),
    )


def _blocked(spec: AgentSpec, reason: str) -> AgentTask:
    return _make_task(
        spec,
        action_mode="blocked",
        summary_ar=f"تم حظر الوكيل: {reason}",
        summary_en=f"agent blocked: {reason}",
        output={"error": reason},
        risk=RiskLevel.BLOCKED,
        approval_status="blocked",
    )


# ─── Individual agent bodies ─────────────────────────────────────


def _company_brain(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.company_brain_v6 import (
        BuildRequest,
        build_company_brain_v6,
    )

    req = BuildRequest(
        company_handle=goal.company_handle,
        sector="b2b_services",
        region="ksa",
        allowed_channels=list(goal.approved_channels),
        blocked_channels=list(goal.blocked_channels),
        language_preference=(
            goal.language_preference if goal.language_preference != "bilingual" else "ar"
        ),
        growth_goal=goal.desired_outcome or goal.goal_en or goal.goal_ar,
    )
    brain = build_company_brain_v6(req)
    return {
        "company_handle": brain.company_handle,
        "sector": brain.sector,
        "region": brain.region,
        "service_recommendation": brain.service_recommendation,
        "allowed_channels": list(brain.allowed_channels),
        "blocked_channels": list(brain.blocked_channels),
        "next_best_action": brain.next_best_action,
    }


def _market_radar(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import geo_aio_radar, search_radar

    radar = search_radar.build_search_radar(top_n=5)
    geo = geo_aio_radar.audit_all()
    return {
        "search_radar_top_n": radar.get("top_n") if isinstance(radar, dict) else None,
        "search_radar_keywords": (
            len(radar.get("keywords", [])) if isinstance(radar, dict) else 0
        ),
        "geo_aio_pages_audited": (
            len(geo.get("pages", [])) if isinstance(geo, dict) else 0
        ),
    }


def _sales_strategist(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    brain_out = prior.get("CompanyBrainAgent", {})
    recommended = brain_out.get("service_recommendation") or "growth_starter"
    return {
        "recommended_service": recommended,
        "rationale_ar": "اختير المسار بناءً على القطاع والقنوات المعتمدة.",
        "rationale_en": "Recommendation based on sector + approved channels.",
        "next_step": "share_diagnostic_then_pilot_offer",
    }


def _saudi_copy(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    company = goal.company_handle
    return {
        "subject_ar": f"عرض موجز لـ {company}",
        "subject_en": f"Brief offer for {company}",
        "body_ar": (
            "شكراً على وقتك. نقترح خطوة تشخيصيّة قصيرة قبل أيّ التزام، "
            "بدون أيّ إرسال خارجي حتى توافق."
        ),
        "body_en": (
            "Thanks for your time. We suggest a short diagnostic step "
            "before any commitment — no external sends until you approve."
        ),
        "channel_hint": "warm_intro_only",
    }


def _partnership(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "partner_categories": [
            "agency", "consulting", "saas_complement", "trainer_network",
        ],
        "fit_score_method": "manual_review_required",
        "warm_intro_required": True,
    }


def _delivery(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.delivery_factory import (
        build_delivery_plan,
        list_available_services,
    )

    services = list_available_services()
    target = "growth_starter_pilot" if "growth_starter_pilot" in services else (
        services[0] if services else ""
    )
    if not target:
        return {"service_id": "", "available": list(services)}
    plan = build_delivery_plan(target)
    return {
        "service_id": target,
        "available_services_count": len(services),
        "approval_required": getattr(plan, "approval_required", True),
    }


def _proof(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.proof_ledger import export_redacted

    pack = export_redacted(limit=10)
    return {
        "events_returned": pack.get("total_returned", 0),
        "schema_version": pack.get("schema_version", 1),
    }


def _compliance_guard(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    # The guard's body is a pass-through summary; the actual veto runs
    # in the orchestrator + workforce_policy after every task is built.
    return {
        "policy": "no_live_send_no_scrape_no_cold_outreach",
        "vetoed_tools": [
            "cold_whatsapp", "linkedin_automation", "scrape_web",
            "send_email_live", "send_whatsapp_live", "charge_payment_live",
        ],
        "language_preference": goal.language_preference,
    }


def _executive_brief(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.executive_reporting import build_weekly_report

    report = build_weekly_report()
    return {
        "week_label": getattr(report, "week_label", ""),
        "decisions_count": len(getattr(report, "decisions", []) or []),
        "risks_count": len(getattr(report, "risks", []) or []),
    }


def _finance(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.finance_os import draft_invoice

    draft = draft_invoice(
        tier_id="growth_starter_pilot",
        customer_email="founder+pending@example.com",
        customer_handle=goal.company_handle,
    )
    return {
        "tier_id": draft.tier_id,
        "amount_sar": draft.amount_sar,
        "approval_status": draft.approval_status,
        "live_charge_enabled": False,
    }


def _customer_success(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.customer_loop import (
        JourneyState,
        next_actions_for_state,
    )

    suggestions = next_actions_for_state(JourneyState.LEAD_INTAKE)
    return {
        "state": suggestions.get("state"),
        "next_actions_count_ar": len(suggestions.get("next_actions_ar", [])),
        "next_actions_count_en": len(suggestions.get("next_actions_en", [])),
        "approval_required": suggestions.get("approval_required", True),
    }


# Map agent_id -> (body_fn, default_summary_ar, default_summary_en, action_mode)
_BODIES: dict[str, tuple[Callable, str, str, str]] = {
    "OrchestratorAgent": (
        lambda goal, prior: {
            "assigned_count": len(prior),
            "language_preference": goal.language_preference,
        },
        "تم تنسيق فريق العمل.",
        "Workforce orchestration prepared.",
        "analyze_only",
    ),
    "CompanyBrainAgent": (
        _company_brain,
        "تم تركيب دماغ الشركة.",
        "Company brain composed.",
        "draft_only",
    ),
    "MarketRadarAgent": (
        _market_radar,
        "تم تحليل السوق محلياً.",
        "Market radar analyzed locally.",
        "analyze_only",
    ),
    "SalesStrategistAgent": (
        _sales_strategist,
        "تم اقتراح الخطّة البيعية.",
        "Sales strategy drafted.",
        "draft_only",
    ),
    "SaudiCopyAgent": (
        _saudi_copy,
        "تمّت كتابة مسوّدات النصوص العربية.",
        "Arabic-primary copy drafts ready.",
        "draft_only",
    ),
    "PartnershipAgent": (
        _partnership,
        "تم تحضير قائمة فئات الشراكة.",
        "Partner-category map drafted.",
        "draft_only",
    ),
    "DeliveryAgent": (
        _delivery,
        "تم بناء خطّة التسليم.",
        "Delivery plan drafted.",
        "draft_only",
    ),
    "ProofAgent": (
        _proof,
        "تم تحضير ملخّص البرهان المخفّف.",
        "Redacted proof summary prepared.",
        "analyze_only",
    ),
    "ComplianceGuardAgent": (
        _compliance_guard,
        "حارس الامتثال جاهز للفيتو.",
        "ComplianceGuard active — veto ready.",
        "approval_required",
    ),
    "ExecutiveBriefAgent": (
        _executive_brief,
        "تم تحضير الموجز التنفيذي الأسبوعي.",
        "Weekly executive brief drafted.",
        "draft_only",
    ),
    "FinanceAgent": (
        _finance,
        "تمّ تحضير مسوّدة فاتورة 499 ريال (Pilot).",
        "499 SAR Pilot invoice draft prepared.",
        "draft_only",
    ),
    "CustomerSuccessAgent": (
        _customer_success,
        "تم اقتراح خطوات نجاح العميل.",
        "Customer success next-steps drafted.",
        "draft_only",
    ),
}


def run_agent(
    agent_id: str,
    goal: WorkforceGoal,
    prior_outputs: dict[str, Any],
) -> AgentTask:
    """Dispatch to the agent body for ``agent_id`` defensively.

    Any exception is captured and the task returns blocked so the
    orchestrator can complete the run instead of crashing.
    """
    spec = get_agent(agent_id)

    body = _BODIES.get(agent_id)
    if body is None:
        return _blocked(spec, f"no body registered for {agent_id}")

    fn, summary_ar, summary_en, action_mode = body

    try:
        output = fn(goal, prior_outputs) or {}
    except Exception as exc:  # noqa: BLE001
        return _blocked(spec, f"{agent_id}_failed: {type(exc).__name__}")

    if not isinstance(output, dict):
        return _blocked(spec, f"{agent_id}_bad_output_type")

    return _make_task(
        spec,
        action_mode=action_mode,
        summary_ar=summary_ar,
        summary_en=summary_en,
        output=output,
        risk=spec.risk_level,
        evidence_pointers=[f"agent:{agent_id}:{goal.company_handle}"],
    )

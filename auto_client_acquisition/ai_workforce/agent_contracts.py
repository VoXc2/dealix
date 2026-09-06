"""Specialist-role dispatcher for the legacy AI Workforce layer.

Each historical role remains a small pure function that wraps an existing v5/v6
module. Every emitted task is delegated to one of Dealix's five canonical agents.
A single upstream failure becomes a blocked AgentTask, never a crash.

No LLM, no external HTTP, no live send, no autonomous pricing or payment.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from auto_client_acquisition.ai_workforce.agent_registry import get_agent
from auto_client_acquisition.ai_workforce.canonical_delegation import canonical_owner_for
from auto_client_acquisition.ai_workforce.schemas import (
    AgentSpec,
    AgentTask,
    RiskLevel,
    WorkforceGoal,
)

CANONICAL_ENTRY_OFFER = "free_mini_diagnostic"
CANONICAL_PAID_OFFER = "revenue_command_pilot_30d"
CANONICAL_PAID_PATH = (
    "qualified_discovery -> customer_specific_quote -> revenue_command_pilot_30d -> "
    "verified_payment -> delivery -> customer_validated_proof -> stop_expand_redesign"
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
        canonical_owner=canonical_owner_for(spec.agent_id),
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
        summary_ar=f"تم حظر الدور التخصصي: {reason}",
        summary_en=f"specialist role blocked: {reason}",
        output={"error": reason},
        risk=RiskLevel.BLOCKED,
        approval_status="blocked",
    )


# ─── Individual specialist-role bodies ───────────────────────────


def _company_brain(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.company_brain_v6 import BuildRequest, build_company_brain_v6

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
        "service_recommendation": CANONICAL_ENTRY_OFFER,
        "legacy_service_recommendation_observed": getattr(brain, "service_recommendation", None),
        "allowed_channels": list(brain.allowed_channels),
        "blocked_channels": list(brain.blocked_channels),
        "next_best_action": "prepare_free_mini_diagnostic",
    }


def _market_radar(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import geo_aio_radar, search_radar

    radar = search_radar.build_search_radar(top_n=5)
    geo = geo_aio_radar.audit_all()
    return {
        "search_radar_top_n": radar.get("top_n") if isinstance(radar, dict) else None,
        "search_radar_keywords": len(radar.get("keywords", [])) if isinstance(radar, dict) else 0,
        "geo_aio_pages_audited": len(geo.get("pages", [])) if isinstance(geo, dict) else 0,
        "promotion_rule": "public_signal_is_research_only_until_relationship_or_consent_evidence",
    }


def _sales_strategist(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "recommended_service": CANONICAL_ENTRY_OFFER,
        "paid_offer": CANONICAL_PAID_OFFER,
        "paid_path": CANONICAL_PAID_PATH,
        "rationale_ar": "ابدأ بتشخيص مجاني مبني على الدليل، ثم Discovery، ثم عرض سعر خاص بالعميل فقط إذا تأهلت المشكلة.",
        "rationale_en": "Start with an evidence-backed Free Mini Diagnostic, then discovery and a customer-specific quote only after qualification.",
        "next_step": "prepare_free_mini_diagnostic_then_qualified_discovery",
        "public_fixed_price": False,
        "public_checkout": False,
    }


def _saudi_copy(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    company = goal.company_handle
    return {
        "subject_ar": f"تشخيص موجز لـ {company}",
        "subject_en": f"Brief diagnostic for {company}",
        "body_ar": (
            "بناءً على السياق المتاح، نقدر نجهز تشخيصاً أولياً قصيراً يوضح أين توجد فجوة قرار أو إيراد أو إثبات. "
            "أي تواصل خارجي يبقى مرتبطاً بأهلية القناة والعلاقة والموافقة المناسبة."
        ),
        "body_en": (
            "Based on the available context, we can prepare a short initial diagnostic showing the clearest decision, revenue, or proof gap. "
            "Any external communication remains gated by channel eligibility, relationship state, and required authorization."
        ),
        "channel_hint": "warm_or_permissioned_only",
    }


def _partnership(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "partner_categories": ["agency", "consulting", "saas_complement", "trainer_network"],
        "fit_score_method": "evidence_backed_review",
        "warm_intro_or_permission_required": True,
    }


def _delivery(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "service_id": CANONICAL_PAID_OFFER,
        "delivery_owner": "dealix-delivery",
        "release_status": "blocked_until_customer_specific_quote_and_verified_payment_or_start_authority",
        "approval_required": True,
        "required_before_release": [
            "qualified_discovery",
            "customer_specific_quote",
            "accepted_scope",
            "verified_payment_or_explicit_free_delivery_authority",
            "acceptance_criteria",
            "data_boundary",
        ],
        "public_fixed_price": False,
    }


def _proof(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.proof_ledger import export_redacted

    pack = export_redacted(limit=10)
    return {
        "events_returned": pack.get("total_returned", 0),
        "schema_version": pack.get("schema_version", 1),
        "customer_validated_proof_required_for_commercial_claim": True,
    }


def _compliance_guard(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy": "no_live_send_no_scrape_no_cold_outreach_no_self_granted_l5",
        "vetoed_tools": [
            "cold_whatsapp",
            "linkedin_automation",
            "scrape_web",
            "send_email_live",
            "send_whatsapp_live",
            "charge_payment_live",
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
        "founder_surface": ["cash", "decisions", "risks", "approvals", "next_action"],
    }


def _finance(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "finance_owner": "dealix-engineer",
        "quote_required": True,
        "customer_specific_quote_only": True,
        "amount_sar": None,
        "invoice_draft_status": "blocked_until_approved_customer_specific_quote",
        "live_charge_enabled": False,
        "payment_execution_enabled": False,
        "payment_verification_required": True,
        "delivery_release_requires_verified_payment_or_explicit_free_authority": True,
    }


def _customer_success(goal: WorkforceGoal, prior: dict[str, Any]) -> dict[str, Any]:
    from auto_client_acquisition.customer_loop import JourneyState, next_actions_for_state

    suggestions = next_actions_for_state(JourneyState.LEAD_INTAKE)
    return {
        "state": suggestions.get("state"),
        "next_actions_count_ar": len(suggestions.get("next_actions_ar", [])),
        "next_actions_count_en": len(suggestions.get("next_actions_en", [])),
        "approval_required": suggestions.get("approval_required", True),
        "canonical_owner": "dealix-delivery",
    }


_BODIES: dict[str, tuple[Callable, str, str, str]] = {
    "OrchestratorAgent": (
        lambda goal, prior: {"specialist_outputs_available": len(prior), "language_preference": goal.language_preference},
        "تم تنسيق الأعمال التخصصية تحت الوكلاء الخمسة.",
        "Specialist workloads coordinated under the five canonical agents.",
        "analyze_only",
    ),
    "CompanyBrainAgent": (_company_brain, "تم تركيب سياق الشركة.", "Company context composed.", "draft_only"),
    "MarketRadarAgent": (_market_radar, "تم تحليل السوق محلياً.", "Market radar analyzed locally.", "analyze_only"),
    "SalesStrategistAgent": (_sales_strategist, "تم اقتراح المسار التجاري المعتمد.", "Canonical commercial path drafted.", "draft_only"),
    "SaudiCopyAgent": (_saudi_copy, "تمّت كتابة مسودات طبيعية ومحكومة.", "Natural governed copy drafts ready.", "draft_only"),
    "PartnershipAgent": (_partnership, "تم تحضير خريطة الشراكات.", "Partner-category map drafted.", "draft_only"),
    "DeliveryAgent": (_delivery, "تم تحضير خطة تسليم محكومة بالإثبات والدفع.", "Proof/payment-gated delivery plan prepared.", "draft_only"),
    "ProofAgent": (_proof, "تم تحضير ملخص البرهان المخفف.", "Redacted proof summary prepared.", "analyze_only"),
    "ComplianceGuardAgent": (_compliance_guard, "حارس الامتثال جاهز للفيتو.", "Compliance guard active — veto ready.", "approval_required"),
    "ExecutiveBriefAgent": (_executive_brief, "تم تحضير الموجز التنفيذي.", "Executive brief drafted.", "draft_only"),
    "FinanceAgent": (_finance, "تم تحضير بوابة مالية بدون سعر أو فاتورة ذاتية.", "Finance gate prepared without autonomous pricing or invoicing.", "analyze_only"),
    "CustomerSuccessAgent": (_customer_success, "تم اقتراح خطوات نجاح العميل.", "Customer-success next steps drafted.", "draft_only"),
}


def run_agent(agent_id: str, goal: WorkforceGoal, prior_outputs: dict[str, Any]) -> AgentTask:
    """Dispatch a bounded specialist role defensively."""
    spec = get_agent(agent_id)
    body = _BODIES.get(agent_id)
    if body is None:
        return _blocked(spec, f"no body registered for {agent_id}")

    fn, summary_ar, summary_en, action_mode = body
    try:
        output = fn(goal, prior_outputs) or {}
    except Exception as exc:
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
        evidence_pointers=[f"specialist_role:{agent_id}:{goal.company_handle}"],
    )

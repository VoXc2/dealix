"""Read-only daily command center — composes existing subsystems (no LLM, no external HTTP)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.delivery_factory import list_available_services
from auto_client_acquisition.personal_operator import build_daily_brief, default_sami_profile, suggest_opportunities
from auto_client_acquisition.proof_ledger import get_default_ledger
from auto_client_acquisition.v3.agents import agent_catalog
from auto_client_acquisition.v3.compliance_os import ContactPolicyInput, assess_contactability
from auto_client_acquisition.v3.market_radar import demo_signals, rank_opportunities
from auto_client_acquisition.v3.memory import demo_memory
from auto_client_acquisition.v3.revenue_science import demo_forecast


def _command_center_core() -> dict[str, Any]:
    """Same composition as GET /api/v1/v3/command-center/snapshot (deterministic demo)."""
    signals = demo_signals()
    mem = demo_memory()
    return {
        "today_decisions": [
            "Approve 12 safe WhatsApp follow-ups from warm inbound replies.",
            "Pause cold WhatsApp campaign: compliance risk blocked.",
            "Focus this week on clinics in Riyadh and real estate in Jeddah.",
        ],
        "agents": agent_catalog(),
        "market_radar": rank_opportunities(signals, limit=3),
        "forecast": demo_forecast(),
        "compliance": assess_contactability(ContactPolicyInput(channel="email", has_prior_relationship=True)),
        "memory": mem.projection("clinic_riyadh_01"),
    }


def build_daily_command_center() -> dict[str, Any]:
    """Single JSON for founder morning loop. Always safe to call; no customer PII required."""
    profile = default_sami_profile()
    brief = build_daily_brief(profile)
    opps = suggest_opportunities(profile)
    cc = _command_center_core()

    warm_intro_slots = []
    for item in opps[:3]:
        warm_intro_slots.append(
            {
                "id": item.id,
                "title": item.title,
                "segment_hint": item.opportunity_type.value,
                "recommended_action": item.recommended_action,
            }
        )

    ledger = get_default_ledger()
    try:
        recent = ledger.list_events(limit=5)
        proof_summary = {
            "recent_events_count": len(recent),
            "sample": [e.model_dump(mode="json") for e in recent[:3]],
        }
    except Exception as exc:  # noqa: BLE001
        proof_summary = {"recent_events_count": 0, "error": str(exc), "sample": []}

    growth_queue = {
        "module": "growth_os",
        "status": "GET /api/v1/growth-os/status",
        "delegate": "GET /api/v1/growth-v10/status",
    }
    sales_queue = {
        "module": "sales_os",
        "status": "GET /api/v1/sales-os/status",
        "crm": "POST /api/v1/crm-v10/score-lead",
    }
    support_queue = {
        "module": "customer_inbox_v10",
        "guardrails": {
            "no_auto_send_external": True,
            "no_cold_whatsapp": True,
            "manual_linkedin_only": True,
            "approval_required_for_external_actions": True,
        },
    }
    delivery_queue = {
        "module": "delivery_factory",
        "services_total": len(list_available_services()),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
        },
    }
    cs_queue = {
        "module": "customer_success_os",
        "status": "GET /api/v1/customer-success/customer-success-os/status",
        "at_risk": "GET /api/v1/customer-success/at-risk",
    }
    partner_queue = {
        "module": "partnership_os",
        "status": "GET /api/v1/partnership-os/status",
        "fit_score": "POST /api/v1/partnership-os/fit-score",
        "note": "Partner motions stay draft-only until paid pilot evidence (see docs/V12_1_TRIGGER_RULES.md).",
    }

    hard_gates = {
        "NO_LIVE_SEND": True,
        "NO_LIVE_CHARGE": True,
        "NO_COLD_WHATSAPP": True,
        "NO_LINKEDIN_AUTOMATION": True,
        "NO_SCRAPING": True,
        "NO_FAKE_PROOF": True,
    }

    blocked_actions = [
        "live_whatsapp_outbound",
        "gmail_live_send",
        "linkedin_automation",
        "moyasar_live_charge",
        "web_scraping_for_leads",
    ]

    degraded_sections: list[str] = []
    if proof_summary.get("error"):
        degraded_sections.append("proof_ledger:list_events")

    top = list(brief.top_decisions)[:3]
    while len(top) < 3:
        top.append("راجع قائمة الموافقات وحدّد مخرجاً واحداً قابلاً للتسليم اليوم.")

    next_best_actions = [
        "GET /api/v1/approvals/pending — راجع طابور الموافقات.",
        "GET /api/v1/personal-operator/daily-brief — الملخص التفصيلي.",
        "python scripts/dealix_diagnostic.py — تشخيص عميل (بدون إرسال خارجي).",
    ]

    revenue_execution_next_step = (
        "شغّل bash scripts/revenue_execution_verify.sh ثم حدّث docs/POST_V12_REDEPLOY_VERDICT.md بعد أي نشر."
    )

    executive_summary = {
        "greeting": brief.greeting,
        "risk_count": len(brief.risks),
        "launch_readiness_keys": list((brief.launch_readiness or {}).keys())[:8],
    }

    compliance_alerts = []
    if isinstance(cc.get("compliance"), dict):
        risk = cc["compliance"].get("risk_level") or cc["compliance"].get("overall_risk")
        if risk:
            compliance_alerts.append({"source": "v3_compliance_sample", "level": str(risk)})

    return {
        "schema_version": 1,
        "module": "revenue_execution_daily_command_center",
        "today_top_3_decisions": top,
        "growth_queue": growth_queue,
        "sales_queue": sales_queue,
        "support_queue": support_queue,
        "delivery_queue": delivery_queue,
        "cs_queue": cs_queue,
        "partner_queue": partner_queue,
        "compliance_alerts": compliance_alerts,
        "executive_summary": executive_summary,
        "blocked_actions": blocked_actions,
        "proof_summary": proof_summary,
        "next_best_actions": next_best_actions,
        "hard_gates": hard_gates,
        "degraded_sections": degraded_sections,
        "revenue_execution_next_step": revenue_execution_next_step,
        "warm_intro_slots": warm_intro_slots,
        "command_center_snapshot": cc,
        "personal_operator_brief": brief.to_dict(),
    }

"""Founder Beast Command Center — read-only composer over V12.5 layers."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter

from auto_client_acquisition.founder_v10.cache import cached_dashboard_payload

router = APIRouter(prefix="/api/v1/founder", tags=["founder-beast-cc"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_whatsapp": True,
    "no_linkedin_automation": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "no_fake_revenue": True,
    "no_unapproved_testimonial": True,
}


def _safe(fn: Callable[[], Any], *, degraded: list[str], section: str) -> Any:
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001
        degraded.append(section)
        return {
            "_error": True,
            "_section": section,
            "_type": type(exc).__name__,
            "_message": str(exc)[:200],
        }


def _compose_payload() -> dict[str, Any]:
    degraded: list[str] = []

    def _growth_today() -> dict[str, Any]:
        from auto_client_acquisition.growth_beast import weekly_summary
        from auto_client_acquisition.growth_beast.market_radar import evaluate_signals

        eval_sig = evaluate_signals([])
        summ = weekly_summary(signals=eval_sig)
        return {"evaluation": eval_sig, "weekly_summary": summ}

    growth = _safe(_growth_today, degraded=degraded, section="growth_beast_aggregate")

    def _today_top_3() -> list[str]:
        return [
            "agency_with_no_proof",
            "b2b_with_weak_followup",
            "consulting_with_offer_clarity_gap",
        ]

    top_3 = _safe(_today_top_3, degraded=degraded, section="today_top_3_decisions")

    def _revenue_truth() -> dict[str, Any]:
        from auto_client_acquisition.revenue_pipeline import snapshot_revenue_truth
        from auto_client_acquisition.revenue_pipeline.pipeline import (
            get_default_pipeline,
        )
        from auto_client_acquisition.revenue_pipeline.revenue_truth import to_dict
        from auto_client_acquisition.runtime_paths import resolve_proof_events_dir

        pipe = get_default_pipeline()
        proof_dir = resolve_proof_events_dir()
        proof_n = 0
        if proof_dir.exists():
            for f in proof_dir.iterdir():
                if not f.is_file():
                    continue
                name_lower = f.name.lower()
                if any(
                    s in name_lower
                    for s in (
                        ".gitkeep",
                        "readme",
                        "schema.example",
                        ".example.",
                        "template",
                    )
                ):
                    continue
                if f.suffix.lower() not in (".json", ".jsonl", ".md"):
                    continue
                proof_n += 1
        snap = snapshot_revenue_truth(
            pipeline_summary=pipe.summary(),
            proof_event_files_count=proof_n,
        )
        return to_dict(snap)

    revenue_truth = _safe(_revenue_truth, degraded=degraded, section="revenue_truth")

    def _finance_brief() -> dict[str, Any]:
        from auto_client_acquisition.revops import build_finance_brief
        from auto_client_acquisition.revops.payment_confirmation import (
            list_confirmations,
        )
        from auto_client_acquisition.revenue_pipeline.pipeline import (
            get_default_pipeline,
        )
        from api.routers import revops as revops_mod

        pipe = get_default_pipeline()
        summary = pipe.summary()
        brief = build_finance_brief(
            pipeline_summary=summary,
            payment_confirmations_count=len(list_confirmations()),
            invoice_drafts_count=sum(
                1
                for inv in revops_mod._INVOICES.values()
                if inv.status == "draft"
            ),
        )
        return {
            "cash_collected_sar": brief.cash_collected_sar,
            "commitments_open_sar": brief.commitments_open_sar,
            "pipeline_value_sar": brief.pipeline_value_sar,
            "paid_pilots_count": brief.paid_pilots_count,
            "committed_count": brief.committed_count,
            "payment_confirmations_count": brief.payment_confirmations_count,
            "invoice_drafts_count": brief.invoice_drafts_count,
            "avg_margin_pct": brief.avg_margin_pct,
            "data_status": brief.data_status,
            "blockers": brief.blockers,
            "next_action_ar": brief.next_action_ar,
            "next_action_en": brief.next_action_en,
        }

    finance_brief = _safe(_finance_brief, degraded=degraded, section="finance_brief")

    def _delivery_status() -> dict[str, Any]:
        from api.routers import delivery_os as d_os

        return {"active_sessions": len(d_os._SESSIONS)}

    delivery_status = _safe(
        _delivery_status, degraded=degraded, section="delivery_status",
    )

    def _support_alerts() -> dict[str, Any]:
        return {"p0_escalations_estimate": 0, "note_ar": "لا تذاكر مرتبطة بعد"}

    support_alerts = _safe(
        _support_alerts, degraded=degraded, section="support_alerts",
    )

    def _proof_summary() -> dict[str, Any]:
        from auto_client_acquisition.proof_to_market import sector_learning_summary
        from auto_client_acquisition.runtime_paths import resolve_proof_events_dir
        import json

        proof_dir = resolve_proof_events_dir()
        events: list[dict] = []
        if proof_dir.exists():
            for f in proof_dir.iterdir():
                if not f.is_file() or f.suffix.lower() != ".json":
                    continue
                if any(
                    s in f.name.lower()
                    for s in (
                        ".gitkeep",
                        "readme",
                        "schema.example",
                        ".example.",
                        "template",
                    )
                ):
                    continue
                try:
                    events.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:  # noqa: BLE001
                    continue
        return sector_learning_summary(events)

    proof_summary = _safe(_proof_summary, degraded=degraded, section="proof_summary")

    def _compliance_alerts() -> dict[str, Any]:
        from auto_client_acquisition.compliance_os_v12.action_policy import (
            evaluate_action,
        )

        blocked_sample = evaluate_action(action_type="cold_whatsapp")
        return {
            "blocked_channel_probe": blocked_sample.verdict == "blocked",
            "action_mode": blocked_sample.action_mode,
        }

    compliance_alerts = _safe(
        _compliance_alerts, degraded=degraded, section="compliance_alerts",
    )

    def _role_command_status() -> dict[str, Any]:
        from api.routers.role_command import _ROLE_PAYLOADS

        return {"roles_supported": list(_ROLE_PAYLOADS.keys())}

    role_command_status = _safe(
        _role_command_status, degraded=degraded, section="role_command_status",
    )

    next_ar, next_en = (
        "ابدأ Phase E — راجع الحقيقة المالية والنمو",
        "Start Phase E — review finance brief and growth snapshot.",
    )
    if isinstance(finance_brief, dict) and finance_brief.get("next_action_ar"):
        next_ar = str(finance_brief["next_action_ar"])
        next_en = str(finance_brief.get("next_action_en") or next_en)
    if isinstance(revenue_truth, dict) and revenue_truth.get("next_action_ar"):
        next_ar = str(revenue_truth["next_action_ar"])

    return {
        "schema_version": 1,
        "experience_layer": "founder_beast_command_center",
        "language_primary": "ar",
        "today_top_3_decisions": top_3 if isinstance(top_3, list) else [],
        "growth_beast_snapshot": growth,
        "revenue_truth": revenue_truth,
        "finance_brief": finance_brief,
        "delivery_status": delivery_status,
        "support_alerts": support_alerts,
        "proof_summary": proof_summary,
        "compliance_alerts": compliance_alerts,
        "role_command_status": role_command_status,
        "next_best_action_ar": next_ar,
        "next_best_action_en": next_en,
        "hard_gates": _HARD_GATES,
        "degraded": bool(degraded),
        "degraded_sections": degraded,
    }


@router.get("/beast-command-center")
async def beast_command_center() -> dict[str, Any]:
    """Single founder-facing snapshot composing Beast layers (cached ~60s)."""
    return cached_dashboard_payload(_compose_payload)

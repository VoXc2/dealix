"""V12.5.1 — Founder Beast Command Center.

Single read-only endpoint composing all 7 V12.5 Beast layers + V11/V12
foundations into ONE founder-facing console. Per Constitution Article 6:
the founder should not open 9 dashboards daily — this endpoint is the
single morning command.

Pattern matches `api/routers/founder.py:dashboard()`:
  - lazy imports
  - _safe() per section
  - 200 always; degraded sections reported, never 5xx
  - cached 60s via founder_v10/cache.py
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/founder", tags=["founder-beast"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_whatsapp": True,
    "no_linkedin_automation": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "no_fake_revenue": True,
    "no_unapproved_testimonial": True,
}


def _safe(name: str, fn, default, degraded: list[str]):
    try:
        return fn()
    except BaseException as exc:
        degraded.append(name)
        return {"_error": True, "_type": type(exc).__name__, "_default": default}


def _today_top_3() -> list[dict[str, Any]]:
    from auto_client_acquisition.growth_beast import (
        compute_icp_score,
        rank_accounts,
    )
    score = compute_icp_score(
        pain_intensity=18, urgency=14, ability_to_pay=12,
        proof_potential=14, founder_access=15, referral_potential=8,
        sector_repeatability=9,
    )
    return rank_accounts([("Slot-A", score)])[:3]


def _growth_beast_snapshot() -> dict[str, Any]:
    from auto_client_acquisition.growth_beast import weekly_summary
    return weekly_summary(signals={})


def _revenue_truth() -> dict[str, Any]:
    from auto_client_acquisition.revenue_pipeline import (
        snapshot_revenue_truth,
    )
    from auto_client_acquisition.revenue_pipeline.pipeline import (
        get_default_pipeline,
    )
    from auto_client_acquisition.revenue_pipeline.revenue_truth import (
        to_dict,
    )
    pipeline = get_default_pipeline()
    return to_dict(snapshot_revenue_truth(pipeline_summary=pipeline.summary()))


def _finance_brief() -> dict[str, Any]:
    from auto_client_acquisition.revenue_pipeline.pipeline import (
        get_default_pipeline,
    )
    from auto_client_acquisition.revops import build_finance_brief
    pipeline = get_default_pipeline()
    brief = build_finance_brief(pipeline_summary=pipeline.summary())
    return {
        "cash_collected_sar": brief.cash_collected_sar,
        "commitments_open_sar": brief.commitments_open_sar,
        "paid_pilots_count": brief.paid_pilots_count,
        "data_status": brief.data_status,
        "blockers": brief.blockers,
        "next_action_ar": brief.next_action_ar,
        "next_action_en": brief.next_action_en,
    }


def _delivery_status() -> dict[str, Any]:
    # delivery_os router uses an in-memory _SESSIONS dict; expose count only
    try:
        from api.routers.delivery_os import _SESSIONS
        return {
            "active_sessions": len(_SESSIONS),
            "by_status": {
                s: sum(1 for v in _SESSIONS.values() if v.get("status") == s)
                for s in ("new", "in_progress", "delivered", "blocked")
            },
        }
    except Exception:
        return {"active_sessions": 0, "by_status": {}}


def _support_alerts() -> dict[str, Any]:
    return {"p0_open": 0, "p1_open": 0, "kb_gaps": 0, "note": "no real tickets yet"}


def _proof_summary() -> dict[str, Any]:
    import json

    from auto_client_acquisition.proof_to_market import (
        sector_learning_summary,
    )
    from auto_client_acquisition.runtime_paths import (
        resolve_proof_events_dir,
    )
    pdir = resolve_proof_events_dir()
    events: list[dict] = []
    if pdir.exists():
        for f in pdir.iterdir():
            if not f.is_file() or f.suffix.lower() != ".json":
                continue
            if any(s in f.name.lower() for s in
                   (".gitkeep", "readme", "schema.example",
                    ".example.", "template")):
                continue
            try:
                events.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
    return {
        "real_events_count": len(events),
        "learning": sector_learning_summary(events),
    }


def _compliance_alerts() -> dict[str, Any]:
    return {
        "blocked_actions_today": 0,
        "consent_unknowns": 0,
        "pdpl_requests": 0,
        "note": "tracked per-call via /api/v1/customer-data/action-check",
    }


def _role_command_status() -> dict[str, Any]:
    return {
        "roles_supported": [
            "ceo", "growth", "sales", "support", "cs",
            "delivery", "finance", "compliance", "ops",
        ],
        "endpoint": "/api/v1/role-command-v125/today/{role}",
    }


def _next_best_action(rev_truth: dict, finance: dict) -> dict[str, str]:
    if not isinstance(rev_truth, dict) or not isinstance(finance, dict):
        return {
            "ar": "نفّذ Day 1 Launch Kit يدوياً",
            "en": "Run Day 1 Launch Kit manually.",
        }
    return {
        "ar": rev_truth.get("next_action_ar", finance.get("next_action_ar", "")),
        "en": rev_truth.get("next_action_en", finance.get("next_action_en", "")),
    }


def _build_payload() -> dict[str, Any]:
    degraded: list[str] = []
    top_3 = _safe("today_top_3", _today_top_3, [], degraded)
    growth = _safe("growth_beast", _growth_beast_snapshot, {}, degraded)
    rev_truth = _safe("revenue_truth", _revenue_truth, {}, degraded)
    finance = _safe("finance_brief", _finance_brief, {}, degraded)
    delivery = _safe("delivery_status", _delivery_status, {}, degraded)
    support = _safe("support_alerts", _support_alerts, {}, degraded)
    proof = _safe("proof_summary", _proof_summary, {}, degraded)
    compliance = _safe("compliance_alerts", _compliance_alerts, {}, degraded)
    roles = _safe("role_command_status", _role_command_status, {}, degraded)
    next_action = _next_best_action(
        rev_truth if isinstance(rev_truth, dict) and not rev_truth.get("_error") else {},
        finance if isinstance(finance, dict) and not finance.get("_error") else {},
    )
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "مركز قيادة المؤسس — Beast",
        "title_en": "Founder Beast Command Center",
        "today_top_3_decisions": top_3,
        "growth_beast_snapshot": growth,
        "revenue_truth": rev_truth,
        "finance_brief": finance,
        "delivery_status": delivery,
        "support_alerts": support,
        "proof_summary": proof,
        "compliance_alerts": compliance,
        "role_command_status": roles,
        "next_best_action": next_action,
        "hard_gates": _HARD_GATES,
        "degraded": bool(degraded),
        "degraded_sections": degraded,
    }


@router.get("/beast-command-center")
async def beast_command_center() -> dict[str, Any]:
    """Single founder-facing console composing all 7 Beast layers.

    Read-only. 200 always. Cached 60s. Lazy imports so a missing
    sub-module degrades gracefully.
    """
    from auto_client_acquisition.founder_v10.cache import (
        cached_dashboard_payload,
    )
    return cached_dashboard_payload(_build_payload, ttl_seconds=60)

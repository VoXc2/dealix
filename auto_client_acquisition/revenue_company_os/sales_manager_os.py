"""
Sales Manager OS — produces today's pipeline snapshot + decisions.

Pure planner; reads minimal projections (deals + sessions + proof events) and
returns the structured brief used by:
  - api/routers/sales_os.py (JSON API)
  - whatsapp_brief_renderer (Arabic WhatsApp text)
  - role_brief_builder (composes the multi-role daily payload)

No I/O. The router fetches the rows.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any


def _stale_followup_threshold_hours() -> int:
    return 48


def _now() -> datetime:
    return datetime.now(timezone.utc)


def pipeline_snapshot(deals, sessions, objection_events) -> dict[str, Any]:
    """Compute the Sales Manager pipeline snapshot from minimal inputs.

    Args:
      deals: iterable of DealRecord-like (.stage, .updated_at, .amount, .currency)
      sessions: iterable of ServiceSessionRecord-like (.status, .service_id, .deadline_at)
      objection_events: iterable of ObjectionEventRecord-like (.objection_class, .outcome)
    """
    deals = list(deals or [])
    sessions = list(sessions or [])
    objections = list(objection_events or [])

    by_stage: Counter[str] = Counter()
    deals_at_risk: list[dict[str, Any]] = []
    followups_due = 0
    for d in deals:
        by_stage[d.stage or "new"] += 1
        last = d.updated_at if d.updated_at else d.created_at
        if last is None:
            continue
        last = last if last.tzinfo else last.replace(tzinfo=timezone.utc)
        age_h = (_now() - last).total_seconds() / 3600.0
        if age_h >= _stale_followup_threshold_hours() and (d.stage or "") not in ("won", "lost", "closed"):
            followups_due += 1
            deals_at_risk.append({
                "deal_id": d.id,
                "lead_id": getattr(d, "lead_id", None),
                "stage": d.stage,
                "stale_hours": round(age_h, 1),
                "amount_sar": float(getattr(d, "amount", 0) or 0),
            })

    # Sort by staleness, take top 5 for the brief
    deals_at_risk.sort(key=lambda x: x["stale_hours"], reverse=True)
    deals_at_risk = deals_at_risk[:5]

    objections_open = sum(1 for o in objections if (o.outcome or "open") == "open")

    pilot_offers_ready = sum(
        1 for s in sessions
        if (s.service_id == "growth_starter" and s.status in ("new", "waiting_inputs"))
    )
    invoice_requests = sum(
        1 for s in sessions
        if s.status in ("ready_to_deliver",) and (s.service_id == "growth_starter")
    )
    meetings_to_book = sum(
        1 for s in sessions if s.status == "needs_approval"
    )

    return {
        "as_of": _now().isoformat(),
        "summary": {
            "deals_total": len(deals),
            "deals_at_risk": len(deals_at_risk),
            "followups_due": followups_due,
            "objections_open": objections_open,
            "meetings_to_book": meetings_to_book,
            "pilot_offers_ready": pilot_offers_ready,
            "invoice_requests": invoice_requests,
        },
        "by_stage": dict(by_stage),
        "deals_at_risk": deals_at_risk,
    }


def top_decisions(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Build the Top-3 decision cards (max 3) for the Sales Manager brief."""
    decisions: list[dict[str, Any]] = []
    summary = snapshot.get("summary") or {}
    deals_at_risk = snapshot.get("deals_at_risk") or []

    if deals_at_risk:
        d = deals_at_risk[0]
        decisions.append({
            "type": "deal_followup",
            "title_ar": "تابع صفقة ركدت",
            "why_now_ar": f"مرّت {d['stale_hours']:.0f} ساعة بدون متابعة (deal {d['deal_id'][:10]}…).",
            "recommended_action_ar": "أرسل follow-up بعرض Pilot 499 لمدة 7 أيام.",
            "risk_level": "high" if d["stale_hours"] >= 96 else "medium",
            "proof_impact": ["followup_created", "deal_risk_reduced"],
            "action_mode": "approval_required",
            "buttons_ar": ["جهّز Follow-up", "اعرض الصفقة", "صعّد"],
        })

    if summary.get("objections_open", 0) > 0:
        decisions.append({
            "type": "negotiation",
            "title_ar": "اعتراض مفتوح يحتاج رد",
            "why_now_ar": "Dealix يحتفظ بـ objection سجل — الرد المُقترَح موجود في النظام.",
            "recommended_action_ar": "افتح الكرت، استخدم الرد المقترح أو عدّل النبرة، ثم اعتمد.",
            "risk_level": "medium",
            "proof_impact": ["objection_classified", "response_drafted"],
            "action_mode": "approval_required",
            "buttons_ar": ["استخدم الرد", "عدّل", "صعّد"],
        })

    if summary.get("pilot_offers_ready", 0) > 0:
        decisions.append({
            "type": "close_plan",
            "title_ar": f"{summary['pilot_offers_ready']} عرض Pilot جاهز للإرسال",
            "why_now_ar": "Sessions في حالة waiting_inputs/new — العميل وافق ضمنياً، ينقص الـ intake.",
            "recommended_action_ar": "أرسل intake form + رابط Moyasar manual + خطة 7 أيام.",
            "risk_level": "low",
            "proof_impact": ["pilot_offer_ready", "payment_link_drafted"],
            "action_mode": "approval_required",
            "buttons_ar": ["جهّز عرض 499", "أرسل intake", "تخطي"],
        })

    return decisions[:3]


def build_brief(deals, sessions, objection_events) -> dict[str, Any]:
    snap = pipeline_snapshot(deals, sessions, objection_events)
    return {
        "role": "sales_manager",
        "brief_type": "daily_sales_brief",
        "date": _now().date().isoformat(),
        "summary": snap["summary"],
        "by_stage": snap["by_stage"],
        "top_decisions": top_decisions(snap),
        "blocked_today_ar": [
            "لا cold WhatsApp",
            "لا live charge",
            "لا خصم بدون policy",
            "لا 'نضمن' أو 'guaranteed'",
        ],
    }

"""Per-section panel builders. Each is best-effort + safe_call-wrapped."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import (
    customer_safe_label,
    safe_call,
)


def _executive_summary_panel(customer_handle: str) -> dict[str, Any]:
    """Headline + 2-3 sentences sourced from executive_pack_v2 if present."""
    def fn():
        from auto_client_acquisition.executive_pack_v2 import build_daily_pack
        pack = build_daily_pack(customer_handle=customer_handle)
        return {
            "headline_ar": pack.executive_summary_ar or "لا تحديثات اليوم",
            "headline_en": pack.executive_summary_en or "No updates today",
            "source": "executive_pack_v2",
        }
    return safe_call(name="executive_summary", fn=fn, fallback={
        "headline_ar": "لا توجد بيانات تنفيذيّة كافية بعد.",
        "headline_en": "Not enough executive data yet.",
        "source": "insufficient_data",
    })


def _full_ops_score_panel() -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.full_ops_radar import compute_full_ops_score
        return compute_full_ops_score()
    return safe_call(name="full_ops_score", fn=fn, fallback={
        "score": 0, "readiness_label": "Internal Only",
        "source": "insufficient_data",
    })


def _today_3_decisions_panel(customer_handle: str) -> list[dict[str, Any]]:
    """Phase 2 — emits 8-field decision cards (signal/why_now/recommended_action/
    risk/impact/owner/action_mode/proof_link)."""
    from auto_client_acquisition.executive_command_center.card_schema import (
        to_card_dict,
    )

    def fn():
        from auto_client_acquisition.approval_center import approval_store
        pending = approval_store.get_default_approval_store().list_pending()
        scoped = [
            ap for ap in pending
            if customer_handle in (ap.proof_impact or "")
            or customer_handle in (ap.summary_ar or "")
        ][:3]
        out: list[dict[str, Any]] = []
        for ap in scoped:
            risk_text = {
                "high": "احتمال عالي للأثر إذا تأخّر القرار.",
                "medium": "أثر متوسّط إذا تأخّر.",
                "low": "أثر محدود.",
            }.get(ap.risk_level or "medium", "—")
            owner = "founder" if (ap.risk_level == "high" or ap.channel == "whatsapp") else "csm_or_founder"
            out.append(to_card_dict(
                signal=f"{ap.action_type or 'pending_action'} على قناة {ap.channel or '—'}",
                why_now=(ap.summary_ar or "")[:120] or "قرار معلّق",
                recommended_action="راجع المسوّدة واعتمد أو ارفض",
                risk=risk_text,
                impact="ينقل المسار إلى الخطوة التالية فور الاعتماد.",
                owner=owner,
                action_mode="approval_required",
                proof_link=ap.proof_impact,
            ))
        return out
    result = safe_call(name="today_3_decisions", fn=fn, fallback=[])
    if isinstance(result, dict) and result.get("degraded"):
        return []
    return result if isinstance(result, list) else []


def _revenue_radar_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.payment_ops.orchestrator import _INDEX
        confirmed = [p for p in _INDEX.values()
                     if p.customer_handle == customer_handle
                     and p.status in ("payment_confirmed", "delivery_kickoff")]
        return {
            "confirmed_payments_count": len(confirmed),
            "confirmed_revenue_sar": sum(p.amount_sar for p in confirmed),
            "is_revenue_real": True,
            "source": "payment_ops",
        }
    return safe_call(name="revenue_radar", fn=fn, fallback={
        "confirmed_payments_count": 0,
        "confirmed_revenue_sar": 0,
        "is_revenue_real": True,
        "source": "insufficient_data",
    })


def _sales_pipeline_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.service_sessions import list_sessions
        sessions = list_sessions(customer_handle=customer_handle, limit=50)
        return {
            "sessions_active": sum(1 for s in sessions if s.status == "active"),
            "sessions_delivered": sum(1 for s in sessions if s.status == "delivered"),
            "sessions_complete": sum(1 for s in sessions if s.status == "complete"),
            "sessions_total": len(sessions),
            "source": "service_sessions",
        }
    return safe_call(name="sales_pipeline", fn=fn, fallback={
        "sessions_total": 0, "source": "insufficient_data",
    })


def _growth_radar_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.market_intelligence.signal_detectors import (
            SIGNAL_TYPES,
        )
        return {
            "signal_types_tracked": len(SIGNAL_TYPES),
            "live_signals": [],
            "note_ar": "تشغيل الـ live signals يحتاج تفعيل مفاتيح API.",
            "note_en": "Live signal ingestion requires API keys.",
            "source": "market_intelligence",
        }
    return safe_call(name="growth_radar", fn=fn, fallback={
        "signal_types_tracked": 0, "source": "insufficient_data",
    })


def _partnership_radar_panel() -> dict[str, Any]:
    def fn():
        # Best-effort: check if partnership_os router exists
        from auto_client_acquisition.integration_upgrade import safe_import
        mod = safe_import("api.routers.partnership_os")
        if mod is None:
            return {"available": False, "source": "insufficient_data"}
        return {"available": True, "source": "partnership_os"}
    return safe_call(name="partnership_radar", fn=fn, fallback={
        "available": False, "source": "insufficient_data",
    })


def _support_inbox_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.support_inbox import (
            find_breached_tickets,
            list_tickets,
        )
        tickets = list_tickets(customer_id=customer_handle, limit=100)
        breached = find_breached_tickets(customer_id=customer_handle)
        return {
            "open_tickets": sum(1 for t in tickets if t.status == "open"),
            "escalated": sum(1 for t in tickets if t.status == "escalated"),
            "sla_breached_count": len(breached),
            "source": "support_inbox",
        }
    return safe_call(name="support_inbox", fn=fn, fallback={
        "open_tickets": 0, "source": "insufficient_data",
    })


def _delivery_operations_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.service_sessions import list_sessions
        sessions = list_sessions(customer_handle=customer_handle, limit=50)
        in_delivery = [s for s in sessions if s.status in ("active", "delivered", "proof_pending")]
        return {
            "in_delivery_count": len(in_delivery),
            "deliverable_count_total": sum(len(s.deliverables) for s in in_delivery),
            "source": "service_sessions",
        }
    return safe_call(name="delivery_operations", fn=fn, fallback={
        "in_delivery_count": 0, "source": "insufficient_data",
    })


def _finance_state_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.payment_ops.orchestrator import _INDEX
        states = [p for p in _INDEX.values() if p.customer_handle == customer_handle]
        by_status: dict[str, int] = {}
        for p in states:
            by_status[p.status] = by_status.get(p.status, 0) + 1
        return {
            "by_status": by_status,
            "total_payments": len(states),
            "source": "payment_ops",
        }
    return safe_call(name="finance_state", fn=fn, fallback={
        "by_status": {}, "source": "insufficient_data",
    })


def _proof_ledger_panel(customer_handle: str) -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.proof_ledger.file_backend import list_events
        events = list_events(customer_handle=customer_handle, limit=200)
        return {
            "proof_events_count": len(events),
            "source": "proof_ledger",
            "is_proof_real": True,  # NO_FAKE_PROOF
        }
    return safe_call(name="proof_ledger", fn=fn, fallback={
        "proof_events_count": 0, "source": "insufficient_data",
    })


def _risks_compliance_panel() -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.full_ops_radar import detect_weaknesses
        ws = detect_weaknesses()
        critical = [w for w in ws if w["severity"] == "critical"]
        high = [w for w in ws if w["severity"] == "high"]
        return {
            "critical_count": len(critical),
            "high_count": len(high),
            "source": "full_ops_radar.weakness_radar",
        }
    return safe_call(name="risks_compliance", fn=fn, fallback={
        "critical_count": 0, "high_count": 0, "source": "insufficient_data",
    })


def _approval_center_panel() -> dict[str, Any]:
    def fn():
        from auto_client_acquisition.approval_center import approval_store
        pending = approval_store.get_default_approval_store().list_pending()
        return {
            "pending_count": len(pending),
            "source": "approval_center",
        }
    return safe_call(name="approval_center", fn=fn, fallback={
        "pending_count": 0, "source": "insufficient_data",
    })


def _whatsapp_decision_preview_panel(customer_handle: str) -> dict[str, Any]:
    """Preview only — never live send. Phase 7 adds the bot itself."""
    return {
        "preview_only": True,
        "would_send_live": False,
        "note_ar": "كل قرار WhatsApp يحتاج موافقة يدويّة قبل الإرسال.",
        "note_en": "Every WhatsApp action requires manual approval before send.",
        "source": "whatsapp_decision_bot (preview-only)",
    }

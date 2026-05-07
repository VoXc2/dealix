"""Brief builder — composes "today's status" answer for admin queries.

Sources:
- executive_pack_v2.build_daily_pack
- approval_center.list_pending
- support_inbox.find_breached_tickets

Returns a bilingual short brief safe to show in WhatsApp internally.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import (
    hide_internal_terms,
    safe_call,
)


def build_brief(*, customer_handle: str | None = None) -> dict[str, Any]:
    """Bilingual brief. Falls back gracefully if any source missing."""
    pack = safe_call(
        name="executive_pack",
        fn=lambda: _daily_pack(customer_handle),
        fallback={"summary_ar": "لا تحديثات اليوم", "summary_en": "No updates today"},
    )
    pending_count = safe_call(
        name="pending_approvals_count",
        fn=lambda: _pending_count(customer_handle),
        fallback=0,
    )
    breached_count = safe_call(
        name="sla_breached_count",
        fn=lambda: _breached_count(customer_handle),
        fallback=0,
    )

    brief_ar = (
        f"ملخّص اليوم: {pack.get('summary_ar', '—')}. "
        f"قرارات معلّقة: {pending_count}. "
        f"تذاكر تجاوزت SLA: {breached_count}."
    )
    brief_en = (
        f"Today's brief: {pack.get('summary_en', '—')}. "
        f"Pending approvals: {pending_count}. "
        f"SLA breaches: {breached_count}."
    )

    return {
        "brief_ar": hide_internal_terms(brief_ar),
        "brief_en": hide_internal_terms(brief_en),
        "pending_approvals_count": pending_count if isinstance(pending_count, int) else 0,
        "sla_breached_count": breached_count if isinstance(breached_count, int) else 0,
    }


def _daily_pack(customer_handle: str | None) -> dict[str, Any]:
    if not customer_handle:
        return {"summary_ar": "اختر عميل لرؤية التحديثات", "summary_en": "Select a customer to see updates"}
    from auto_client_acquisition.executive_pack_v2 import build_daily_pack
    pack = build_daily_pack(customer_handle=customer_handle)
    return {"summary_ar": pack.executive_summary_ar, "summary_en": pack.executive_summary_en}


def _pending_count(customer_handle: str | None) -> int:
    from auto_client_acquisition.approval_center import approval_store
    pending = approval_store.get_default_approval_store().list_pending()
    if customer_handle:
        pending = [
            ap for ap in pending
            if customer_handle in (ap.proof_impact or "")
            or customer_handle in (ap.summary_ar or "")
        ]
    return len(pending)


def _breached_count(customer_handle: str | None) -> int:
    from auto_client_acquisition.support_inbox import find_breached_tickets
    return len(find_breached_tickets(customer_id=customer_handle))

"""next_decisions — surface top 3 decisions across the platform.

Wraps approval_center.list_pending with severity ordering.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call


def top_3_decisions(*, customer_handle: str | None = None) -> list[dict[str, Any]]:
    def fn():
        from auto_client_acquisition.approval_center import approval_store
        pending = approval_store.list_pending()
        if customer_handle:
            pending = [
                ap for ap in pending
                if customer_handle in (ap.proof_impact or "")
                or customer_handle in (ap.summary_ar or "")
            ]
        # Order by risk_level (high → medium → low)
        order = {"high": 0, "medium": 1, "low": 2}
        pending.sort(key=lambda ap: order.get(ap.risk_level or "low", 3))
        return [{
            "approval_id": ap.approval_id,
            "action_type": ap.action_type,
            "channel": ap.channel,
            "risk_level": ap.risk_level,
            "summary_ar": (ap.summary_ar or "")[:120],
            "summary_en": (ap.summary_en or "")[:120],
        } for ap in pending[:3]]
    result = safe_call(name="next_decisions", fn=fn, fallback=[])
    return result if isinstance(result, list) else []

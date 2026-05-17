"""Adapter over the Approval Center.

Reads two real, in-process sources:
  - the channel policy table (approval_center/approval_policy.py)
  - the live ApprovalStore singleton (approval_center/approval_store.py)

The store is always wired in-process, so ``live_stats`` returns OK even
when empty (real zeros, not fabricated data).
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.models import AdapterResult

_EXTERNAL_CHANNELS = {"whatsapp", "linkedin", "phone", "email"}


class ApprovalAdapter(BaseAdapter):
    source = "auto_client_acquisition.approval_center"

    def channel_policy(self) -> AdapterResult:
        try:
            from auto_client_acquisition.approval_center.approval_policy import (
                CHANNEL_POLICY,
            )
        except Exception as exc:  # noqa: BLE001
            return self.error(f"channel policy unavailable: {exc}")
        return self.ok(dict(CHANNEL_POLICY), "approval_policy.CHANNEL_POLICY")

    def live_stats(self) -> AdapterResult:
        """Counts from the live ApprovalStore plus a high-risk auto-send
        scan. ``high_risk_auto_send`` counts requests that are high risk
        AND ``approved_execute`` on an external channel — the doctrine
        violation the Assurance System must catch."""
        try:
            from auto_client_acquisition.approval_center.approval_store import (
                get_default_approval_store,
            )

            store = get_default_approval_store()
            history = store.list_history(limit=500)
        except Exception as exc:  # noqa: BLE001
            return self.error(f"approval store unavailable: {exc}")

        stats: dict[str, Any] = {
            "total": len(history),
            "pending": 0,
            "approved": 0,
            "rejected": 0,
            "blocked": 0,
            "expired": 0,
            "high_risk_auto_send": 0,
        }
        for req in history:
            status = str(getattr(req, "status", "")).lower()
            if status in stats:
                stats[status] += 1
            channel = (getattr(req, "channel", "") or "").lower()
            risk = (getattr(req, "risk_level", "") or "").lower()
            mode = (getattr(req, "action_mode", "") or "").lower()
            if risk == "high" and mode == "approved_execute" and channel in _EXTERNAL_CHANNELS:
                stats["high_risk_auto_send"] += 1
        return self.ok(stats, "ApprovalStore.list_history")

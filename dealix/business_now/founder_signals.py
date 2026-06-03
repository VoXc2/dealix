"""Founder operator signals — shared by business-now and founder dashboard."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def build_operator_signals() -> dict[str, Any]:
    from api.routers.founder_dashboard import (
        _friction_last_7d,
        _leads_waiting,
        _pending_approvals,
    )
    from dealix.commercial_ops.value_plan import build_value_plan_snapshot

    vp = build_value_plan_snapshot(motion_top_n=3)
    fp = vp.get("first_paid_diagnostic") or {}

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "leads_waiting_24h_plus": _leads_waiting(),
        "friction_last_7d": _friction_last_7d(),
        "pending_approvals": _pending_approvals(),
        "value_plan": {
            "first_paid_verdict": fp.get("verdict"),
            "evidence_today": (vp.get("evidence") or {}).get("today_total", 0),
            "proof_packs_week": (vp.get("north_star") or {}).get("proof_packs_week", 0),
            "warnings_ar": (vp.get("warnings_ar") or [])[:5],
            "ops_founder_href": "/ar/ops/founder",
        },
    }

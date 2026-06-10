"""Complete autonomous day plan — no subprocess."""

from __future__ import annotations

from dealix.commercial_ops.autonomous_ops import build_autonomous_ops_status
from dealix.commercial_ops.complete_autonomous_day import build_complete_autonomous_plan


def test_complete_autonomous_plan_dry():
    plan = build_complete_autonomous_plan()
    assert plan.get("research_verdict_ar")
    assert len(plan.get("phases") or []) >= 3
    assert plan.get("policy_ar")


def test_autonomous_status_includes_governed_autopilot():
    blob = build_autonomous_ops_status()
    assert blob.get("governed_autopilot")
    assert "technical_expansion_ready" in blob
    social = (blob.get("expansion") or {}).get("social") or {}
    assert (social.get("posts") or 0) > 0

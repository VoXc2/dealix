"""Unified founder day in-process pipeline."""

from __future__ import annotations

from dealix.commercial_ops.unified_founder_day import run_unified_founder_day


def test_unified_founder_day_quick():
    payload = run_unified_founder_day(
        quick=True,
        top_n=5,
        run_commercial_subprocess=False,
        run_optional_scripts=False,
    )
    assert payload["verdict"] in ("PASS", "DEGRADED")
    assert len(payload.get("phases") or []) >= 3
    assert payload.get("comprehensive_plan")


def test_cockpit_unified_day_import():
    from dealix.commercial_ops.founder_cockpit import run_cockpit_unified_day

    snap = run_cockpit_unified_day(quick=True, top_n=5, run_optional_scripts=False)
    assert snap.get("cockpit_verdict")
    assert snap.get("unified_day_run")

"""Complete autonomous day — fast in-process smoke (no heavy subprocess CLI)."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_complete_autonomous_plan_module() -> None:
    from dealix.commercial_ops.complete_autonomous_day import build_complete_autonomous_plan

    plan = build_complete_autonomous_plan(skip_commercial_day=True)
    assert plan.get("strongest_plan_wiring") is True
    assert int(plan.get("task_count") or 0) >= 138
    assert plan.get("research_verdict_ar")


def test_complete_autonomous_day_dry_run_cli() -> None:
    """CLI dry-run must finish quickly (lazy imports; no full autopilot stack)."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from scripts.run_dealix_complete_autonomous_day import main

    buf = io.StringIO()
    argv = sys.argv
    try:
        sys.argv = ["run_dealix_complete_autonomous_day.py", "--dry-run"]
        with redirect_stdout(buf):
            code = main()
    finally:
        sys.argv = argv

    out = buf.getvalue()
    assert code == 0
    assert "DEALIX_COMPLETE_AUTONOMOUS_DAY=DRY_RUN" in out
    assert "strongest_plan_wiring" in out

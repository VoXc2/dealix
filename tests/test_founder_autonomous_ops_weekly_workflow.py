"""Regression guard for the scheduled Founder Autonomous Ops Weekly runner."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "founder_autonomous_ops_weekly.yml"
RUNNER = ROOT / "scripts" / "run_dealix_full_autonomous_ops.py"


def test_weekly_workflow_does_not_use_removed_skip_founder_day_flag() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "--skip-founder-day" not in workflow


def test_weekly_workflow_uses_supported_governed_dry_run_flags() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")

    for flag in ("--dry-run", "--weekly", "--skip-commercial-day"):
        assert flag in workflow
        assert f'p.add_argument("{flag}"' in runner

    assert "python3 scripts/run_dealix_full_autonomous_ops.py" in workflow

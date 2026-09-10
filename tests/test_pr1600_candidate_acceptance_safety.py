from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "run_pr1600_candidate_acceptance.sh"


def _text() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_candidate_acceptance_never_mutates_live_schedulers() -> None:
    text = _text()
    assert "SCHEDULER_MUTATION=false" in text
    assert "systemctl stop" not in text
    assert "systemctl start" not in text
    assert "systemctl restart" not in text
    assert "RESTORE_TIMERS" not in text


def test_candidate_acceptance_relies_on_reference_stability_not_timer_freeze() -> None:
    text = _text()
    assert '[[ "$END_MAIN" == "$MAIN" ]]' in text
    assert '[[ "$LIVE_END" == "$CANDIDATE" ]]' in text
    assert "MAIN_MOVED_DURING_ACCEPTANCE" in text
    assert "PR_MOVED_DURING_FULL" in text
    assert "PRODUCTION_GREEN=false" in text
    assert "MERGE_EXECUTED=false" in text
    assert "DEPLOY_EXECUTED=false" in text
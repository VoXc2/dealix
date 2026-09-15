from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/ops/dealix_agentic_holding_master.sh"


def _text() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_legacy_launcher_cannot_bypass_session_factory() -> None:
    text = _text()
    assert "scripts/ops/session_factory.py" in text
    assert "factory.submit_job" in text
    assert 'job_class="ENGINEERING"' in text
    assert 'authority_level="L4"' in text
    assert 'modifying=True' in text


def test_legacy_launcher_does_not_create_worktrees_or_run_opencode_directly() -> None:
    text = _text()
    assert "worktree add" not in text
    assert '"$OPENCODE" run' not in text
    assert "DIRECT_OPENCODE_EXECUTION=DENIED" in text
    assert "DIRECT_WORKTREE_CREATION=DENIED" in text


def test_legacy_launcher_runs_as_canonical_user_without_root_dependency() -> None:
    text = _text()
    assert "ERROR=RUN_AS_ROOT" not in text
    assert 'CURRENT_USER="$(id -un)"' in text
    assert 'if [ "$(id -un)" = "$RUN_USER" ]; then' in text
    assert "ERROR=RUN_AS_CANONICAL_USER_OR_ROOT" in text


def test_legacy_launcher_preserves_material_effect_guard() -> None:
    text = _text()
    assert "L5_EXECUTED=NONE" in text
    assert "no silent paid spill" in text.lower()
    assert "Builder and independent Verifier must remain separate" in text

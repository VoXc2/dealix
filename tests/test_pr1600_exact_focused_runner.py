"""Regression guards for the repo-native PR #1600 focused orchestrator."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "ops" / "run_pr1600_exact_focused.sh"
CATALOG_REPAIR = ROOT / "scripts" / "ops" / "repair_verify_catalog_exact_head.sh"


def _source() -> str:
    return RUNNER.read_text(encoding="utf-8")


def _catalog_repair_source() -> str:
    return CATALOG_REPAIR.read_text(encoding="utf-8")


def test_runner_avoids_heredocs_after_v11_wrapper_incident() -> None:
    text = _source()
    assert "<<" not in text
    assert "here-doc" not in text.lower()


def test_runner_propagates_focused_failure_before_any_pass_result() -> None:
    text = _source()
    fail_branch = text.index("if (( FOCUSED_RC != 0 )); then")
    hold_call = text.index('hold CURRENT_EXACT_FOCUSED "$FOCUSED_RC"', fail_branch)
    pass_result = text.index("RESULT=PR1600_CURRENT_EXACT_FOCUSED_PASS")
    assert fail_branch < hold_call < pass_result
    assert "FOCUSED_ACCEPTANCE=FAIL" in text
    assert "FOCUSED_ACCEPTANCE=PASS" in text


def test_runner_binds_acceptance_to_live_exact_head_and_current_main() -> None:
    text = _source()
    assert '"+refs/pull/$PR/head:$REF"' in text
    assert 'API_HEAD="$(as_dealix gh api' in text
    assert '[[ "$HEAD" == "$API_HEAD" ]]' in text
    assert 'merge-base "$MAIN" "$HEAD"' in text
    assert 'DEALIX_ACCEPT_EXPECTED_HEAD="$HEAD"' in text
    assert 'DEALIX_ACCEPT_EXPECTED_BASE="$MAIN"' in text
    assert '[[ "$HEAD" == "$END_HEAD" ]]' in text
    assert '[[ "$MAIN" == "$END_MAIN" ]]' in text


def test_runner_cannot_execute_material_l5_actions() -> None:
    text = _source()
    forbidden = (
        "gh pr merge",
        "git push",
        "railway up",
        "railway deploy",
        "railway link",
        "vercel --prod",
        "cloudflare",
        "payment_intent",
    )
    for token in forbidden:
        assert token not in text.lower()
    assert "PRODUCTION_GREEN=false" in text
    assert "RAILWAY_STAGED_APPLY=0" in text
    assert "DEALIX_EXTERNAL_SEND=0" in text
    assert "PAYMENT_EXECUTION=0" in text


def test_runner_does_not_mask_required_gate_failures() -> None:
    text = _source()
    assert "|| true" not in text
    assert "DEALIX_ACCEPT_FULL_PYTEST=0" in text
    assert 'FOCUSED_RC=$?' in text


def test_catalog_repair_runs_python_and_pytest_from_exact_worktree_cwd() -> None:
    text = _catalog_repair_source()
    assert "run_in_wt()" in text
    assert 'cd "$WT"' in text
    assert 'PYTHONPATH="$WT"' in text
    assert 'HOME="/home/$RUN_USER"' in text
    assert 'run_in_wt "$PY" scripts/ops/build_verify_catalog.py > "$TMP"' in text
    assert 'run_in_wt "$PY" scripts/ops/build_verify_catalog.py --check' in text
    assert 'run_in_wt "$PY" -m pytest -q tests/test_verify_catalog.py' in text


def test_catalog_repair_avoids_shellcheck_sc2016_child_shell_pattern() -> None:
    text = _catalog_repair_source()
    assert "bash -c 'set -Eeuo pipefail" not in text
    assert 'cd "$1"' not in text


def test_catalog_repair_does_not_run_repo_pytest_from_inherited_root_cwd() -> None:
    text = _catalog_repair_source()
    forbidden = (
        'as_dealix env PYTHONPATH="$WT" "$PY" -m pytest',
        'as_dealix "$PY" -m pytest',
    )
    for token in forbidden:
        assert token not in text


def test_catalog_repair_remains_l4_only() -> None:
    text = _catalog_repair_source().lower()
    forbidden = (
        "gh pr merge",
        "railway up",
        "railway deploy",
        "vercel --prod",
        "dns_mutation=1",
        "db_mutation=1",
        "secret_mutation=1",
        "payment_execution=1",
        "dealix_external_send=1",
    )
    for token in forbidden:
        assert token not in text
    assert "production_green=false" in text

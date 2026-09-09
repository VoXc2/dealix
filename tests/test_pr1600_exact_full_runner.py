"""Regression guards for the repo-native PR #1600 full acceptance wrapper."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "ops" / "run_pr1600_live_full_acceptance.sh"


def _source() -> str:
    return RUNNER.read_text(encoding="utf-8")


def test_full_runner_uses_live_exact_head_and_current_main() -> None:
    text = _source()
    assert '"+refs/pull/$PR/head:$REF"' in text
    assert 'API_HEAD="$(as_dealix gh api' in text
    assert '[[ "$HEAD" == "$API_HEAD" ]]' in text
    assert 'merge-base "$MAIN" "$HEAD"' in text
    assert 'DEALIX_ACCEPT_EXPECTED_HEAD="$HEAD"' in text
    assert 'DEALIX_ACCEPT_EXPECTED_BASE="$MAIN"' in text
    assert 'DEALIX_ACCEPT_FULL_PYTEST=1' in text


def test_full_runner_is_read_only_with_respect_to_l5() -> None:
    text = _source().lower()
    forbidden = (
        "gh pr merge",
        "git push",
        "railway up",
        "railway deploy",
        "railway redeploy",
        "vercel --prod",
        "payment_intent",
    )
    for token in forbidden:
        assert token not in text
    assert "production_green=false" in text
    assert "railway_staged_apply=0" in text
    assert "dealix_external_send=0" in text
    assert "payment_execution=0" in text


def test_full_runner_propagates_acceptance_failure() -> None:
    text = _source()
    fail_branch = text.index("if (( RC != 0 )); then")
    hold_call = text.index("hold FULL_ACCEPTANCE", fail_branch)
    pass_result = text.index("RESULT=PR1600_CURRENT_EXACT_FULL_PASS")
    assert fail_branch < hold_call < pass_result
    assert "FULL_ACCEPTANCE=FAIL" in text
    assert "FULL_ACCEPTANCE=PASS" in text


def test_full_runner_checks_head_stability_after_acceptance() -> None:
    text = _source()
    assert '[[ "$END_HEAD" == "$HEAD" ]]' in text
    assert '[[ "$END_MAIN" == "$MAIN" ]]' in text
    assert '[[ "$END_PR" == "$HEAD" ]]' in text
    assert "EXACT_HEAD_STABILITY=PASS" in text

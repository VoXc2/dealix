from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "accept_release_trust_pr.sh"


def _text() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_acceptance_runner_is_fail_closed_and_exact_head_bound() -> None:
    text = _text()
    assert "set -Eeuo pipefail" in text
    assert "DEALIX_ACCEPT_EXPECTED_HEAD" in text
    assert "EXACT_HEAD=FAIL" in text
    assert "HEAD_STABILITY=FAIL" in text
    assert "RELEASE_TRUST_ACCEPTANCE=PASS" in text
    assert "run_gate TARGETED_PYTHON" in text
    assert "run_gate WEB_ACCEPTANCE" in text
    assert "run_gate BRAND_IDENTITY_V2" in text


def test_acceptance_runner_rejects_unsupported_node_runtime() -> None:
    text = _text()
    assert 'required="20 || >=22"' in text
    assert 'node_major" != "20"' in text
    assert 'node_major" -lt 22' in text


def test_acceptance_runner_contains_no_material_execution_verbs() -> None:
    text = _text().lower()
    forbidden_commands = (
        "git merge ",
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "railway variables set",
        "kubectl apply",
    )
    for token in forbidden_commands:
        assert token not in text


def test_full_pytest_is_explicit_mode_and_still_fail_closed() -> None:
    text = _text()
    assert "DEALIX_ACCEPT_FULL_PYTEST" in text
    assert 'run_gate PYTHON_FULL "$PY" -m pytest -q' in text
    assert "PYTHON_FULL=SKIPPED_BY_MODE" in text

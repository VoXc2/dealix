from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "ops" / "fail_closed_gate.sh"


def _run(label: str, *command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(GATE), label, *command],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_gate_emits_pass_only_for_zero_exit() -> None:
    result = _run("PYTHON_TESTS", "bash", "-c", "exit 0")
    assert result.returncode == 0
    assert "PYTHON_TESTS=PASS" in result.stdout
    assert "PYTHON_TESTS=FAIL" not in result.stdout + result.stderr


def test_gate_propagates_failure_and_never_prints_false_pass() -> None:
    result = _run("PYTHON_TESTS", "bash", "-c", "exit 7")
    assert result.returncode == 7
    combined = result.stdout + result.stderr
    assert "PYTHON_TESTS=FAIL rc=7" in combined
    assert "PYTHON_TESTS=PASS" not in combined


def test_web_failure_cannot_be_relabelled_pass() -> None:
    result = _run("WEB_ACCEPTANCE", "bash", "-c", "printf 'tsc failed\\n'; exit 2")
    assert result.returncode == 2
    combined = result.stdout + result.stderr
    assert "tsc failed" in combined
    assert "WEB_ACCEPTANCE=FAIL rc=2" in combined
    assert "WEB_ACCEPTANCE=PASS" not in combined


def test_invalid_label_fails_closed() -> None:
    result = _run("bad-label", "true")
    assert result.returncode == 64
    assert "INVALID_GATE_LABEL=bad-label" in result.stderr

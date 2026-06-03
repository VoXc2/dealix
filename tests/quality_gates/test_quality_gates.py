"""Email / proposal / delivery quality gates must pass on the seed data."""
import pytest

CHECKS = [
    "scripts/checks/check_email_quality_gate.py",
    "scripts/checks/check_proposal_gate.py",
    "scripts/checks/check_delivery_gate.py",
]


@pytest.mark.parametrize("script", CHECKS)
def test_quality_gate(run_check, script):
    proc = run_check(script)
    assert proc.returncode == 0, f"{script} failed:\n{proc.stdout}\n{proc.stderr}"

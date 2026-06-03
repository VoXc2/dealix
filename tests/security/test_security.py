"""Security & privacy gate must pass."""


def test_security_privacy_gate(run_check):
    proc = run_check("scripts/checks/check_security_privacy_gates.py")
    assert proc.returncode == 0, f"security gate failed:\n{proc.stdout}\n{proc.stderr}"

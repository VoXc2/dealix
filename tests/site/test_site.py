"""Public site route + catalog boundary checks must pass."""


def test_site_routes(run_check):
    proc = run_check("scripts/checks/check_site_routes.py")
    assert proc.returncode == 0, f"site routes check failed:\n{proc.stdout}\n{proc.stderr}"


def test_ready_to_launch(run_check):
    proc = run_check("scripts/checks/check_ready_to_launch_scorecard.py")
    assert proc.returncode == 0, f"launch scorecard failed:\n{proc.stdout}\n{proc.stderr}"

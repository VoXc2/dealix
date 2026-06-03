"""Smoke-test the dealix CLI commands (all read-only, no external sends)."""
import dealix


def test_account_packs_dry_run():
    assert dealix.main(["account-packs", "--limit", "5", "--dry-run"]) == 0


def test_delivery_status():
    assert dealix.main(["delivery-status"]) == 0


def test_founder_command_dry_run():
    assert dealix.main(["founder-command", "--dry-run"]) == 0


def test_quality_check():
    assert dealix.main(["quality-check"]) == 0


def test_security_check():
    assert dealix.main(["security-check"]) == 0


def test_launch_score_full():
    assert dealix.main(["launch-score", "--min", "90"]) == 0


def test_factory_run_requires_dry_run():
    assert dealix.main(["factory-run"]) == 2
    assert dealix.main(["factory-run", "--dry-run"]) == 0

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


def _text(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def test_legacy_healthcheck_is_manual_and_read_only() -> None:
    text = _text("scheduled_healthcheck.yml")
    assert "workflow_dispatch:" in text
    assert "schedule:" not in text
    assert "demo-request" not in text
    assert '"consent":true' not in text
    assert "-X POST" not in text
    assert "/healthz" in text
    assert "/api/v1/pricing/plans" in text


def test_production_watchdog_is_manual_only_in_github_actions() -> None:
    text = _text("production-watchdog.yml")
    assert "workflow_dispatch:" in text
    assert "schedule:" not in text
    assert "https://dealix.me/" in text
    assert "https://api.dealix.me/healthz" in text


def test_dlq_check_is_manual_only_in_github_actions() -> None:
    text = _text("dlq_check.yml")
    assert "workflow_dispatch:" in text
    assert "schedule:" not in text
    assert "scripts/check_dlq_size.py --max 5 --json" in text
    assert "STAGING_REDIS_URL" in text
    assert "PRODUCTION_REDIS_URL" in text

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-full-ops-daily.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_governed_daily_scheduler_runs_canonical_company_os() -> None:
    text = workflow_text()
    assert 'cron: "0 */4 * * *"' in text
    assert "scripts/run_dealix_complete_autonomous_day.py" in text
    assert "scripts/commercial/run_company_os_daily.py" in text
    assert "scripts/commercial/run_autonomous_growth_daily.py" in text
    assert "scripts/commercial/run_self_improvement_daily.py" in text
    assert "--autonomy-level 4" in text
    assert "--mode draft-only" in text


def test_governed_daily_scheduler_remains_fail_closed_for_l5() -> None:
    text = workflow_text()
    required_zero = (
        "DEALIX_EXTERNAL_SEND",
        "DEALIX_EMAIL_LIVE_SEND",
        "DEALIX_WHATSAPP_OUTBOUND",
        "DEALIX_PUBLIC_PUBLISH",
        "DEALIX_PAID_SPEND",
        "DEALIX_LIVE_PAYMENT",
        "DEALIX_PAYMENT_EXECUTION",
        "DEALIX_PRODUCTION_MUTATION",
        "DEALIX_DNS_MUTATION",
        "DEALIX_DB_MUTATION",
        "DEALIX_SECRET_MUTATION",
        "DEALIX_IDENTITY_MUTATION",
        "DEALIX_AGENT_SELF_AUTHORITY",
    )
    for flag in required_zero:
        assert f'{flag}: "0"' in text
        assert f'test "${flag}" = "0"' in text

    assert 'DEALIX_AUTONOMY_LEVEL: "4"' in text
    assert 'DEALIX_MODE: "draft-only"' in text
    assert 'VOICE_AI_ENABLED: "false"' in text
    assert 'VOICE_OUTBOUND_ENABLED: "false"' in text
    assert 'VOICE_RECORDING_ENABLED: "false"' in text


def test_governed_daily_scheduler_preserves_company_os_evidence() -> None:
    text = workflow_text()
    assert "reports/self_operating_company_os/" in text
    assert "docs/snapshots/*.json" in text
    assert "data/founder_briefs/" in text

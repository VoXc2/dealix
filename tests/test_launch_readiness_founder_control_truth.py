from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify_dealix_launch_readiness.py"


def test_launch_readiness_requires_telegram_openclaw_not_slack() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert "Telegram/OpenClaw Founder Control E2E" in text
    assert "Telegram/OpenClaw Founder Control end-to-end execution receipt" in text
    assert "Slack Founder Bridge end-to-end execution receipt" not in text
    assert "Slack bridge E2E" not in text


def test_repository_score_cannot_claim_public_production_readiness() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert "PUBLIC_PRODUCTION_READINESS=NOT_INFERRED" in text
    assert "Railway canonical `apps/web` deployment identity + deployed SHA" in text
    assert "exact-head sovereign Trust/Commercial/E2E acceptance" in text

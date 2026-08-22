"""Regression guard for the bounded Hermes 8K acceptance probe."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "scripts/ops/dealix_total_company_launcher.sh",
    ROOT / "scripts/ops/activate_dealix_from_main.sh",
]

EXPECTED = (
    'hermes chat -Q --ignore-rules --toolsets clarify --max-turns 1 '
    '-q "Do not use tools. Reply with exactly: DEALIX_HERMES_8K_OK"'
)


def test_hermes_acceptance_uses_chat_path_that_honors_ignore_rules() -> None:
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        assert EXPECTED in text, path
        assert 'hermes --ignore-rules --toolsets terminal -z' not in text, path


def test_council_stays_fail_closed_until_exact_acceptance_marker() -> None:
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        assert "HERMES_OK=0" in text, path
        assert "grep -Fxq DEALIX_HERMES_8K_OK" in text, path
        assert "dealix-agent-council.timer" in text, path
        assert "HERMES_8K=FAIL_CLOSED" in text or "AGENT_COUNCIL=DISABLED_FAIL_CLOSED" in text, path


def test_acceptance_does_not_use_dangerous_or_mutating_toolset() -> None:
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        acceptance = [line for line in text.splitlines() if "DEALIX_HERMES_8K_OK" in line and "hermes chat" in line]
        assert len(acceptance) == 1, path
        line = acceptance[0]
        assert "--toolsets clarify" in line
        assert "--toolsets terminal" not in line
        assert "--yolo" not in line

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts/ops/dealix_omega_weekly_wrapper.sh"
INSTALLER = ROOT / "scripts/ops/install_dealix_omega_weekly_wrapper.sh"


def test_shell_sources_are_syntax_valid() -> None:
    for path in (WRAPPER, INSTALLER):
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr


def test_timeout_runs_inside_identity_wrapper() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    assert "as_dealix timeout 1800" in text
    assert "timeout 1800 \\\n    as_dealix" not in text


def test_weekly_wrapper_is_draft_only_and_non_sending() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    assert "DEALIX_EXTERNAL_OUTREACH_ENABLED=false" in text
    assert "AUTO_SEND_ENABLED=false" in text
    assert "DEALIX_LIVE_CHARGE=false" in text
    assert "--mode draft-only" in text

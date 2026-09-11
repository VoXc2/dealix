from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SH = (ROOT / "scripts" / "railway_prod_bootstrap.sh").read_text(encoding="utf-8")
PS1 = (ROOT / "scripts" / "railway_prod_bootstrap.ps1").read_text(encoding="utf-8")


def test_legacy_bootstraps_are_fail_closed() -> None:
    for text in (SH, PS1):
        assert "ACTION_HASH" in text
        assert "exit 75" in text
        assert "alembic upgrade head" not in text
        assert "seed_revenue_machine_candidates" not in text
        assert "ops-autopilot/war-room/import-targets" not in text


def test_shell_bootstrap_has_no_material_command_surface() -> None:
    assert "curl " not in SH
    assert "DATABASE_URL" not in SH


def test_powershell_bootstrap_has_no_material_command_surface() -> None:
    assert "Invoke-RestMethod" not in PS1
    assert "DATABASE_URL" not in PS1

"""Smoke tests for official launch helpers."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_official_launch_scripts_exist() -> None:
    for name in (
        "scripts/official_launch_verify.sh",
        "scripts/official_launch_verify.ps1",
        "scripts/railway_prod_bootstrap.sh",
        "scripts/railway_prod_bootstrap.ps1",
    ):
        assert (REPO / name).is_file(), name


def test_founder_daily_pack_endpoint_importable() -> None:
    from api.routers.revenue_ops_autopilot import ops_founder_daily_pack

    assert callable(ops_founder_daily_pack)


def test_agency_seed_has_warm_replace_rows() -> None:
    csv_path = REPO / "docs/commercial/operations/targeting/agency_accounts_seed.csv"
    text = csv_path.read_text(encoding="utf-8")
    assert "REPLACE:" in text
    assert text.count("\n") >= 20

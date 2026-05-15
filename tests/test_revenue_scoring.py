"""Revenue OS — deterministic account scoring."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.scoring import score_account_row


def test_score_account_row_full_icp_match() -> None:
    row = {
        "company_name": "Acme",
        "sector": "logistics",
        "city": "Riyadh",
        "source": "crm_export",
    }
    out = score_account_row(
        row,
        icp_sectors=frozenset({"logistics"}),
        icp_cities=frozenset({"Riyadh"}),
    )
    assert out["score"] == 100
    assert "sector_icp_match" in out["reasons"]
    assert "city_icp_match" in out["reasons"]


def test_score_account_row_flags_missing_source() -> None:
    row = {
        "company_name": "Acme",
        "sector": "logistics",
        "city": "Riyadh",
        "source": "",
    }
    out = score_account_row(row, icp_sectors=frozenset({"logistics"}))
    assert "missing_source" in out["risks"]
    assert out["score"] < 100


def test_score_account_row_missing_company() -> None:
    row = {"company_name": "", "sector": "x", "city": "y", "source": "s"}
    out = score_account_row(row)
    assert "missing_company_name" in out["risks"]

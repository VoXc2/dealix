"""Basic structural checks on the public holding landing page."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HOLDING = REPO_ROOT / "landing" / "holding.html"
ANNUAL = REPO_ROOT / "landing" / "annual-report.html"
PORTFOLIO = REPO_ROOT / "landing" / "portfolio.html"


def test_holding_landing_exists():
    assert HOLDING.exists()


def test_holding_landing_has_required_sections():
    text = HOLDING.read_text(encoding="utf-8")
    for header in (
        "Dealix Group",
        "Sub-Brand Portfolio",
        "Board",
        "Cap Table",
        "Doctrine Anchor",
        "Trust at a Glance",
    ):
        assert header in text, f"holding.html missing section: {header}"


def test_holding_landing_links_to_versioned_doctrine():
    text = HOLDING.read_text(encoding="utf-8")
    assert "/api/v1/doctrine?version=v1.0.0" in text


def test_holding_landing_references_all_public_endpoints():
    text = HOLDING.read_text(encoding="utf-8")
    for endpoint in (
        "/api/v1/holding/charter",
        "/api/v1/holding/portfolio",
        "/api/v1/holding/board",
        "/api/v1/holding/cap-table/public",
        "/api/v1/dealix-promise",
    ):
        assert endpoint in text, f"holding.html missing endpoint: {endpoint}"


def test_annual_report_viewer_exists_and_loads_md():
    assert ANNUAL.exists()
    text = ANNUAL.read_text(encoding="utf-8")
    assert "dealix-group-annual-report-2026.md" in text


def test_portfolio_page_exists_and_redirects_to_group():
    assert PORTFOLIO.exists()
    text = PORTFOLIO.read_text(encoding="utf-8")
    assert "group.html" in text

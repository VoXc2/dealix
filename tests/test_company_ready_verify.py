"""Smoke tests for company_ready_verify required documentation paths."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/company/DEALIX_COMPANY_READY_MASTER_AR.md",
    "docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md",
    "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
    "docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md",
    "docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md",
    "scripts/company_ready_verify.sh",
    "scripts/run_founder_revenue_day.sh",
]


def test_company_ready_required_docs_exist() -> None:
    missing = [p for p in REQUIRED if not (REPO_ROOT / p).is_file()]
    assert not missing, f"missing: {missing}"


def test_company_ready_master_links_revenue_day() -> None:
    text = (REPO_ROOT / "docs/company/DEALIX_COMPANY_READY_MASTER_AR.md").read_text(
        encoding="utf-8",
    )
    assert "run_founder_revenue_day" in text
    assert "company_ready_verify" in text

"""API domain ownership docs and sales OWNERS."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_api_domain_ownership_doc_exists() -> None:
    assert (REPO / "docs/architecture/API_DOMAIN_OWNERSHIP.md").is_file()


def test_sales_owners_yaml() -> None:
    data = yaml.safe_load(
        (REPO / "api/routers/domains/sales/OWNERS.yaml").read_text(encoding="utf-8")
    )
    assert data.get("domain") == "sales"
    assert data.get("owner_os") == "gtm"

"""Smoke: external pack registry and usage log shape."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_external_pack_registry_exists() -> None:
    p = REPO_ROOT / "docs/strategic/EXTERNAL_PACK_REGISTRY_AR.md"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "Partner Intro Pack" in text
    assert "Investor Diligence Lite" in text
    assert "Client Proof Demo Pack" in text
    assert "لا يحتوي بيانات عميل" in text
    assert "Operator Onboarding Pack" in text
    assert "Enterprise Trust Pack Lite" in text


def test_docs_usage_log_exists_and_schema() -> None:
    p = REPO_ROOT / "data/docs_asset_usage_log.json"
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert data.get("log_id") == "DOCS-ASSET-USAGE-LOG-001"
    assert "entries" in data
    assert isinstance(data["entries"], list)
    assert "usage_types" in data
    assert isinstance(data["usage_types"], list)
    ro = data.get("response_outcomes")
    assert isinstance(ro, list)
    for o in (
        "follow_up_sent",
        "scope_requested",
        "prepared_not_sent",
        "invoice_sent",
    ):
        assert o in ro

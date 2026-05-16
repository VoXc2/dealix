"""AI unit economics config."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_ai_unit_economics_yaml() -> None:
    data = yaml.safe_load((REPO / "dealix/transformation/ai_unit_economics.yaml").read_text())
    assert data.get("ledger_kind") == "ai_spend"

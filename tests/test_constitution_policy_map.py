"""Constitution policy map non-negotiables."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_constitution_policy_map_has_five_rules() -> None:
    path = REPO / "auto_client_acquisition/governance_os/constitution_policy_map.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules = data.get("non_negotiables") or []
    assert len(rules) >= 5
    ids = {r["id"] for r in rules}
    assert "no_cold_whatsapp" in ids
    assert "no_linkedin_dm" in ids

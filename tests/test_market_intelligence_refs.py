"""Market intelligence pack YAML — paths exist."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
REFS = REPO / "dealix" / "config" / "market_intelligence_refs.yaml"


def test_market_intelligence_refs_yaml_loads() -> None:
    data = yaml.safe_load(REFS.read_text(encoding="utf-8"))
    assert data.get("version") == "1"
    pillars = data.get("pillars") or {}
    assert len(pillars) >= 10


def test_market_intelligence_pillar_paths_exist() -> None:
    data = yaml.safe_load(REFS.read_text(encoding="utf-8"))
    missing: list[str] = []
    for _key, item in (data.get("pillars") or {}).items():
        if not isinstance(item, dict):
            continue
        rel = item.get("path")
        if rel and not (REPO / str(rel)).is_file():
            missing.append(str(rel))
    index = data.get("index")
    if index and not (REPO / str(index)).is_file():
        missing.append(str(index))
    assert missing == [], f"missing: {missing}"


def test_pillar_of_week_has_doc() -> None:
    from dealix.commercial_ops.market_intelligence_refs import pillar_of_week

    pow_doc = pillar_of_week()
    assert pow_doc is not None
    assert pow_doc.get("doc")
    assert (REPO / pow_doc["doc"]).is_file()


def test_build_market_intel_digest_block() -> None:
    from dealix.commercial_ops.market_intelligence_refs import build_market_intel_digest_block

    block = build_market_intel_digest_block()
    assert "pillar_of_week" in block
    assert block.get("master_index")

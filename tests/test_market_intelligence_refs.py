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


def test_official_source_watch_block_is_read_only_evidence() -> None:
    from datetime import UTC, datetime

    from dealix.commercial_ops.market_intelligence_refs import (
        build_official_source_watch_digest_block,
    )

    block = build_official_source_watch_digest_block(
        datetime(2026, 9, 15, 3, 10, tzinfo=UTC)
    )
    assert block["status"] == "PASS_READ_ONLY_EVIDENCE"
    assert block["signal_count"] >= 1
    assert block["fresh_count"] >= 1
    assert block["authority"] == {
        "relationship": False,
        "consent": False,
        "buyer_intent": False,
        "pipeline": False,
        "revenue": False,
        "external_send": False,
    }
    assert all(signal["relationship_state"] == "RESEARCH_ONLY" for signal in block["signals"])
    assert all(signal["consent_state"] == "NOT_PROVEN" for signal in block["signals"])
    assert all(signal["counts_as_pipeline"] is False for signal in block["signals"])
    assert all(signal["allows_external_send"] is False for signal in block["signals"])
    assert all(signal["economic_governor_hint"]["creates_opportunity"] is False for signal in block["signals"])
    assert all(signal["radar_projection"]["counts_as_pipeline"] is False for signal in block["signals"])
    assert all(signal["radar_projection"]["counts_as_relationship"] is False for signal in block["signals"])


def test_official_source_watch_missing_receipts_holds(tmp_path: Path) -> None:
    from dealix.commercial_ops.market_intelligence_refs import (
        build_official_source_watch_digest_block,
    )

    block = build_official_source_watch_digest_block(receipts_path=tmp_path / "missing.json")
    assert block["status"] == "HOLD_MISSING_CANONICAL_RECEIPTS"
    assert block["signal_count"] == 0
    assert block["authority"]["pipeline"] is False
    assert block["authority"]["external_send"] is False


def test_market_digest_exposes_official_source_watch() -> None:
    from dealix.commercial_ops.market_intelligence_refs import build_market_intel_digest_block

    block = build_market_intel_digest_block()
    watch = block["official_source_watch"]
    assert watch["source_path"] == "data/commercial/market_signal_receipts_v1.json"
    assert watch["authority"]["relationship"] is False
    assert watch["authority"]["consent"] is False


def test_monshaat_jadeer_receipt_reaches_official_watch_without_opportunity_promotion() -> None:
    from datetime import UTC, datetime

    from dealix.commercial_ops.market_intelligence_refs import (
        build_official_source_watch_digest_block,
    )

    block = build_official_source_watch_digest_block(datetime(2026, 9, 15, 5, 0, tzinfo=UTC))
    jadeer = [
        signal
        for signal in block["signals"]
        if signal["canonical_ref"] == "sig-2026-monshaat-jadeer-supplier-readiness"
    ]
    assert len(jadeer) == 1
    signal = jadeer[0]
    assert signal["source_authority"] == "MONSHAAT"
    assert signal["relationship_state"] == "RESEARCH_ONLY"
    assert signal["consent_state"] == "NOT_PROVEN"
    assert signal["counts_as_pipeline"] is False
    assert signal["allows_external_send"] is False
    assert signal["economic_governor_hint"]["creates_opportunity"] is False
    assert signal["radar_projection"]["counts_as_revenue"] is False

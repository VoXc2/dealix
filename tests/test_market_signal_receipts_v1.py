"""Contracts for the real market-signal receipts (canonical radar contract).

Every receipt must validate against the canonical Universal Market Radar
receipt contract, carry provenance, and keep all authority flags false.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "data" / "commercial" / "market_signal_receipts_v1.json"
SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")


def _load_radar() -> object:
    path = ROOT / "scripts" / "commercial" / "run_universal_market_radar_v1.py"
    spec = importlib.util.spec_from_file_location("radar_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


radar = _load_radar()


def _payload() -> dict:
    return json.loads(RECEIPTS.read_text(encoding="utf-8"))


def test_receipt_file_exists_and_has_real_signals() -> None:
    payload = _payload()
    assert payload["schema"] == "dealix.market-signal-set.v1"
    signals = payload["signals"]
    assert len(signals) >= 12
    assert len({signal["signal_id"] for signal in signals}) == len(signals)


def test_every_receipt_passes_the_canonical_contract() -> None:
    radar_meta = json.loads((ROOT / "data" / "commercial" / "universal_market_radar_v1.json").read_text(encoding="utf-8"))
    required = set(radar_meta["market_signal_receipt_contract"]["required"])
    for signal in _payload()["signals"]:
        errors = radar.validate_receipt(signal, required)
        assert errors == [], (signal["signal_id"], errors)


def test_sources_and_sectors_are_admitted_by_the_canonical_registries() -> None:
    radar_meta = json.loads((ROOT / "data" / "commercial" / "universal_market_radar_v1.json").read_text(encoding="utf-8"))
    source_ids = {row["source_id"] for row in radar_meta["source_registry"]}
    playbooks = json.loads((ROOT / "data" / "commercial" / "universal_market_playbooks_v1.json").read_text(encoding="utf-8"))
    sector_ids = {row["id"] for row in playbooks["sector_families"]}
    assert radar.CROSS_SECTOR not in sector_ids  # portfolio-wide sentinel, never a 16th sector
    admitted_sector_refs = sector_ids | {radar.CROSS_SECTOR}
    for signal in _payload()["signals"]:
        assert signal["source_id"] in source_ids, signal["signal_id"]
        assert signal["sector_family"] in admitted_sector_refs, signal["signal_id"]


def test_authority_flags_are_all_false() -> None:
    for signal in _payload()["signals"]:
        assert signal["authority"] == radar.AUTHORITY, signal["signal_id"]


def test_provenance_and_priority_factors_are_complete() -> None:
    for signal in _payload()["signals"]:
        assert signal["evidence_refs"], signal["signal_id"]
        assert signal["facts"], signal["signal_id"]
        assert signal["provenance_ref"], signal["signal_id"]
        factors = signal.get("priority_factors", {})
        for name in radar.FACTOR_NAMES:
            value = factors.get(name)
            assert isinstance(value, (int, float)) and not isinstance(value, bool), (signal["signal_id"], name)
            assert 1 <= float(value) <= 5, (signal["signal_id"], name)


def test_no_secret_like_content_and_research_only_language() -> None:
    text = RECEIPTS.read_text(encoding="utf-8")
    assert not SECRET_RE.search(text)
    for signal in _payload()["signals"]:
        assert "INTERNAL_RESEARCH_ONLY" in signal["allowed_use"]
        assert "not" in (signal.get("priority_basis", "") + " ".join(signal["inferences"])).lower() or signal["inferences"]


def test_current_saudi_official_and_event_signals_are_truth_bounded() -> None:
    by_id = {row["signal_id"]: row for row in _payload()["signals"]}
    zatca = by_id["sig-2026-zatca-wave25-feb2027"]
    assert zatca["observed_at"].startswith("2026-07-24")
    assert zatca["source_ref"].startswith("https://zatca.gov.sa/")
    assert zatca["evidence_refs"] == [zatca["source_ref"]]
    assert not any("penalt" in fact.lower() for fact in zatca["facts"])
    cst = by_id["sig-2026-cst-ai-adoption-guide-20260727"]
    assert cst["observed_at"].startswith("2026-07-27")
    assert any("five dimensions" in fact.lower() for fact in cst["facts"])
    for signal_id in ("sig-2026-hospitality-expo-riyadh-sep15-17", "sig-2026-smart-cities-saudi-expo-sep15-17"):
        signal = by_id[signal_id]
        assert signal["signal_family"] == "EVENT_OR_FIELD"
        assert signal["authority"] == radar.AUTHORITY
        blob = " ".join(signal["inferences"] + signal["unknowns"]).lower()
        assert "relationship" in blob and "consent" in blob

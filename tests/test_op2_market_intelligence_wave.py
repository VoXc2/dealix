"""Contracts for the OP2 fresh market-intelligence wave.

The OP2 wave is public/regulatory research only. These tests assert the wave
stays inside the canonical radar contract, admits only registered sources and
sectors, and never claims relationship/consent/offer/quote/payment authority.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"


def _load_verifier():
    path = ROOT / "scripts" / "commercial" / "verify_op2_market_intelligence_wave.py"
    spec = importlib.util.spec_from_file_location("op2_wave_verifier", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


verifier = _load_verifier()


def _wave() -> dict:
    return json.loads(WAVE.read_text(encoding="utf-8"))


def test_wave_file_exists_with_unique_signals() -> None:
    payload = _wave()
    assert payload["schema"] == "dealix.market-signal-set.v1"
    assert payload["lane"] == "OP2"
    signals = payload["signals"]
    assert len(signals) >= verifier.MIN_SIGNALS
    assert len({signal["signal_id"] for signal in signals}) == len(signals)


def test_wave_passes_all_fail_closed_checks() -> None:
    payload = _wave()
    radar_meta = verifier._read_json(verifier.RADAR_PATH)
    playbooks = verifier._read_json(verifier.PLAYBOOK_PATH)
    runner = verifier._load_runner()
    assert verifier.validate_wave(payload, radar_meta, playbooks, runner) == []


def test_authority_and_allowed_use_are_research_only() -> None:
    runner = verifier._load_runner()
    payload = _wave()
    assert payload["authority"] == runner.AUTHORITY
    for signal in payload["signals"]:
        assert signal["authority"] == runner.AUTHORITY
        assert signal["allowed_use"] == ["INTERNAL_RESEARCH_ONLY"]


def test_canonical_sector_overrides_are_bounded() -> None:
    from dealix.commercial.economic_cell import Sector

    allowed = {sector.value for sector in Sector}
    for signal in _wave()["signals"]:
        override = signal.get("canonical_sector_id")
        if override:
            assert override in allowed

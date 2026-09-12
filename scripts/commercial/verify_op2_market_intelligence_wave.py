#!/usr/bin/env python3
"""Verify the OP2 fresh Saudi market-intelligence wave.

The OP2 lane captures public/regulatory market signals only. A signal is not an
opportunity, relationship, consent, quote, or revenue. This verifier fails closed
if any receipt over-claims authority, drifts from the canonical radar contract,
or cites a source/sector that the canonical registries do not admit.

Prints: DEALIX_OP2_MARKET_WAVE_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
WAVE_PATH = REPO_ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"
RADAR_PATH = REPO_ROOT / "data" / "commercial" / "universal_market_radar_v1.json"
PLAYBOOK_PATH = REPO_ROOT / "data" / "commercial" / "universal_market_playbooks_v1.json"
RUNNER_PATH = REPO_ROOT / "scripts" / "commercial" / "run_universal_market_radar_v1.py"

SCHEMA = "dealix.market-signal-set.v1"
MIN_SIGNALS = 8
MIN_REGULATORS = 4
SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")
VERDICT_PASS = "DEALIX_OP2_MARKET_WAVE_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_MARKET_WAVE_VERDICT=FAIL"


def _load_runner() -> Any:
    spec = importlib.util.spec_from_file_location("op2_radar_runner", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_wave(wave: dict[str, Any], radar_meta: dict[str, Any], playbooks: dict[str, Any], runner: Any) -> list[str]:
    errors: list[str] = []

    if wave.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if wave.get("lane") != "OP2":
        errors.append("lane must be OP2")

    signals = wave.get("signals")
    if not isinstance(signals, list):
        return ["signals must be a list"]
    if len(signals) < MIN_SIGNALS:
        errors.append(f"expected >= {MIN_SIGNALS} signals, got {len(signals)}")

    ids = [signal.get("signal_id") for signal in signals]
    if len(set(ids)) != len(ids):
        errors.append("signal_id values must be unique")

    required = set(radar_meta["market_signal_receipt_contract"]["required"])
    source_ids = {row["source_id"] for row in radar_meta["source_registry"]}
    sector_ids = {row["id"] for row in playbooks["sector_families"]}
    regulators: set[str] = set()

    for signal in signals:
        signal_id = str(signal.get("signal_id"))
        errors.extend(f"{signal_id}: {err}" for err in runner.validate_receipt(signal, required))
        if signal.get("source_id") not in source_ids:
            errors.append(f"{signal_id}: source_id not admitted by canonical registry")
        if signal.get("sector_family") not in sector_ids:
            errors.append(f"{signal_id}: sector_family not admitted by canonical playbooks")
        if signal.get("authority") != runner.AUTHORITY:
            errors.append(f"{signal_id}: authority over-claims (must be all-false)")
        factors = signal.get("priority_factors") or {}
        for name in runner.FACTOR_NAMES:
            value = factors.get(name)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{signal_id}: priority factor {name} missing/non-numeric")
        if signal.get("allowed_use") != ["INTERNAL_RESEARCH_ONLY"]:
            errors.append(f"{signal_id}: allowed_use must be exactly INTERNAL_RESEARCH_ONLY")
        if not signal.get("evidence_refs"):
            errors.append(f"{signal_id}: evidence_refs must be non-empty")
        if not signal.get("facts"):
            errors.append(f"{signal_id}: facts must be non-empty")
        observed = runner.parse_time(signal.get("observed_at"))
        fresh_until = runner.parse_time(signal.get("fresh_until"))
        if observed and fresh_until and fresh_until <= observed:
            errors.append(f"{signal_id}: fresh_until must be after observed_at")
        authority_ref = str(signal.get("authority_ref") or "").strip()
        if authority_ref:
            regulators.add(authority_ref)
        else:
            errors.append(f"{signal_id}: authority_ref must be non-empty")

    if len(regulators) < MIN_REGULATORS:
        errors.append(f"expected >= {MIN_REGULATORS} distinct authority refs, got {len(regulators)}")

    if SECRET_RE.search(WAVE_PATH.read_text(encoding="utf-8")):
        errors.append("secret-like content detected in wave file")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the OP2 market-intelligence wave")
    parser.add_argument("--json", action="store_true", help="emit machine-readable result")
    args = parser.parse_args()

    try:
        wave = _read_json(WAVE_PATH)
        radar_meta = _read_json(RADAR_PATH)
        playbooks = _read_json(PLAYBOOK_PATH)
        runner = _load_runner()
    except Exception as exc:
        print(VERDICT_FAIL)
        print(f"ERROR={exc}")
        return 1

    errors = validate_wave(wave, radar_meta, playbooks, runner)
    if args.json:
        print(json.dumps({"verdict": "PASS" if not errors else "FAIL", "errors": errors}, indent=2))
    else:
        print(VERDICT_PASS if not errors else VERDICT_FAIL)
        for err in errors:
            print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

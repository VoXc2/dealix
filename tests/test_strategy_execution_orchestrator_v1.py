from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "commercial" / "run_strategy_execution_orchestrator_v1.py"
CONFIG = ROOT / "config" / "company" / "strategy_execution_orchestrator_v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("strategy_orchestrator", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_config_keeps_material_authority_false_and_wip_bounded():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert all(value is False for value in data["material_authority"].values())
    assert data["wip_limits"]["top_actions_per_cycle"] <= 3
    assert data["wip_limits"]["active_venture_experiments"] <= 2
    assert data["wip_limits"]["capability_benchmarks"] <= 1
    assert data["wip_limits"]["material_approval_packets"] <= 1


def test_no_oss_auto_install():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert data["oss_admission"]
    assert all(item["automatic_install"] is False for item in data["oss_admission"])


def test_top_actions_never_exceed_three():
    module = load_module()
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    actions = module.choose_actions(data, {})
    assert 1 <= len(actions) <= 3
    assert all(all(v is False for v in item["material_authority"].values()) for item in actions)


def test_d4_signal_prioritizes_bid_no_bid_without_submission_authority():
    module = load_module()
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    state = {"active_d4_procurement": True, "evidence": {"official_procurement_evidence": True}}
    actions = module.choose_actions(data, state)
    ids = {item["id"] for item in actions}
    assert "d4_procurement_bid_no_bid" in ids
    item = next(x for x in actions if x["id"] == "d4_procurement_bid_no_bid")
    assert item["material_authority"]["bid"] is False


def test_oss_requires_named_gap():
    module = load_module()
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert module.choose_oss(data, {}) == []
    chosen = module.choose_oss(data, {"named_capability_gap": "sbom evidence"})
    assert len(chosen) <= 1
    assert chosen[0]["automatic_install"] is False

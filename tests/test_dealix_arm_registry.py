from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "scripts" / "commercial" / "verify_dealix_arm_registry.py"
REGISTRY_PATH = ROOT / "config" / "company" / "dealix_arm_registry.json"
CONSTITUTION_PATH = ROOT / "config" / "company" / "dealix_operating_constitution.json"
SPEC = importlib.util.spec_from_file_location("arm_registry_verify", VERIFY_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def registry_payload() -> dict:
    return copy.deepcopy(json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))


def constitution_payload() -> dict:
    return copy.deepcopy(json.loads(CONSTITUTION_PATH.read_text(encoding="utf-8")))


def test_canonical_arm_registry_passes():
    assert MOD.verify(registry_payload(), constitution_payload()) == []


def test_registry_has_broad_portfolio_but_only_three_deep_arms():
    registry = registry_payload()
    arms = registry["arms"]
    assert len(arms) >= 40
    assert sum(1 for arm in arms if arm["state"] == "ACTIVE_DEEP") == 3


def test_fourth_deep_arm_fails():
    registry = registry_payload()
    candidate = next(arm for arm in registry["arms"] if arm["state"] == "ACTIVE_LIGHT")
    candidate["state"] = "ACTIVE_DEEP"
    assert "ACTIVE_DEEP_WIP" in MOD.verify(registry, constitution_payload())


def test_sixth_agent_cannot_own_an_arm():
    registry = registry_payload()
    registry["arms"][0]["owner"] = "dealix-extra"
    assert "ARM_001_OWNER" in MOD.verify(registry, constitution_payload())


def test_arm_requires_monetization_and_kill_condition():
    registry = registry_payload()
    registry["arms"][0]["monetization"] = []
    registry["arms"][0]["kill_condition"] = ""
    failures = MOD.verify(registry, constitution_payload())
    assert "ARM_001_MONETIZATION" in failures
    assert "ARM_001_KILL_CONDITION" in failures


def test_unknown_engine_fails():
    registry = registry_payload()
    registry["arms"][0]["engine"] = "PARALLEL_COMPANY_ENGINE"
    assert "ARM_001_ENGINE" in MOD.verify(registry, constitution_payload())


def test_constitution_and_registry_wip_must_match():
    constitution = constitution_payload()
    constitution["compression_law"]["deep_wip_max"] = 2
    assert "CONSTITUTION_COMPRESSION_WIP_MATCH" in MOD.verify(registry_payload(), constitution)


def test_arm_ids_are_unique():
    registry = registry_payload()
    registry["arms"][1]["id"] = registry["arms"][0]["id"]
    assert "ARM_IDS_UNIQUE" in MOD.verify(registry, constitution_payload())


def test_all_nine_engines_have_at_least_one_arm():
    registry = registry_payload()
    engines = {arm["engine"] for arm in registry["arms"]}
    assert MOD.ALLOWED_ENGINES <= engines

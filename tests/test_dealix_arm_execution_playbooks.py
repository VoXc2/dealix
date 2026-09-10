from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "scripts" / "commercial" / "verify_dealix_arm_execution_playbooks.py"
PLAYBOOK_PATH = ROOT / "config" / "company" / "dealix_arm_execution_playbooks.json"
REGISTRY_PATH = ROOT / "config" / "company" / "dealix_arm_registry.json"
SPEC = importlib.util.spec_from_file_location("arm_execution_verify", VERIFY_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def playbook_payload() -> dict:
    return copy.deepcopy(json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8")))


def registry_payload() -> dict:
    return copy.deepcopy(json.loads(REGISTRY_PATH.read_text(encoding="utf-8")))


def test_canonical_execution_playbooks_pass():
    assert MOD.verify(playbook_payload(), registry_payload()) == []


def test_playbooks_cover_registry_exactly_once():
    playbooks = playbook_payload()["playbooks"]
    registry = registry_payload()["arms"]
    playbook_ids = [item["arm_id"] for item in playbooks]
    registry_ids = [item["id"] for item in registry]
    assert len(playbook_ids) == len(set(playbook_ids))
    assert set(playbook_ids) == set(registry_ids)


def test_missing_playbook_fails_closed():
    playbooks = playbook_payload()
    playbooks["playbooks"].pop()
    assert "PLAYBOOK_IDS_MATCH_REGISTRY" in MOD.verify(playbooks, registry_payload())


def test_duplicate_playbook_id_fails_closed():
    playbooks = playbook_payload()
    playbooks["playbooks"][1]["arm_id"] = playbooks["playbooks"][0]["arm_id"]
    failures = MOD.verify(playbooks, registry_payload())
    assert "PLAYBOOK_IDS_UNIQUE" in failures
    assert "PLAYBOOK_IDS_MATCH_REGISTRY" in failures


def test_blocked_arm_must_remain_hold():
    playbooks = playbook_payload()
    target = next(item for item in playbooks["playbooks"] if item["arm_id"] == "ARM-042")
    target["horizon"] = "30-90D"
    failures = MOD.verify(playbooks, registry_payload())
    index = playbooks["playbooks"].index(target) + 1
    assert f"PLAYBOOK_{index:03d}_BLOCKED_MUST_HOLD" in failures


def test_active_deep_arms_must_be_now():
    playbooks = playbook_payload()
    target = next(item for item in playbooks["playbooks"] if item["arm_id"] == "ARM-001")
    target["horizon"] = "90-180D"
    failures = MOD.verify(playbooks, registry_payload())
    index = playbooks["playbooks"].index(target) + 1
    assert f"PLAYBOOK_{index:03d}_DEEP_MUST_BE_NOW" in failures


def test_watch_arm_cannot_take_immediate_deep_horizon():
    playbooks = playbook_payload()
    target = next(item for item in playbooks["playbooks"] if item["arm_id"] == "ARM-029")
    target["horizon"] = "NOW-30D"
    failures = MOD.verify(playbooks, registry_payload())
    index = playbooks["playbooks"].index(target) + 1
    assert f"PLAYBOOK_{index:03d}_WATCH_CANNOT_BE_NOW" in failures


def test_p3_arm_cannot_consume_near_term_capacity():
    playbooks = playbook_payload()
    target = next(item for item in playbooks["playbooks"] if item["arm_id"] == "ARM-043")
    target["horizon"] = "30-90D"
    failures = MOD.verify(playbooks, registry_payload())
    index = playbooks["playbooks"].index(target) + 1
    assert f"PLAYBOOK_{index:03d}_P3_HORIZON" in failures


def test_execution_fields_are_required():
    playbooks = playbook_payload()
    playbooks["playbooks"][0]["primary_kpi"] = ""
    playbooks["playbooks"][0]["strategic_dependency"] = ""
    failures = MOD.verify(playbooks, registry_payload())
    assert "PLAYBOOK_001_PRIMARY_KPI" in failures
    assert "PLAYBOOK_001_STRATEGIC_DEPENDENCY" in failures

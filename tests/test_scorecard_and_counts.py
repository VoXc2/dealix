"""Launch Score must be 100 (all gates green) and taxonomy counts must be exact."""
import importlib

import _common as common


def test_launch_score_full():
    sc = importlib.import_module("check_ready_to_launch_scorecard").compute_scorecard()
    assert sc["score"] == 100, [r for r in sc["rows"] if not r["passed"]]
    assert sc["full_launch_ready"] is True


def test_taxonomy_counts():
    needs = common.load_yaml("data/business_need_intelligence/need_taxonomy_25.yaml")["needs"]
    sectors = common.load_yaml("data/business_need_intelligence/sector_need_matrix_20.yaml")["sectors"]
    sprints = common.load_yaml("data/business_need_intelligence/specialized_sprint_library_50.yaml")["sprints"]
    systems = common.load_yaml("data/business_os_catalog/systems.yaml")["systems"]
    packs = common.load_jsonl("data/account_intelligence/account_packs.jsonl")
    assert len(needs) == common.EXPECTED_NEEDS == 25
    assert len(sectors) == common.EXPECTED_SECTORS == 20
    assert len(sprints) == common.EXPECTED_SPRINTS == 50
    assert len(systems) == common.EXPECTED_BUSINESS_SYSTEMS == 40
    assert len(common.core_system_ids()) == common.EXPECTED_CORE_SYSTEMS == 5
    assert len(packs) >= 100  # enough for a Top-100 queue


def test_every_account_pack_has_27_fields():
    packs = common.load_jsonl("data/account_intelligence/account_packs.jsonl")
    for p in packs:
        for field in common.ACCOUNT_PACK_FIELDS:
            assert field in p, f"missing {field}"

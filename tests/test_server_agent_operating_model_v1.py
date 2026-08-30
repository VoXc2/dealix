from __future__ import annotations

from scripts.ops.verify_server_agent_operating_model_v1 import load_manifest, validate_manifest


def test_server_agent_operating_model_is_fail_closed():
    validate_manifest(load_manifest())


def test_all_external_effects_default_false():
    payload = load_manifest()
    assert all(value is False for value in payload["external_effect_defaults"].values())


def test_each_canonical_system_has_one_accountable_lane():
    payload = load_manifest()
    coverage = payload["canonical_system_coverage"]
    assert len(coverage) == 12
    assert len({item["id"] for item in coverage}) == 12
    assert len({item["accountable_owner"] for item in coverage}) == 12


def test_no_parallel_agent_or_scheduler_is_declared():
    payload = load_manifest()
    cadence = payload["cadence_binding"]
    assert cadence["new_permanent_agents"] == 0
    assert cadence["new_timers_or_cron"] == 0
    assert cadence["parallel_scheduler_created"] is False

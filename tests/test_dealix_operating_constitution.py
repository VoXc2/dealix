from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "scripts" / "commercial" / "verify_dealix_operating_constitution.py"
CANONICAL_PATH = ROOT / "config" / "company" / "dealix_operating_constitution.json"
SPEC = importlib.util.spec_from_file_location("constitution_verify", VERIFY_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def valid_payload() -> dict:
    return copy.deepcopy(json.loads(CANONICAL_PATH.read_text(encoding="utf-8")))


def test_valid_contract_passes():
    assert MOD.verify(valid_payload()) == []


def test_v2_fast_compression_is_canonical():
    payload = valid_payload()
    assert payload["constitution_version"] == "2.0-fast-compression"
    assert payload["compression_law"]["compress_time"] is True
    assert payload["compression_law"]["compress_truth"] is False
    assert payload["compression_law"]["deep_wip_max"] == 3
    assert payload["arm_registry"]["path"] == "config/company/dealix_arm_registry.json"


def test_sixth_permanent_agent_fails():
    payload = valid_payload()
    payload["permanent_agents"] = [*MOD.EXPECTED_AGENTS, "dealix-extra"]
    assert "PERMANENT_AGENTS_EXACT" in MOD.verify(payload)


def test_fourth_gtm_wedge_fails():
    payload = valid_payload()
    payload["active_gtm_wedges"] = [*MOD.CURRENT_SEED_WEDGES, "EXTRA_WEDGE"]
    assert "ACTIVE_GTM_WIP" in MOD.verify(payload)


def test_alternative_three_wedge_policy_is_allowed():
    payload = valid_payload()
    payload["active_gtm_wedges"] = ["A", "B", "C"]
    assert MOD.verify(payload) == []


def test_compressing_truth_fails():
    payload = valid_payload()
    payload["compression_law"]["compress_truth"] = True
    assert "NEVER_COMPRESS_TRUTH" in MOD.verify(payload)


def test_deep_wip_above_three_fails():
    payload = valid_payload()
    payload["compression_law"]["deep_wip_max"] = 4
    assert "DEEP_WIP_MAX" in MOD.verify(payload)


def test_missing_arm_registry_link_fails():
    payload = valid_payload()
    payload["arm_registry"]["path"] = "config/company/other.json"
    assert "ARM_REGISTRY_PATH" in MOD.verify(payload)


def test_whatsapp_permission_shortcut_fails():
    payload = valid_payload()
    payload["channel_policy"]["whatsapp"]["discovered_number_is_permission"] = True
    assert "WHATSAPP_DISCOVERY_NOT_PERMISSION" in MOD.verify(payload)


def test_l5_self_authority_fails():
    payload = valid_payload()
    payload["autonomy"]["L5"] = "automatic"
    assert "L5" in MOD.verify(payload)


def test_customer_data_reuse_without_authority_fails():
    payload = valid_payload()
    payload["low_touch_recurring_law"]["no_customer_data_reuse_without_authority"] = False
    assert "NO_DATA_REUSE_WITHOUT_AUTHORITY" in MOD.verify(payload)


def test_unbounded_agent_admin_fails():
    payload = valid_payload()
    payload["interoperability_and_agent_control"]["no_unbounded_shell_or_prod_admin"] = False
    assert "NO_UNBOUNDED_AGENT_ADMIN" in MOD.verify(payload)


def test_deep_build_every_researched_arm_shortcut_is_required():
    payload = valid_payload()
    payload["forbidden_shortcuts"] = [
        item
        for item in payload["forbidden_shortcuts"]
        if "deep-build every researched arm" not in item.lower()
    ]
    assert "FORBID_UNBOUNDED_ARM_BUILD" in MOD.verify(payload)

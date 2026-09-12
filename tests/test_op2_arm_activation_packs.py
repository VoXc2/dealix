"""Truth-law contracts for the OP2 arm activation packs.

These tests are the executable form of the OP2 activation laws:
exactly 44 arms, 20 sectors routed, D0-D2 free, no fixed public prices,
no invented customer/revenue/pipeline, no cold outreach, no L5, and the
ACTIVE_DEEP Top-3 never displaced by research.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "data" / "commercial" / "op2_arm_activation_packs_v1.json"
ROUTES = ROOT / "data" / "commercial" / "op2_sector_diagnostic_routes_v1.json"
REGISTRY = ROOT / "config" / "company" / "dealix_arm_registry.json"
WAVE = ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_arm_activation_packs.py"
    spec = importlib.util.spec_from_file_location("op2_arm_packs", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


packs_mod = _load_module()


def _payload() -> dict:
    return json.loads(PACKS.read_text(encoding="utf-8"))


def _registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_exactly_44_arms_unchanged() -> None:
    registry = _registry()
    assert len(registry["arms"]) == 44
    assert len({a["id"] for a in registry["arms"]}) == 44
    assert len(registry["permanent_agents"]) == 5
    assert registry["deep_wip_max"] == 3


def test_packs_bind_only_existing_arms() -> None:
    registry_ids = {a["id"] for a in _registry()["arms"]}
    for pack in _payload()["packs"]:
        assert pack["arms"], pack["pack_id"]
        for arm in pack["arms"]:
            assert arm in registry_ids, (pack["pack_id"], arm)


def test_all_20_sectors_remain_routed() -> None:
    routes = json.loads(ROUTES.read_text(encoding="utf-8"))
    assert routes["route_count"] == 20
    assert len(routes["routes"]) == 20
    assert len({r["sector_id"] for r in routes["routes"]}) == 20


def test_diagnostics_are_free_no_card_no_roi() -> None:
    for pack in _payload()["packs"]:
        diag = pack["free_diagnostic"]
        assert set(diag["depths"]) <= {"D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"}
        assert diag["card_required"] is False
        assert diag["roi_promised"] is False


def test_no_public_fixed_price() -> None:
    for pack in _payload()["packs"]:
        skeleton = pack["proposal_skeleton"]
        assert skeleton["public_fixed_price"] is False
        assert skeleton["pricing_basis"] == "QUOTE_AFTER_QUALIFIED_DISCOVERY"


def test_no_certification_or_licensed_provider_claims() -> None:
    payload = _payload()
    for pack in payload["packs"]:
        assert pack["certification_claim"] is False
    ob = next(p for p in payload["packs"] if p["pack_id"].endswith("OPEN-BANKING"))
    assert ob["partner_regulatory_boundary"]["licensed_provider_claim"] == "NONE_NEVER"
    cy = next(p for p in payload["packs"] if p["pack_id"].endswith("MARKET-ACCESS-CYBER"))
    assert cy["partner_regulatory_boundary"]["government_access_claim"] == "NONE"
    assert cy["partner_regulatory_boundary"]["accreditation_claim"] == "NONE"


def test_no_invented_customer_pipeline_or_revenue() -> None:
    for pack in _payload()["packs"]:
        assert pack["counts_as_pipeline"] is False
        assert pack["counts_as_revenue"] is False
        assert pack["counts_as_relationship"] is False
        assert pack["truth_class"] == "PATTERN_RESEARCH_PACK"


def test_all_external_effects_false_and_no_l5() -> None:
    payload = _payload()
    assert payload["l5_executed"] == "NONE"
    assert payload["new_arms_created"] == 0
    assert payload["new_permanent_agents_created"] == 0
    for pack in payload["packs"]:
        assert all(v is False for v in pack["external_effects"].values())
        assert pack["authority_all_false"] is True


def test_content_drafts_have_no_publish_authority() -> None:
    for pack in _payload()["packs"]:
        drafts = pack["content_seo_drafts"]
        assert drafts["publish_authority"] is False
        assert drafts["ar_title"] and drafts["en_title"]


def test_research_cannot_displace_active_deep() -> None:
    ranking = _payload()["ranking"]
    assert ranking["arm_count"] == 44
    assert ranking["state_changes_applied"] == 0
    assert [r["arm_id"] for r in ranking["active_deep_locked_top3"]] == ["ARM-001", "ARM-002", "ARM-003"]
    for row in ranking["rows"]:
        assert row["state_change_allowed"] is False
        assert row["disposition"] == "RESEARCH_ONLY_NO_STATE_CHANGE"


def test_official_signals_are_all_false_authority() -> None:
    for pack in _payload()["packs"]:
        assert pack["official_signals"], pack["pack_id"]
        for signal in pack["official_signals"]:
            assert signal["source_ref"].startswith("http")
            assert all(v is False for v in signal["authority"].values())


def test_no_stale_imini_dollar_or_placeholder_hash_as_send_authority() -> None:
    text = PACKS.read_text(encoding="utf-8")
    # No fixed $150 authority and no reused placeholder packet hash may appear.
    assert "$150" not in text
    assert "824a9d8b3caae92d" not in text


def test_wave_signals_remain_contract_research_only() -> None:
    wave = json.loads(WAVE.read_text(encoding="utf-8"))
    assert len(wave["signals"]) >= 12
    for signal in wave["signals"]:
        assert signal["allowed_use"] == ["INTERNAL_RESEARCH_ONLY"]
        assert all(v is False for v in signal["authority"].values())


def test_builder_is_deterministic() -> None:
    rebuilt = packs_mod.build()
    stored = _payload()
    assert [p["pack_id"] for p in rebuilt["packs"]] == [p["pack_id"] for p in stored["packs"]]
    assert rebuilt["ranking"]["arm_count"] == stored["ranking"]["arm_count"]

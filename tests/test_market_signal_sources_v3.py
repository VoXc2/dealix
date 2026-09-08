from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ops" / "verify_market_signal_sources_v3.py"
REGISTRY_PATH = ROOT / "config" / "market" / "market_signal_sources_v3.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("verify_market_signal_sources_v3", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_verifier_passes_current_contract(capsys):
    module = _load_module()
    module.main()
    out = capsys.readouterr().out
    assert "DEALIX_MARKET_SIGNAL_SOURCES_V3=PASS" in out
    assert "source_count=42" in out
    assert "source_family_count=15" in out
    assert "d4_source_count=4" in out
    assert "permanent_agent_count=5" in out
    assert "commercial_authority_from_external_sources=false" in out
    assert "default_relationship_state=RESEARCH_ONLY" in out
    assert "default_consent_state=NOT_PROVEN" in out
    assert "project_cell_required_after=VERIFIED_PAYMENT_OR_EXACT_START_AUTHORITY" in out


def test_required_contract_includes_truth_state_fields():
    module = _load_module()
    assert "relationship_state" in module.REQUIRED_SIGNAL_FIELDS
    assert "consent_state" in module.REQUIRED_SIGNAL_FIELDS
    assert "demand_grade" in module.REQUIRED_SIGNAL_FIELDS
    assert module.ALLOWED_GRADES == {"D1", "D2", "D3", "D4"}


def test_saudi_opportunity_mesh_preserves_core_channels_and_five_agents():
    module = _load_module()
    data = _registry()
    sources = data["sources"]

    assert len(sources) == 42
    assert {source["id"] for source in sources} == module.CORE_SOURCE_IDS
    assert set(data["source_families"]) == module.ALLOWED_SOURCE_FAMILIES
    assert set(data["execution_policy"]["permanent_agents"]) == module.PERMANENT_AGENTS
    assert set(data["execution_policy"]["agent_routes"]) == module.PERMANENT_AGENTS

    routed_agents = {agent for source in sources for agent in source["agent_route"]}
    assert routed_agents == module.PERMANENT_AGENTS


def test_expansion_families_have_explicit_owned_sources():
    data = _registry()
    by_id = {source["id"]: source for source in data["sources"]}

    assert by_id["nupco_tenders"]["lane"] == "HEALTHCARE_PROCUREMENT"
    assert by_id["ntdp_programs"]["lane"] == "GROWTH_ENABLEMENT"
    assert by_id["saudi_exports_incentives"]["lane"] == "EXPORT_MARKET_ACCESS"
    assert by_id["saudi_exports_directory"]["lane"] == "EXPORT_MARKET_ACCESS"

    for source_id in (
        "nhc_procurement_gate",
        "rcu_supplier_portal",
        "jeddah_central_suppliers",
        "diriyah_company_vendors",
    ):
        assert by_id[source_id]["lane"] == "SUPPLIER_NETWORK"

    assert by_id["alat_partnerships"]["lane"] == "TECH_PARTNERSHIP"
    assert by_id["biban_2026"]["lane"] == "EVENT_MARKET_ACCESS"


def test_material_execution_stays_exact_l5_and_sources_stay_research_safe():
    module = _load_module()
    data = _registry()
    execution = data["execution_policy"]

    assert module.REQUIRED_MATERIAL_ACTIONS.issubset(
        set(execution["material_actions_require_exact_l5"])
    )
    assert execution["opportunity_graph_owner"] == "existing_company_machine"
    assert execution["source_registry_owner"] == "PR1555"

    for source in data["sources"]:
        assert source["freshness_hours"] > 0
        assert source["access_mode"]
        assert source["polling_hint"]
        assert source["allowed_outputs"]
        assert source["agent_route"]
        assert set(source["agent_route"]).issubset(module.PERMANENT_AGENTS)
        assert set(source["forbidden_inference"]) & module.FORBIDDEN_AUTHORITY_TERMS


def test_explicit_demand_sources_remain_narrow_and_governed():
    data = _registry()
    d4 = {s["id"] for s in data["sources"] if s["default_grade"] == "D4"}
    assert d4 == {
        "etimad_tenders",
        "aramco_marketplace",
        "sec_ebid",
        "nupco_tenders",
    }
    for source in data["sources"]:
        if source["id"] in d4:
            assert "award" in source["forbidden_inference"]
            assert source["access_mode"]


def test_event_sources_are_explicitly_time_bounded():
    data = _registry()
    events = [s for s in data["sources"] if s["lane"] == "EVENT_MARKET_ACCESS"]
    assert len(events) >= 8
    for source in events:
        assert source["event_window"].count("/") == 1
        start, end = source["event_window"].split("/", 1)
        assert len(start) == 10 and len(end) == 10

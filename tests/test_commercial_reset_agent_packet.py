from __future__ import annotations

import pytest

from dealix.commercial.economic_cell import Sector
from scripts.commercial.commercial_reset_agent_packet import (
    build_daily_packets,
    build_holding_blueprint,
    build_work_packet,
)


CANONICAL_SECTOR_IDS = {sector.value for sector in Sector}


def test_holding_blueprint_is_dynamic_and_legacy_five_is_deprecated() -> None:
    blueprint = build_holding_blueprint()
    assert blueprint["architecture"] == "agentic_holding_sector_company_mesh"
    assert blueprint["legacy_fixed_five_permanent_agents"] == "deprecated"
    assert len(blueprint["group_roles"]) > 5
    assert len(blueprint["sector_role_templates"]) >= 20
    assert {"lead", "scout", "operator", "verifier"} <= set(blueprint["arm_pod_roles"])
    assert blueprint["runtime_workers"] == "lazy_resource_governed"
    assert blueprint["orphan_agents_allowed"] is False


def test_daily_packets_use_resource_governed_holding_dispatch_with_canonical_sectors() -> None:
    payload = build_daily_packets()
    assert payload["dispatch_policy"] == "lazy_resource_governed"
    assert payload["external_effects"] == "exact_action_bound"
    assert len(payload["group_packets"]) > 5
    assert len(payload["sector_company_packets"]) == 6
    assert all(row["safe_to_send"] is False for row in payload["group_packets"])
    assert all("deep_wip_max" not in row for row in payload["group_packets"])
    assert all(row["sector"] in CANONICAL_SECTOR_IDS for row in payload["sector_company_packets"])
    assert all(
        row["agent_identity"] == f"dealix.{row['sector']}.sector-ceo"
        for row in payload["sector_company_packets"]
    )


def test_legacy_sales_alias_resolves_to_group_revenue_role() -> None:
    packet = build_work_packet(
        agent="dealix-sales",
        function="OPPORTUNITY_SCORING",
        opportunity_id="OPP-001",
        entity="Example Co",
        stage="REAL_INTERACTION",
        problem="Slow approval workflow",
        relationship_state="REAL_INTERACTION",
        consent_state="WARM_CONTEXT",
        next_state_sought="QUALIFIED_PROBLEM",
        evidence_refs=["source-1"],
        facts=["Customer described approval delay"],
        inferences=["Delay may affect billing cycle"],
        missing_evidence=["Baseline approval time"],
        urgency="HIGH",
    )
    assert packet["agent_identity"] == "dealix.group.revenue"
    assert packet["agent_parent"] == "dealix.group"
    assert packet["legacy_owner_alias"] == "dealix-sales"
    assert packet["safe_to_send"] is False
    assert "EXACT_COMMERCIAL_APPROVAL" in packet["price_authority"]
    assert packet["pricing_reference_authority"] == "UNVERIFIED_INTERNAL_REFERENCE"
    assert packet["problem_evidence"] == ["source-1"]
    assert "research != relationship" in packet["truth_firewall"]


def test_sector_diagnostic_packet_gets_canonical_sector_parent() -> None:
    packet = build_work_packet(
        layer="sector",
        function="DIAGNOSTIC",
        opportunity_id="OPP-002",
        entity="Contractor Co",
        sector="construction_epc",
        stage="QUALIFIED_PROBLEM",
        problem="RFI and approval delays",
    )
    assert packet["agent_identity"] == "dealix.construction_epc.sector-diagnostic"
    assert packet["agent_parent"] == "dealix.construction_epc"
    assert packet["agent_layer"] == "sector"
    assert packet["agent_role"] == "sector-diagnostic"


def test_arm_proof_packet_gets_canonical_arm_parent() -> None:
    packet = build_work_packet(
        layer="arm",
        function="PROOF",
        opportunity_id="OPP-003",
        entity="Retail Co",
        sector="retail_commerce_ecommerce",
        arm="arm_42_proof_ledger",
        stage="DELIVERY",
        problem="Need source-bound outcome evidence",
    )
    assert packet["agent_identity"] == (
        "dealix.retail_commerce_ecommerce.arm_42_proof_ledger.verifier"
    )
    assert packet["agent_parent"] == (
        "dealix.retail_commerce_ecommerce.arm_42_proof_ledger"
    )
    assert packet["agent_role"] == "verifier"


def test_noncanonical_human_sector_slug_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown canonical sector"):
        build_work_packet(
            layer="sector",
            function="DIAGNOSTIC",
            opportunity_id="OPP-BAD",
            entity="Contractor Co",
            sector="construction-contractors",
            stage="QUALIFIED_PROBLEM",
            problem="RFI and approval delays",
        )


def test_orphan_sector_and_arm_packets_are_rejected() -> None:
    with pytest.raises(ValueError, match="sector is required"):
        build_work_packet(
            layer="sector",
            function="DIAGNOSTIC",
            opportunity_id="OPP-X",
            entity="Example",
            stage="RESEARCH_ONLY",
            problem="Example",
        )
    with pytest.raises(ValueError, match="arm is required"):
        build_work_packet(
            layer="arm",
            function="PROOF",
            opportunity_id="OPP-Y",
            entity="Example",
            sector="technology_saas_si",
            stage="DELIVERY",
            problem="Example",
        )


def test_unknown_legacy_alias_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown legacy owner alias"):
        build_work_packet(
            agent="dealix-random",
            function="OPPORTUNITY_SCORING",
            opportunity_id="OPP-Z",
            entity="Example",
            stage="RESEARCH_ONLY",
            problem="Example",
        )
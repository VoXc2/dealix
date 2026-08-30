#!/usr/bin/env python3
"""Fail-closed verifier for the Dealix Universal Market Radar.

This verifier proves that the radar is a research/playbook input to existing
canonical owners. It must never become a relationship, consent, commercial,
payment, proof, execution, production, scheduler or permanent-agent authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dealix.commercial.portfolio_router import (
    DemandSignal,
    EntryPackage,
    PortfolioPackageRouter,
)

ROOT = Path(__file__).resolve().parents[1]
RADAR_PATH = ROOT / "data/commercial/universal_market_radar_v1.json"
PLAYBOOK_PATH = ROOT / "data/commercial/universal_market_playbooks_v1.json"
CHANNEL_PATH = ROOT / "data/commercial/channel_readiness_registry.json"
WORKLOAD_PATH = ROOT / "data/commercial/agent_council_growth_workloads.json"

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-content",
    "dealix-delivery",
    "dealix-engineer",
}

SECTOR_FAMILIES = {
    "AGRICULTURE_FOOD",
    "ENERGY",
    "HEALTHCARE_LIFE_SCIENCES",
    "ENVIRONMENTAL_SERVICES",
    "MANUFACTURING",
    "PHARMA_BIOTECH",
    "CHEMICALS",
    "REAL_ESTATE",
    "FINANCIAL_SERVICES",
    "TRANSPORT_LOGISTICS",
    "MINING_METALS",
    "TOURISM_QUALITY_OF_LIFE",
    "ICT",
    "HUMAN_CAPITAL_INNOVATION",
    "AVIATION_DEFENSE",
}

CLUSTERS = {
    "PROJECT_ASSET",
    "COMPLEX_B2B_DISTRIBUTION",
    "KNOWLEDGE_DIGITAL",
    "REGULATED_HIGH_TRUST",
    "CONSUMER_MULTI_SITE",
    "FOREIGN_MARKET_ENTRY_PARTNER_LED",
}

AUTHORITY_FIELDS = {
    "relationship",
    "consent",
    "offer",
    "price",
    "quote",
    "contract",
    "external_send",
    "payment",
    "customer_proof",
    "execution",
    "production",
}

REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "kind",
    "authority_class",
    "provenance",
    "freshness_sla_hours",
    "cost_class",
    "policy_risk",
    "access_state",
    "allowed_uses",
    "prohibited_uses",
    "can_create_commercial_authority",
}

REQUIRED_SIGNAL_RECEIPT_FIELDS = {
    "signal_id",
    "source_id",
    "source_ref",
    "observed_at",
    "ingested_at",
    "provenance_ref",
    "fresh_until",
    "signal_family",
    "market",
    "sector_family",
    "business_archetype",
    "evidence_refs",
    "facts",
    "inferences",
    "unknowns",
    "risk_class",
    "allowed_use",
    "next_evidence",
    "authority",
}

SECRET_MARKERS = ("xoxb-", "xapp-", "ghp_", "sk-proj-")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def all_authority_false(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and AUTHORITY_FIELDS.issubset(value)
        and all(value.get(field) is False for field in AUTHORITY_FIELDS)
    )


def verify_static_contracts(errors: list[str]) -> None:
    for path in (RADAR_PATH, PLAYBOOK_PATH, CHANNEL_PATH, WORKLOAD_PATH):
        require(path.exists(), f"missing required file: {path}", errors)
    if errors:
        return

    radar = load_json(RADAR_PATH)
    playbooks = load_json(PLAYBOOK_PATH)
    channels = load_json(CHANNEL_PATH)
    workloads = load_json(WORKLOAD_PATH)

    require(
        radar.get("schema") == "dealix.universal-market-radar.v1",
        "radar schema drift",
        errors,
    )
    require(
        radar.get("scope") == "dealix_company",
        "radar scope must be Dealix company",
        errors,
    )
    require(
        radar.get("objective")
        == "VERIFIED_ECONOMIC_MOVEMENT_PER_FOUNDER_MINUTE_PER_COST_PER_RISK",
        "radar economic objective drift",
        errors,
    )

    integration = radar.get("canonical_integration", {})
    require(
        integration.get("company_brain") == "EXISTING_CANONICAL_OWNER_ONLY",
        "parallel Company Brain must be blocked",
        errors,
    )
    require(
        integration.get("company_autopilot") == "EXISTING_CANONICAL_SCHEDULER_ONLY",
        "radar must reuse canonical scheduler",
        errors,
    )
    require(
        integration.get("portfolio_router") == "dealix/commercial/portfolio_router.py",
        "radar must use canonical portfolio router",
        errors,
    )
    require(
        integration.get("channel_registry")
        == "data/commercial/channel_readiness_registry.json",
        "radar must use canonical channel registry",
        errors,
    )

    hard_truth = radar.get("hard_truth_boundaries", {})
    require(
        hard_truth and all(value is False for value in hard_truth.values()),
        "all radar truth-promotion shortcuts must remain false",
        errors,
    )

    receipt = radar.get("market_signal_receipt_contract", {})
    required_receipt = set(receipt.get("required", []))
    require(
        REQUIRED_SIGNAL_RECEIPT_FIELDS.issubset(required_receipt),
        "MarketSignalReceipt required fields incomplete",
        errors,
    )
    require(
        receipt.get("unknown_literal") == "UNKNOWN_NOT_EVIDENCE_BACKED",
        "unknown literal drift",
        errors,
    )
    require(
        all_authority_false(receipt.get("authority")),
        "MarketSignalReceipt must grant zero downstream authority",
        errors,
    )
    require(
        receipt.get("promotion_owner") == "CANONICAL_DOWNSTREAM_STATE_OWNER_ONLY",
        "signal receipt must not own truth promotion",
        errors,
    )

    signal_ids = {row.get("id") for row in radar.get("signal_families", [])}
    for required in {
        "FIRST_PARTY_INBOUND",
        "EXPLICIT_EMAIL_REPLY",
        "EVENT_OR_FIELD",
        "TENDER_OR_PROCUREMENT",
        "COMPANY_CHANGE",
        "HIRING_OR_ORG_CHANGE",
        "TECHNOLOGY_OR_PLATFORM_CHANGE",
        "COMPETITOR_CHANGE",
        "SEARCH_DEMAND",
        "PARTNER_OR_ECOSYSTEM",
        "REGULATION_OR_POLICY",
        "FIRST_PARTY_OPERATING_TELEMETRY",
        "OFFICIAL_SOCIAL_OR_PAID_REPORTING",
        "CUSTOMER_LEARNING",
    }:
        require(required in signal_ids, f"signal family missing: {required}", errors)

    source_ids: set[str] = set()
    for source in radar.get("source_registry", []):
        require(isinstance(source, dict), "source row must be object", errors)
        if not isinstance(source, dict):
            continue
        missing = REQUIRED_SOURCE_FIELDS - set(source)
        require(
            not missing,
            f"source {source.get('source_id', '<unknown>')} missing fields: {sorted(missing)}",
            errors,
        )
        source_id = str(source.get("source_id", "")).strip()
        require(bool(source_id), "source_id must be non-empty", errors)
        require(source_id not in source_ids, f"duplicate source_id: {source_id}", errors)
        source_ids.add(source_id)
        require(
            isinstance(source.get("freshness_sla_hours"), int)
            and source.get("freshness_sla_hours", 0) > 0,
            f"source {source_id} needs positive freshness SLA",
            errors,
        )
        require(
            source.get("can_create_commercial_authority") is False,
            f"source {source_id} cannot mint commercial authority",
            errors,
        )
        require(
            bool(source.get("provenance")),
            f"source {source_id} needs provenance",
            errors,
        )
        require(
            bool(source.get("allowed_uses")) and bool(source.get("prohibited_uses")),
            f"source {source_id} needs allowed/prohibited uses",
            errors,
        )

    for required in {
        "GASTAT_OFFICIAL",
        "MONSHAAT_OFFICIAL",
        "INVEST_SAUDI_OFFICIAL",
        "ETIMAD_PUBLIC_PROCUREMENT",
        "GOOGLE_SEARCH_CONSOLE",
        "AHREFS",
        "FIRST_PARTY_INBOUND_AND_RELATIONSHIP",
    }:
        require(required in source_ids, f"source registry missing: {required}", errors)

    adapters = radar.get("web_research_adapter_admission", {})
    selected = adapters.get("selected", [])
    maximum = adapters.get("maximum_selected")
    require(isinstance(selected, list), "adapter selected must be a list", errors)
    require(maximum == 1, "web-research adapter maximum must remain one", errors)
    require(
        isinstance(selected, list) and len(selected) <= 1,
        "do not install multiple web-research adapters by default",
        errors,
    )
    require(
        adapters.get("adapter_is_authority_owner") is False,
        "web adapter must not own authority",
        errors,
    )

    channel_registry = channels.get("channels", {})
    require(isinstance(channel_registry, dict), "canonical channels missing", errors)
    for family in radar.get("channel_intelligence", {}).get("families", []):
        for channel in family.get("channels", []):
            require(
                channel in channel_registry,
                f"radar channel must exist in canonical registry: {channel}",
                errors,
            )
    blocked = set(radar.get("channel_intelligence", {}).get("blocked_patterns", []))
    for phrase in {
        "personal LinkedIn scraping or auto-DM",
        "cold WhatsApp blasting",
        "generic scraping-to-pipeline promotion",
    }:
        require(phrase in blocked, f"blocked channel pattern missing: {phrase}", errors)

    agent_routing = radar.get("canonical_agent_routing", {})
    require(
        set(agent_routing) == CANONICAL_AGENTS,
        "radar must route only to the five canonical agents",
        errors,
    )
    require(
        radar.get("new_permanent_agent_created") is False,
        "new permanent agent must remain false",
        errors,
    )
    require(
        radar.get("new_scheduler_created") is False,
        "new scheduler must remain false",
        errors,
    )

    cadence = workloads.get("workload_cadence", {})
    require(
        cadence.get("new_timer_created") is False,
        "existing workload owner unexpectedly declares new timer",
        errors,
    )
    require(
        cadence.get("new_permanent_agent_created") is False,
        "existing workload owner unexpectedly declares new permanent agent",
        errors,
    )

    scoring = radar.get("priority_scoring", {})
    require(
        scoring.get("score_is_purchase_probability") is False,
        "priority score must not equal purchase probability",
        errors,
    )
    require(
        scoring.get("score_may_promote_relationship_or_opportunity") is False,
        "priority score must not promote relationship/opportunity truth",
        errors,
    )

    freshness = radar.get("freshness_and_expiry", {})
    require(
        freshness.get("stale_signal_may_trigger_external_action") is False,
        "stale signals must not trigger external actions",
        errors,
    )
    require(
        freshness.get("stale_signal_may_promote_commercial_truth") is False,
        "stale signals must not promote commercial truth",
        errors,
    )

    experiment = radar.get("experiment_contract", {})
    require(
        set(experiment.get("verdicts", [])) == {"SCALE", "ITERATE", "STOP", "INVALID"},
        "experiment verdict contract drift",
        errors,
    )
    require(
        experiment.get("external_mutation_authority") is False,
        "experiment contract must not grant external mutation",
        errors,
    )
    require(
        experiment.get("vanity_metric_only_may_scale") is False,
        "vanity-only experiments must not scale",
        errors,
    )

    autopilot = radar.get("autopilot_consumption", {})
    require(
        autopilot.get("mode") == "READ_ONLY_REGISTRY_INPUT_TO_EXISTING_RUNNERS",
        "radar must be read-only input to existing runners",
        errors,
    )
    require(autopilot.get("new_timer") is False, "autopilot may not add timer", errors)
    require(
        autopilot.get("outbound_or_spend_enabled") is False,
        "radar may not enable outbound or spend",
        errors,
    )
    require(
        all_authority_false(radar.get("global_authority")),
        "radar global authority must remain all false",
        errors,
    )

    require(
        playbooks.get("schema") == "dealix.universal-market-playbooks.v1",
        "playbook schema drift",
        errors,
    )
    sectors = playbooks.get("sector_families", [])
    sector_ids = {row.get("id") for row in sectors if isinstance(row, dict)}
    require(sector_ids == SECTOR_FAMILIES, "15-sector universe incomplete or drifted", errors)
    cluster_ids = {row.get("cluster") for row in sectors if isinstance(row, dict)}
    require(
        cluster_ids.issubset(CLUSTERS - {"FOREIGN_MARKET_ENTRY_PARTNER_LED"}),
        "sector family mapped to unknown cluster",
        errors,
    )
    playbook_clusters = set(playbooks.get("cluster_playbooks", {}))
    require(
        playbook_clusters == CLUSTERS,
        "all six operating cluster playbooks are required",
        errors,
    )

    demand_rows = playbooks.get("demand_to_package_playbooks", [])
    demand_map = {
        row.get("demand"): row.get("primary_route")
        for row in demand_rows
        if isinstance(row, dict)
    }
    for demand in {
        "AI_OR_AI_STRATEGY",
        "AUTOMATION_OR_WORKFLOW",
        "COMPANY_KNOWLEDGE_OR_COMPANY_BRAIN",
        "AI_AGENTS_OR_COPILOTS",
        "DECISION_INTELLIGENCE",
        "TENDER_RFP_PROPOSAL_INTELLIGENCE",
        "CUSTOMER_OPERATIONS",
    }:
        require(
            demand_map.get(demand) == "COMPANY_BRAIN_GOVERNED_AI_SPRINT",
            f"technical demand must map to Company Brain Sprint hypothesis: {demand}",
            errors,
        )
    require(
        demand_map.get("REVENUE_SALES_REVOPS") == "REVENUE_COMMAND_PILOT",
        "RevOps demand must map to Revenue Command hypothesis",
        errors,
    )
    require(
        demand_map.get("SAUDI_MARKET_ENTRY") == "SAUDI_MARKET_ACCESS_SPRINT",
        "pure Saudi market-entry demand must preserve Market Access package ownership",
        errors,
    )
    require(
        demand_map.get("PARTNER_IMPLEMENTATION_OR_WHITE_LABEL")
        == "PARTNER_IMPLEMENTATION_PROOF_LAYER",
        "partner demand must preserve Partner Layer ownership",
        errors,
    )

    workflow_packs = set(playbooks.get("company_brain_workflow_packs", {}))
    require(
        workflow_packs
        == {
            "EXECUTIVE_KNOWLEDGE",
            "SALES_AND_CRM_INTELLIGENCE",
            "SUPPORT_AND_OPS",
            "DOCUMENT_TENDER_AND_PROPOSAL_INTELLIGENCE",
            "FINANCE_AND_ADMIN",
            "ENGINEERING_AND_IT",
        },
        "Company Brain workflow pack registry drift",
        errors,
    )

    rules = playbooks.get("playbook_rules", {})
    require(rules.get("fixed_public_price_authority") is False, "fixed pricing must remain false", errors)
    require(
        rules.get("one_named_outcome_required_for_company_brain_sprint") is True,
        "Company Brain Sprint must remain bounded to one named outcome",
        errors,
    )
    for field in (
        "external_send_or_publish_authority",
        "payment_or_spend_authority",
        "production_mutation_authority",
    ):
        require(rules.get(field) is False, f"playbook authority drift: {field}", errors)

    joined = RADAR_PATH.read_text(encoding="utf-8") + PLAYBOOK_PATH.read_text(encoding="utf-8")
    for marker in SECRET_MARKERS:
        require(marker not in joined, f"secret-like token marker found: {marker}", errors)


def verify_router_alignment(errors: list[str]) -> None:
    router = PortfolioPackageRouter()

    research_ai = router.route(
        DemandSignal(
            signal_id="radar-research-ai",
            company_name="Research AI Co",
            source_ref="public://company/research-ai",
            observed_at="2026-08-29T10:00:00+00:00",
            evidence_refs=["evidence://public/research-ai"],
            explicit_inbound_ref="raw-ref-without-canonical-state",
            problem_tags=["ai", "automation"],
            urgency="MEDIUM",
            economic_relevance="MEDIUM",
            risk_class="STANDARD",
        )
    )
    require(
        research_ai.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS,
        "raw research/reference must remain research-only",
        errors,
    )
    require(research_ai.status == "RESEARCH_ONLY", "research signal status drift", errors)
    require(
        not any(research_ai.authority.values()),
        "research signal unexpectedly received authority",
        errors,
    )

    inbound_ai = router.route(
        DemandSignal(
            signal_id="radar-inbound-ai",
            company_name="Inbound AI Co",
            source_ref="inbound://website/ai-request",
            observed_at="2026-08-29T10:05:00+00:00",
            evidence_refs=["evidence://inbound/ai-request"],
            real_interaction_state="EXPLICIT_INBOUND",
            explicit_inbound_ref="inbound://message/1",
            consent_state="CONSENTED",
            problem_statement="We need AI automation and a company knowledge brain.",
            problem_tags=["ai", "automation", "company_brain"],
            requested_capabilities=["agents", "knowledge", "workflow"],
            urgency="HIGH",
            economic_relevance="HIGH",
            risk_class="STANDARD",
        )
    )
    require(
        inbound_ai.recommended_package == EntryPackage.COMPANY_BRAIN,
        "legitimate technical inbound must route to Company Brain Sprint hypothesis",
        errors,
    )
    require(
        inbound_ai.authority_class == "PACKAGE_HYPOTHESIS_ONLY",
        "Company Brain route must remain package hypothesis only",
        errors,
    )
    require(
        not any(inbound_ai.authority.values()),
        "Company Brain route unexpectedly granted downstream authority",
        errors,
    )

    inbound_market = router.route(
        DemandSignal(
            signal_id="radar-inbound-market-entry",
            company_name="Inbound Market Co",
            source_ref="inbound://website/ksa-entry",
            observed_at="2026-08-29T10:10:00+00:00",
            evidence_refs=["evidence://inbound/ksa-entry"],
            real_interaction_state="EXPLICIT_INBOUND",
            explicit_inbound_ref="inbound://message/2",
            consent_state="CONSENTED",
            problem_statement="We need to enter the Saudi market and map local partners.",
            ksa_market_entry_intent=True,
            urgency="HIGH",
            economic_relevance="HIGH",
            risk_class="STANDARD",
        )
    )
    require(
        inbound_market.recommended_package == EntryPackage.SAUDI_MARKET_ACCESS,
        "pure market-entry demand must route to Saudi Market Access hypothesis",
        errors,
    )
    require(not any(inbound_market.authority.values()), "market-entry route granted authority", errors)

    multi_family = router.route(
        DemandSignal(
            signal_id="radar-inbound-market-ai",
            company_name="Inbound Mixed Co",
            source_ref="inbound://website/mixed",
            observed_at="2026-08-29T10:15:00+00:00",
            evidence_refs=["evidence://inbound/mixed"],
            real_interaction_state="EXPLICIT_INBOUND",
            explicit_inbound_ref="inbound://message/3",
            consent_state="CONSENTED",
            problem_statement="We need Saudi market entry plus an AI agent workflow.",
            problem_tags=["ai", "agent"],
            ksa_market_entry_intent=True,
            urgency="HIGH",
            economic_relevance="HIGH",
            risk_class="STANDARD",
        )
    )
    require(
        multi_family.recommended_package == EntryPackage.DIAGNOSTIC_DISCOVERY,
        "multi-family demand must route to Diagnostic/Discovery for scope resolution",
        errors,
    )
    require(not any(multi_family.authority.values()), "multi-family route granted authority", errors)

    suppressed = router.route(
        DemandSignal(
            signal_id="radar-suppressed",
            company_name="Suppressed Co",
            source_ref="inbound://website/suppressed",
            observed_at="2026-08-29T10:20:00+00:00",
            evidence_refs=["evidence://inbound/suppressed"],
            real_interaction_state="EXPLICIT_INBOUND",
            explicit_inbound_ref="inbound://message/4",
            consent_state="SUPPRESSED",
            problem_tags=["automation"],
            urgency="MEDIUM",
            economic_relevance="MEDIUM",
            risk_class="STANDARD",
        )
    )
    require(suppressed.status == "SUPPRESSED", "suppression must override package routing", errors)
    require(not any(suppressed.authority.values()), "suppressed signal granted authority", errors)


def main() -> int:
    errors: list[str] = []
    verify_static_contracts(errors)
    if not errors:
        verify_router_alignment(errors)

    if errors:
        print("DEALIX_UNIVERSAL_MARKET_RADAR_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("DEALIX_UNIVERSAL_MARKET_RADAR_VERDICT=PASS")
    print("UNIVERSAL_CORE_VERTICAL_PLAYBOOKS=PASS")
    print("SOURCE_PROVENANCE_FRESHNESS_AUTHORITY=PASS")
    print("FIVE_CANONICAL_AGENT_ROUTING=PASS")
    print("NEW_SCHEDULER=NO")
    print("NEW_PERMANENT_AGENT_FLEET=NO")
    print("SIGNAL_SELF_PROMOTION=BLOCKED")
    print("COMPANY_BRAIN_TECHNICAL_DEMAND_ROUTE=BOUNDED_HYPOTHESIS_ONLY")
    print("MARKET_ENTRY_ROUTE=SAUDI_MARKET_ACCESS_UNLESS_MULTI_FAMILY_DISCOVERY")
    print("EXTERNAL_SEND_SPEND_PAYMENT_PRODUCTION_AUTHORITY=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

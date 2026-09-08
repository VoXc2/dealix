#!/usr/bin/env python3
"""Fail-closed verifier for Dealix Market Signal Source Registry V3."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "config" / "market" / "market_signal_sources_v3.json"

ALLOWED_GRADES = {"D1", "D2", "D3", "D4"}
PERMANENT_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
ALLOWED_SOURCE_FAMILIES = {
    "B2G_PROCUREMENT",
    "PPP_PRIVATIZATION",
    "PIF_PRIVATE_SECTOR",
    "SUPPLIER_NETWORK",
    "CONSTRUCTION_PROJECTS",
    "REGULATORY_TRIGGER",
    "INDUSTRIAL_DIGITIZATION",
    "ENERGY_INDUSTRIAL_PROCUREMENT",
    "TECH_PARTNERSHIP",
    "EVENT_MARKET_ACCESS",
    "PUBLIC_COMPANY_ECONOMIC_SIGNAL",
    "TRUST_PROVIDER_AUTHORITY",
}
CORE_SOURCE_IDS = {
    "etimad_tenders",
    "ncp_ppp",
    "pif_company_opportunities",
    "pif_musahama",
    "monshaat_jadeer",
    "muqawil_market",
    "muqawil_consortium",
    "misa_matchmaking",
    "zatca_wave25",
    "sidf_future_factories",
    "neom_suppliers",
    "red_sea_global_vendors",
    "qiddiya_vendors",
    "new_murabba_vendors",
    "roshn_partnerships",
    "aramco_suppliers",
    "aramco_marketplace",
    "maaden_supplier_portal",
    "sec_vendor_registration",
    "sec_ebid",
    "sabic_supplier_portal",
    "riyadh_air_mar",
    "saudi_exchange_announcements",
    "smart_cities_saudi_expo",
    "hotel_hospitality_expo_saudi",
    "rega_proptech_hub",
    "saudi_build_2026",
    "cityscape_global_2026",
    "global_logistics_forum_2026",
    "future_projects_forum_2026",
    "nca_ai_cybersecurity",
    "railway_docs",
}
REQUIRED_SOURCE_FIELDS = {
    "id",
    "name",
    "url",
    "lane",
    "default_grade",
    "purpose",
    "allowed_outputs",
    "forbidden_inference",
    "freshness_hours",
    "access_mode",
    "polling_hint",
    "agent_route",
}
REQUIRED_SIGNAL_FIELDS = {
    "source_id",
    "source_url",
    "observed_at",
    "entity",
    "event",
    "evidence_excerpt_or_digest",
    "freshness",
    "sector",
    "geography",
    "demand_grade",
    "relationship_state",
    "consent_state",
    "confidence",
    "next_safe_action",
}
FORBIDDEN_AUTHORITY_TERMS = {
    "buyer_intent",
    "relationship",
    "consent",
}
REQUIRED_MATERIAL_ACTIONS = {
    "tender_submission",
    "external_send",
    "binding_quote",
    "contract_signature",
    "paid_spend",
    "production_mutation",
    "customer_system_release",
}


def _fail(message: str) -> None:
    raise SystemExit(f"DEALIX_MARKET_SIGNAL_SOURCES_V3=FAIL: {message}")


def main() -> None:
    if not REGISTRY.is_file():
        _fail(f"missing registry: {REGISTRY}")

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive boundary
        _fail(f"invalid JSON: {exc}")

    if data.get("schema_version") != 3:
        _fail("schema_version must be 3")
    if data.get("north_star") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY":
        _fail("north_star drift")

    authority = data.get("authority") or {}
    expected_truth_guards = {
        "source_registry_is_not_opportunity_graph": True,
        "research_is_not_relationship": True,
        "public_contact_is_not_consent": True,
        "signal_is_not_buyer_intent": True,
        "external_sources_may_not_self_create_commercial_authority": True,
    }
    for key, expected in expected_truth_guards.items():
        if authority.get(key) is not expected:
            _fail(f"authority guard {key} must be {expected}")

    grades = data.get("demand_grades") or {}
    if set(grades) != ALLOWED_GRADES:
        _fail("demand_grades must contain exactly D1-D4")

    source_families = set(data.get("source_families") or [])
    if source_families != ALLOWED_SOURCE_FAMILIES:
        missing = sorted(ALLOWED_SOURCE_FAMILIES - source_families)
        extra = sorted(source_families - ALLOWED_SOURCE_FAMILIES)
        _fail(f"source family drift missing={missing} extra={extra}")

    execution = data.get("execution_policy") or {}
    if execution.get("mode") != "RESEARCH_WIDE_SELECT_NARROW_DELIVER_DEEPLY":
        _fail("execution mode must remain RESEARCH_WIDE_SELECT_NARROW_DELIVER_DEEPLY")
    if execution.get("source_registry_owner") != "PR1555":
        _fail("source registry owner must remain PR1555")
    if execution.get("opportunity_graph_owner") != "existing_company_machine":
        _fail("opportunity graph must remain owned by existing company machine")
    if set(execution.get("permanent_agents") or []) != PERMANENT_AGENTS:
        _fail("permanent agent set must remain exactly the canonical five")
    if execution.get("project_cell_required_after") != "VERIFIED_PAYMENT_OR_EXACT_START_AUTHORITY":
        _fail("project cell start authority contract drift")

    material_actions = set(execution.get("material_actions_require_exact_l5") or [])
    if not REQUIRED_MATERIAL_ACTIONS.issubset(material_actions):
        missing = sorted(REQUIRED_MATERIAL_ACTIONS - material_actions)
        _fail(f"missing exact-L5 material actions: {missing}")

    agent_routes = execution.get("agent_routes") or {}
    if set(agent_routes) != PERMANENT_AGENTS:
        _fail("agent route map must contain exactly the canonical five agents")
    for agent, duties in agent_routes.items():
        if not isinstance(duties, list) or not duties or not all(str(x).strip() for x in duties):
            _fail(f"agent {agent} must have at least one bounded duty")

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        _fail("sources must be a non-empty list")
    if len(sources) < len(CORE_SOURCE_IDS):
        _fail(f"source mesh unexpectedly narrowed: {len(sources)} < {len(CORE_SOURCE_IDS)}")

    seen_ids: set[str] = set()
    observed_families: set[str] = set()
    observed_agents: set[str] = set()
    d4_count = 0
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            _fail(f"source[{index}] must be an object")
        missing = sorted(REQUIRED_SOURCE_FIELDS - set(source))
        if missing:
            _fail(f"source[{index}] missing fields: {','.join(missing)}")

        source_id = str(source["id"]).strip()
        if not source_id or source_id in seen_ids:
            _fail(f"source id invalid/duplicate: {source_id!r}")
        seen_ids.add(source_id)

        lane = source.get("lane")
        if lane not in ALLOWED_SOURCE_FAMILIES:
            _fail(f"source {source_id} has invalid lane {lane!r}")
        observed_families.add(lane)

        if source["default_grade"] not in ALLOWED_GRADES:
            _fail(f"source {source_id} has invalid demand grade")
        if source["default_grade"] == "D4":
            d4_count += 1

        if not str(source["url"]).startswith("https://"):
            _fail(f"source {source_id} must use https URL")
        if not isinstance(source["freshness_hours"], int) or source["freshness_hours"] <= 0:
            _fail(f"source {source_id} freshness_hours must be positive int")
        if not str(source.get("access_mode") or "").strip():
            _fail(f"source {source_id} access_mode must be explicit")
        if not str(source.get("polling_hint") or "").strip():
            _fail(f"source {source_id} polling_hint must be explicit")

        allowed_outputs = source.get("allowed_outputs") or []
        if not isinstance(allowed_outputs, list) or not allowed_outputs:
            _fail(f"source {source_id} allowed_outputs must be non-empty")

        forbidden = set(source.get("forbidden_inference") or [])
        if not (forbidden & FORBIDDEN_AUTHORITY_TERMS):
            _fail(
                f"source {source_id} must explicitly forbid at least one commercial-authority inference"
            )

        routes = source.get("agent_route") or []
        if not isinstance(routes, list) or not routes:
            _fail(f"source {source_id} must route to at least one canonical agent")
        unknown_agents = set(routes) - PERMANENT_AGENTS
        if unknown_agents:
            _fail(f"source {source_id} routes to non-canonical agents: {sorted(unknown_agents)}")
        observed_agents.update(routes)

        event_window = source.get("event_window")
        if event_window is not None:
            if lane != "EVENT_MARKET_ACCESS":
                _fail(f"source {source_id} has event_window outside EVENT_MARKET_ACCESS")
            if not isinstance(event_window, str) or "/" not in event_window:
                _fail(f"source {source_id} event_window must be YYYY-MM-DD/YYYY-MM-DD")

    missing_core = sorted(CORE_SOURCE_IDS - seen_ids)
    if missing_core:
        _fail(f"core Saudi opportunity sources missing: {missing_core}")
    if observed_families != ALLOWED_SOURCE_FAMILIES:
        _fail("every declared source family must have at least one source")
    if observed_agents != PERMANENT_AGENTS:
        _fail("the complete mesh must exercise all five permanent agents")
    if d4_count < 3:
        _fail("mesh must preserve multiple explicit-demand D4 intake channels")

    contract = data.get("signal_contract") or {}
    required_fields = set(contract.get("required_fields") or [])
    if required_fields != REQUIRED_SIGNAL_FIELDS:
        missing = sorted(REQUIRED_SIGNAL_FIELDS - required_fields)
        extra = sorted(required_fields - REQUIRED_SIGNAL_FIELDS)
        _fail(f"signal contract drift missing={missing} extra={extra}")

    if contract.get("default_relationship_state") != "RESEARCH_ONLY":
        _fail("default relationship state must remain RESEARCH_ONLY")
    if contract.get("default_consent_state") != "NOT_PROVEN":
        _fail("default consent state must remain NOT_PROVEN")

    print("DEALIX_MARKET_SIGNAL_SOURCES_V3=PASS")
    print(f"source_count={len(sources)}")
    print(f"source_family_count={len(source_families)}")
    print(f"d4_source_count={d4_count}")
    print("permanent_agent_count=5")
    print("commercial_authority_from_external_sources=false")
    print("default_relationship_state=RESEARCH_ONLY")
    print("default_consent_state=NOT_PROVEN")
    print("project_cell_required_after=VERIFIED_PAYMENT_OR_EXACT_START_AUTHORITY")


if __name__ == "__main__":
    main()

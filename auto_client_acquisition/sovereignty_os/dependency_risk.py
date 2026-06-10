"""Dependency risk map — each risk class needs an explicit control."""

from __future__ import annotations

# dependency_key -> required control capability id (must be present in active_controls)
DEPENDENCY_REQUIRED_CONTROLS: dict[str, str] = {
    "single_llm_provider": "llm_gateway_model_router",
    "founder_delivery_only": "delivery_os_checklists",
    "custom_projects_agency_trap": "productized_offers",
    "weak_data_sources": "source_passport",
    "unsafe_automation": "governance_runtime",
    "one_sales_channel": "partner_academy_distribution",
    "one_client_segment": "portfolio_strategy",
    "no_proof": "proof_pack_standard",
    "no_capital_capture": "capital_ledger",
}


def dependency_mitigated(dependency: str, active_controls: frozenset[str]) -> bool:
    req = DEPENDENCY_REQUIRED_CONTROLS.get(dependency)
    if req is None:
        msg = f"unknown dependency key: {dependency}"
        raise ValueError(msg)
    return req in active_controls


def all_listed_dependencies_mitigated(active_controls: frozenset[str]) -> bool:
    return all(
        ctl in active_controls for ctl in DEPENDENCY_REQUIRED_CONTROLS.values()
    )

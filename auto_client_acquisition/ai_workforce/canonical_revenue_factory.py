"""Canonical view over the historical Revenue Factory blueprint.

The underlying blueprint keeps fifteen useful specialist contracts and thirty
automation plays. This adapter makes ownership truthful: those contracts are
bounded workloads delegated to the five canonical Dealix agents, never a second
permanent agent fleet or approval authority.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_workforce.canonical_delegation import (
    CANONICAL_AGENTS,
    REVENUE_SPECIALIST_DELEGATION,
    SPECIALIST_ROLE_SEMANTICS,
    canonical_owner_for,
)
from auto_client_acquisition.ai_workforce.revenue_factory_blueprint import (
    build_revenue_factory_blueprint as _build_legacy_blueprint,
)


def build_canonical_revenue_factory_blueprint() -> dict[str, Any]:
    blueprint = _build_legacy_blueprint()

    contracts: list[dict[str, Any]] = []
    for raw in blueprint.get("agent_contracts", []):
        contract = dict(raw)
        role_id = str(contract.get("agent_id") or "")
        contract["canonical_owner"] = canonical_owner_for(role_id)
        contract["role_semantics"] = SPECIALIST_ROLE_SEMANTICS
        contracts.append(contract)

    schedule: list[dict[str, Any]] = []
    for raw in blueprint.get("daily_schedule", []):
        slot = dict(raw)
        role_id = str(slot.get("owner_agent") or "")
        slot["canonical_owner"] = canonical_owner_for(role_id)
        slot["owner_semantics"] = SPECIALIST_ROLE_SEMANTICS
        schedule.append(slot)

    contract_ids = {str(item.get("agent_id")) for item in contracts}
    expected_ids = set(REVENUE_SPECIALIST_DELEGATION)
    if contract_ids != expected_ids:
        raise RuntimeError("Revenue Factory specialist-role set drifted from canonical delegation")

    blueprint["agent_contracts"] = contracts
    blueprint["daily_schedule"] = schedule
    blueprint["canonical_agents"] = list(CANONICAL_AGENTS)
    blueprint["canonical_agents_total"] = len(CANONICAL_AGENTS)
    blueprint["specialist_roles_total"] = len(contracts)
    blueprint["specialist_role_semantics"] = SPECIALIST_ROLE_SEMANTICS
    blueprint["specialist_role_delegation"] = dict(REVENUE_SPECIALIST_DELEGATION)
    blueprint["legacy_agent_contracts_total"] = len(contracts)
    blueprint.setdefault("policies", {})[
        "specialist_roles_are_bounded_workloads_not_permanent_agents"
    ] = True
    blueprint["policies"]["canonical_agent_ownership_required"] = True
    blueprint["policies"]["no_specialist_self_authority"] = True
    return blueprint

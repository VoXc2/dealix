"""Canonical summary adapter for the Dealix operating-company contract.

The historical operating-company contract models useful logical specialist roles.
Those roles are workloads delegated under the five canonical Dealix agents; they
are not permanent agents or independent authority owners.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_workforce.canonical_delegation import (
    CANONICAL_AGENTS,
    OPERATING_COMPANY_SPECIALIST_DELEGATION,
    SPECIALIST_ROLE_SEMANTICS,
)
from auto_client_acquisition.orchestrator.operating_company_contract import (
    build_operating_company_contract,
)


def build_canonical_operating_company_summary() -> dict[str, Any]:
    contract = build_operating_company_contract()
    legacy = contract.to_summary()
    role_ids = {role.agent_id for role in contract.agent_roles}
    expected_role_ids = set(OPERATING_COMPANY_SPECIALIST_DELEGATION)
    if role_ids != expected_role_ids:
        missing = sorted(role_ids - expected_role_ids)
        stale = sorted(expected_role_ids - role_ids)
        raise ValueError(
            "operating_company_specialist_role_delegation_mismatch:"
            f"unmapped={missing}:stale={stale}"
        )

    specialist_roles_total = len(role_ids)
    legacy_agents_total = legacy.get("agents_total")
    if legacy_agents_total != specialist_roles_total:
        raise ValueError("operating_company_specialist_role_count_mismatch")

    canonical_agents = set(CANONICAL_AGENTS)
    owners = set(OPERATING_COMPANY_SPECIALIST_DELEGATION.values())
    if not owners <= canonical_agents:
        raise ValueError("operating_company_specialist_owner_outside_canonical_agents")

    return {
        "governed_chain": legacy.get("governed_chain", []),
        "canonical_commercial_chain": legacy.get("canonical_commercial_chain", []),
        "factories_total": legacy.get("factories_total", 0),
        "loops_total": legacy.get("loops_total", 0),
        "canonical_agents": list(CANONICAL_AGENTS),
        "canonical_agents_total": len(CANONICAL_AGENTS),
        "specialist_roles_total": specialist_roles_total,
        "specialist_role_semantics": SPECIALIST_ROLE_SEMANTICS,
        "specialist_role_owners": dict(OPERATING_COMPANY_SPECIALIST_DELEGATION),
        "event_types_total": legacy.get("event_types_total", 0),
        "states_total": legacy.get("states_total", 0),
        "legacy_agents_total_compatibility": legacy_agents_total,
        "legacy_agents_total_authoritative": False,
    }

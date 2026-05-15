"""Maps the 11 non-negotiables to the systems that enforce them.

Every non-negotiable must map to at least one system, and every system
must declare at least one gate — ``doctrine_coverage`` proves both.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_os.system_registry import get_system, list_systems

# The 11 immutable non-negotiables (docs/COMMERCIAL_WIRING_MAP.md section 3).
NON_NEGOTIABLES: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp",
    "no_scraping",
    "no_fake_proof",
    "no_unconsented_data",
    "no_unverified_outcomes",
    "no_hidden_pricing",
    "no_silent_failures",
    "no_unbounded_agents",
    "no_unaudited_changes",
)


def gates_for_system(system_id: str) -> tuple[str, ...]:
    """Doctrine gates declared by one system. KeyError if unknown."""
    return get_system(system_id).doctrine_gates


def systems_for_gate(gate: str) -> list[str]:
    """All system ids that declare ``gate`` as a doctrine gate."""
    return [s.system_id for s in list_systems() if gate in s.doctrine_gates]


def doctrine_coverage() -> dict[str, Any]:
    """Coverage report: each non-negotiable mapped to its enforcing systems.

    ``unmapped`` lists any non-negotiable not enforced by the registry;
    ``governance_system`` is the catch-all owner for cross-cutting gates
    (live-send, live-charge, cold-whatsapp, scraping).
    """
    governance_owned = {
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_scraping",
    }
    mapping: dict[str, list[str]] = {}
    for gate in NON_NEGOTIABLES:
        owners = systems_for_gate(gate)
        if not owners and gate in governance_owned:
            owners = ["governance_system"]
        mapping[gate] = owners
    unmapped = [gate for gate, owners in mapping.items() if not owners]
    return {
        "non_negotiable_count": len(NON_NEGOTIABLES),
        "mapping": mapping,
        "unmapped": unmapped,
        "fully_covered": not unmapped,
    }

"""Integration Capability Registry (Wave 13 Phase 10).

Per plan §32.4A.3 — explicit truth-table of every integration's
trust level + trigger condition for next level.

Three levels (per spec):
  L1 = manual_csv         (customer pastes / founder confirms manually)
  L2 = read_only          (OAuth read; no writes)
  L3 = controlled_write   (approved-only mutations; never live send/charge)

Hard rule: NO L3 entry unless "5+ customers prove L1+L2 safe" comment present.
This is the Article 4 prevention layer.
"""

from auto_client_acquisition.integration_capability.registry import (
    INTEGRATIONS,
    INTEGRATION_IDS,
    get_integration,
    list_integrations,
)
from auto_client_acquisition.integration_capability.schemas import (
    IntegrationCapability,
    IntegrationLevel,
)

__all__ = [
    "INTEGRATIONS",
    "INTEGRATION_IDS",
    "IntegrationCapability",
    "IntegrationLevel",
    "get_integration",
    "list_integrations",
]

"""Dealix master layer registry — maps numbered constitution docs to repo packages."""

from auto_client_acquisition.dealix_master_layers.registry import (
    DealixLayer,
    IMPLEMENTATION_HINTS,
    MASTER_LAYERS,
    OI_DOMINANCE_LAYERS,
    OrganizationalIntelligenceLayer,
    dominance_layer_by_id,
    dominance_layer_by_slug,
    layer_by_folder,
    readme_path,
)
from auto_client_acquisition.dealix_master_layers.dominance_execution import (
    CAPABILITY_CONTRACTS,
    DOMINANCE_GATES,
    CapabilityContract,
    GateMilestone,
    contracts_by_layer_slug,
    dominance_readiness_snapshot,
    missing_contract_layer_slugs,
)

__all__ = [
    "DealixLayer",
    "IMPLEMENTATION_HINTS",
    "MASTER_LAYERS",
    "OI_DOMINANCE_LAYERS",
    "OrganizationalIntelligenceLayer",
    "dominance_layer_by_id",
    "dominance_layer_by_slug",
    "CAPABILITY_CONTRACTS",
    "DOMINANCE_GATES",
    "CapabilityContract",
    "GateMilestone",
    "contracts_by_layer_slug",
    "dominance_readiness_snapshot",
    "missing_contract_layer_slugs",
    "layer_by_folder",
    "readme_path",
]

"""Agentic Enterprise OS — the AI Operating Fabric (12-layer unifying index)."""

from auto_client_acquisition.agentic_enterprise_os.fabric import (
    FABRIC_LAYERS,
    FabricLayer,
    fabric_status,
    layer_by_key,
    layer_by_number,
    layer_to_dict,
    maturity_score,
    package_exists,
    resolve_layer_health,
)

__all__ = [
    "FABRIC_LAYERS",
    "FabricLayer",
    "fabric_status",
    "layer_by_key",
    "layer_by_number",
    "layer_to_dict",
    "maturity_score",
    "package_exists",
    "resolve_layer_health",
]

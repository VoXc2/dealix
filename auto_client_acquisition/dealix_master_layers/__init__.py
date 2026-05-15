"""Dealix master layer registry — maps numbered constitution docs to repo packages."""

from auto_client_acquisition.dealix_master_layers.registry import (
    DealixLayer,
    IMPLEMENTATION_HINTS,
    MASTER_LAYERS,
    layer_by_folder,
    readme_path,
)

__all__ = [
    "DealixLayer",
    "IMPLEMENTATION_HINTS",
    "MASTER_LAYERS",
    "layer_by_folder",
    "readme_path",
]

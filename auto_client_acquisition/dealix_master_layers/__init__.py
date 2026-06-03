"""Dealix master layer registry — maps numbered constitution docs to repo packages."""

from auto_client_acquisition.dealix_master_layers.registry import (
    IMPLEMENTATION_HINTS,
    MASTER_LAYERS,
    DealixLayer,
    layer_by_folder,
    readme_path,
)

__all__ = [
    "IMPLEMENTATION_HINTS",
    "MASTER_LAYERS",
    "DealixLayer",
    "layer_by_folder",
    "readme_path",
]

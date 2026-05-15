"""Enterprise Layer Validation System.

Validates the 8 enterprise layers of Dealix — layer by layer — with a strict
dependency gate: layer N is only READY when every lower layer is READY.

The engine READS the manifest registers in
``dealix/registers/enterprise_layers/`` and NEVER edits them. Manifests are
governance state (see ``dealix/registers/__init__.py``); update the YAML, not
the Python.
"""

from __future__ import annotations

from dealix.layer_validation.spec import ENTERPRISE_LAYERS, LayerSpec

__all__ = ["ENTERPRISE_LAYERS", "LayerSpec"]

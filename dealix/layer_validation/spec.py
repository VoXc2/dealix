"""Ordered registry of the 8 enterprise layers.

This module is the source of truth for layer ORDER and DEPENDENCIES. The
per-layer manifest YAML files carry the detail (modules, tests, checklist).
A test asserts the two agree (``tests/test_enterprise_layers_manifests.py``).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayerSpec:
    """One enterprise layer in the validation model."""

    id: str
    order: int  # 1..8
    title: str
    manifest: str  # filename in dealix/registers/enterprise_layers/
    depends_on: tuple[str, ...]


# Order matches the Enterprise Layer Validation Model. ``depends_on`` for each
# layer is every strictly-lower layer — the strict layer-by-layer gate.
ENTERPRISE_LAYERS: tuple[LayerSpec, ...] = (
    LayerSpec(
        "foundation",
        1,
        "Foundation",
        "01_foundation.yaml",
        (),
    ),
    LayerSpec(
        "agent_runtime",
        2,
        "Agent Runtime",
        "02_agent_runtime.yaml",
        ("foundation",),
    ),
    LayerSpec(
        "workflow_engine",
        3,
        "Workflow Engine",
        "03_workflow_engine.yaml",
        ("foundation", "agent_runtime"),
    ),
    LayerSpec(
        "memory_knowledge",
        4,
        "Memory & Knowledge",
        "04_memory_knowledge.yaml",
        ("foundation", "agent_runtime", "workflow_engine"),
    ),
    LayerSpec(
        "governance",
        5,
        "Governance",
        "05_governance.yaml",
        ("foundation", "agent_runtime", "workflow_engine", "memory_knowledge"),
    ),
    LayerSpec(
        "observability",
        6,
        "Observability",
        "06_observability.yaml",
        (
            "foundation",
            "agent_runtime",
            "workflow_engine",
            "memory_knowledge",
            "governance",
        ),
    ),
    LayerSpec(
        "evaluation",
        7,
        "Evaluation",
        "07_evaluation.yaml",
        (
            "foundation",
            "agent_runtime",
            "workflow_engine",
            "memory_knowledge",
            "governance",
            "observability",
        ),
    ),
    LayerSpec(
        "executive_intelligence",
        8,
        "Executive Intelligence",
        "08_executive_intelligence.yaml",
        (
            "foundation",
            "agent_runtime",
            "workflow_engine",
            "memory_knowledge",
            "governance",
            "observability",
            "evaluation",
        ),
    ),
)

_BY_ID = {layer.id: layer for layer in ENTERPRISE_LAYERS}


def layer_by_id(layer_id: str) -> LayerSpec | None:
    """Return the LayerSpec for ``layer_id`` or None."""
    return _BY_ID.get(layer_id)


def lower_layer_ids(layer_id: str) -> tuple[str, ...]:
    """Return ids of all layers strictly below ``layer_id``."""
    layer = _BY_ID.get(layer_id)
    if layer is None:
        return ()
    return tuple(spec.id for spec in ENTERPRISE_LAYERS if spec.order < layer.order)

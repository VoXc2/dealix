"""Loads and schema-validates the enterprise layer manifest registers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from dealix.layer_validation.spec import ENTERPRISE_LAYERS, layer_by_id, lower_layer_ids

REGISTER_DIR = Path(__file__).resolve().parents[1] / "registers" / "enterprise_layers"

_REQUIRED_LAYER_KEYS = (
    "id",
    "order",
    "title",
    "definition",
    "owner",
    "depends_on",
    "responsibilities",
    "kpis",
    "modules",
    "required_tests",
    "checklist",
    "rollback_procedure",
    "observability_signals",
    "risk_model",
)


class ManifestError(RuntimeError):
    """Raised when a manifest file is missing or structurally broken."""


def manifest_path(layer_id: str) -> Path:
    """Return the manifest file path for ``layer_id``."""
    spec = layer_by_id(layer_id)
    if spec is None:
        raise ManifestError(f"unknown_layer:{layer_id}")
    return REGISTER_DIR / spec.manifest


def load_manifest(layer_id: str) -> dict[str, Any]:
    """Load and parse a single layer manifest. Raises ManifestError."""
    path = manifest_path(layer_id)
    if not path.is_file():
        raise ManifestError(f"manifest_missing:{path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise ManifestError(f"manifest_unparseable:{path}: {exc}") from exc
    if not isinstance(data, dict) or "layer" not in data:
        raise ManifestError(f"manifest_no_layer_key:{path}")
    return data


def load_all() -> dict[str, dict[str, Any]]:
    """Load every layer manifest keyed by layer id."""
    return {spec.id: load_manifest(spec.id) for spec in ENTERPRISE_LAYERS}


def validate_schema(layer_id: str, manifest: dict[str, Any]) -> list[str]:
    """Return a list of schema problems; empty list means the manifest is valid."""
    problems: list[str] = []
    layer = manifest.get("layer")
    if not isinstance(layer, dict):
        return [f"{layer_id}:layer_not_object"]

    for key in _REQUIRED_LAYER_KEYS:
        if key not in layer:
            problems.append(f"{layer_id}:missing_key:{key}")

    spec = layer_by_id(layer_id)
    if spec is None:
        problems.append(f"{layer_id}:unknown_layer")
        return problems

    if layer.get("id") != spec.id:
        problems.append(f"{layer_id}:id_mismatch:{layer.get('id')}")
    if layer.get("order") != spec.order:
        problems.append(f"{layer_id}:order_mismatch:{layer.get('order')}")

    declared_deps = layer.get("depends_on")
    if not isinstance(declared_deps, list):
        problems.append(f"{layer_id}:depends_on_not_list")
    else:
        expected = set(lower_layer_ids(layer_id))
        if set(declared_deps) != expected:
            problems.append(
                f"{layer_id}:depends_on_mismatch:"
                f"got={sorted(declared_deps)}:expected={sorted(expected)}"
            )

    for list_key in ("responsibilities", "modules", "required_tests", "checklist"):
        value = layer.get(list_key)
        if not isinstance(value, list) or not value:
            problems.append(f"{layer_id}:empty_or_invalid:{list_key}")

    modules = layer.get("modules")
    if isinstance(modules, list):
        for i, mod in enumerate(modules):
            if not isinstance(mod, dict) or not str(mod.get("path") or "").strip():
                problems.append(f"{layer_id}:module[{i}]_missing_path")

    checklist = layer.get("checklist")
    if isinstance(checklist, list):
        for i, item in enumerate(checklist):
            if not isinstance(item, dict):
                problems.append(f"{layer_id}:checklist[{i}]_not_object")
                continue
            if not str(item.get("id") or "").strip():
                problems.append(f"{layer_id}:checklist[{i}]_missing_id")
            if "done" not in item:
                problems.append(f"{layer_id}:checklist[{i}]_missing_done")

    return problems


def validate_all() -> list[str]:
    """Schema-validate every manifest. Empty list means all are valid."""
    problems: list[str] = []
    for spec in ENTERPRISE_LAYERS:
        try:
            manifest = load_manifest(spec.id)
        except ManifestError as exc:
            problems.append(str(exc))
            continue
        problems.extend(validate_schema(spec.id, manifest))
    return problems

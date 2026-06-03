"""
Dependency-free JSON-Schema validator (subset).

The environment has no ``jsonschema`` package, so this implements just enough
of draft-07 (type, required, enum, const, properties, items, additionalProperties,
minItems) to validate Dealix data files against the bundled schemas in CI and
tests. It is intentionally small and conservative.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
}


def _check(data: Any, schema: Dict, path: str, errors: List[str]) -> None:
    expected = schema.get("type")
    if expected:
        py = _TYPE_MAP.get(expected)
        if py and not isinstance(data, py):
            # bool is a subclass of int — guard against false matches.
            if not (expected in ("number", "integer") and isinstance(data, bool)):
                errors.append(f"{path}: expected {expected}, got {type(data).__name__}")
                return
        if expected in ("number", "integer") and isinstance(data, bool):
            errors.append(f"{path}: expected {expected}, got boolean")
            return

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: {data!r} not in enum {schema['enum']}")
    if "const" in schema and data != schema["const"]:
        errors.append(f"{path}: {data!r} != const {schema['const']!r}")

    if expected == "object" and isinstance(data, dict):
        for req in schema.get("required", []):
            if req not in data:
                errors.append(f"{path}: missing required '{req}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in data:
                if key not in props:
                    errors.append(f"{path}: additional property '{key}' not allowed")
        for key, value in data.items():
            if key in props:
                _check(value, props[key], f"{path}.{key}", errors)

    if expected == "array" and isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(data):
                _check(item, item_schema, f"{path}[{i}]", errors)


def validate(data: Any, schema: Dict) -> Tuple[bool, List[str]]:
    """Validate ``data`` against ``schema``. Returns (ok, errors)."""
    errors: List[str] = []
    _check(data, schema, "$", errors)
    return (len(errors) == 0, errors)


def load_schema(path: str | Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

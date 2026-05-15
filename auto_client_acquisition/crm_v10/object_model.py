"""CRM v10 object-model registry helpers."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.crm_v10.schemas import OBJECT_TYPES


def list_object_types() -> list[str]:
    """Return the 14 first-class CRM object type names in registry order."""
    return [m.__name__ for m in OBJECT_TYPES]


def get_object_schema(name: str) -> dict[str, Any]:
    """Return the JSON Schema for the named object type."""
    for model in OBJECT_TYPES:
        if model.__name__ == name:
            return model.model_json_schema()
    raise KeyError(f"unknown CRM v10 object type: {name}")


def all_object_schemas() -> dict[str, dict[str, Any]]:
    """Return a mapping of {object_type_name: json_schema}."""
    return {m.__name__: m.model_json_schema() for m in OBJECT_TYPES}


__all__ = ["all_object_schemas", "get_object_schema", "list_object_types"]

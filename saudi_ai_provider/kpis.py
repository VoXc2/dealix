"""KPI tree accessors."""

from __future__ import annotations

from typing import Any

from .catalog import load_kpi_tree
from .pricing import parse_service_id


def kpis_for_service(service_id: str) -> dict[str, Any]:
    engine, _tier = parse_service_id(service_id)
    tree = load_kpi_tree()
    if engine not in tree:
        raise ValueError(f"KPI tree missing engine: {engine}")
    return tree[engine]

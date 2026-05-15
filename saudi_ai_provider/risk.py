"""Risk register helpers."""

from __future__ import annotations

from typing import Any

from .catalog import load_risk_register
from .pricing import parse_service_id


def risk_for_service(service_id: str) -> list[dict[str, Any]]:
    engine, _tier = parse_service_id(service_id)
    register = load_risk_register()
    return register.get(engine, [])


def has_unmitigated_blocker(service_id: str) -> tuple[bool, list[str]]:
    blockers: list[str] = []
    for item in risk_for_service(service_id):
        if item.get("blocker") and not str(item.get("mitigation", "")).strip():
            blockers.append(item.get("risk", "unknown blocker"))
    return (len(blockers) > 0, blockers)

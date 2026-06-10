"""Capability dashboard — seven domains, levels 0–5."""

from __future__ import annotations

CAPABILITY_DOMAINS: tuple[str, ...] = (
    "revenue",
    "customer",
    "operations",
    "knowledge",
    "data",
    "governance",
    "reporting",
)

CAPABILITY_LEVEL_MAX = 5


def capability_level_valid(level: int) -> bool:
    return 0 <= level <= CAPABILITY_LEVEL_MAX

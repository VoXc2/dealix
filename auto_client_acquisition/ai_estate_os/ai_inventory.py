"""AI estate inventory row (no live connectors)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AIInventoryRow:
    asset_id: str
    kind: str
    owner: str
    risk_tier: str


def inventory_row_valid(row: AIInventoryRow) -> bool:
    return all((row.asset_id.strip(), row.kind.strip(), row.owner.strip(), row.risk_tier.strip()))


__all__ = ["AIInventoryRow", "inventory_row_valid"]

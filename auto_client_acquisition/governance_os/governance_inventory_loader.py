"""Load governance workflow inventory and validate against control registry."""

from __future__ import annotations

from pathlib import Path

import yaml

from auto_client_acquisition.governance_os.workflow_control_registry import (
    governed_workflow_domains,
)

_INVENTORY = (
    Path(__file__).resolve().parent / "governance_workflow_inventory.yaml"
)


def load_workflow_inventory() -> list[dict]:
    if not _INVENTORY.exists():
        return []
    data = yaml.safe_load(_INVENTORY.read_text(encoding="utf-8")) or {}
    return list(data.get("workflows") or [])


def inventory_matches_registry() -> bool:
    inv = {row.get("domain") for row in load_workflow_inventory()}
    reg = set(governed_workflow_domains())
    return inv == reg and len(reg) >= 10


__all__ = ["inventory_matches_registry", "load_workflow_inventory"]

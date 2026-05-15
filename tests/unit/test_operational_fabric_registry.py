"""Tests for Systems 26-35 platform contract registry."""

from __future__ import annotations

import json
from pathlib import Path

from auto_client_acquisition.operational_fabric_os import (
    PLATFORM_CONTRACTS,
    contract_count,
    contracts_by_system,
    validate_contract_bindings,
)


def test_contract_registry_complete_for_systems_26_to_35() -> None:
    grouped = contracts_by_system()
    assert sorted(grouped.keys()) == list(range(26, 36))
    assert contract_count() == 41
    assert len(PLATFORM_CONTRACTS) == 41


def test_contract_bindings_are_importable() -> None:
    ok, errors = validate_contract_bindings()
    assert ok, errors


def test_manifest_paths_match_registry_paths() -> None:
    manifest_path = Path("platform/contracts_manifest.json")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_paths = sorted(path for system in data["systems"] for path in system["paths"])
    registry_paths = sorted(contract.platform_path for contract in PLATFORM_CONTRACTS)
    assert manifest_paths == registry_paths

"""Delivery OS — service catalog facade."""

from __future__ import annotations

from auto_client_acquisition.delivery_os import (
    delivery_checklist_flat,
    service_catalog_entries,
    service_catalog_snapshot,
)


def test_service_catalog_non_empty() -> None:
    entries = service_catalog_entries()
    assert len(entries) >= 1
    snap = service_catalog_snapshot()
    assert snap.get("schema_version") == 1


def test_delivery_checklist_flat() -> None:
    flat = delivery_checklist_flat()
    assert flat and flat[0][0] == "discover"

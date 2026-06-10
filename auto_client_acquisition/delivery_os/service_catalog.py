"""Service catalog snapshot for Delivery OS."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.commercial_engagements.delivery_catalog import (
    DELIVERY_CATALOG,
    delivery_catalog_snapshot,
)


def service_catalog_entries() -> list[dict[str, Any]]:
    return list(DELIVERY_CATALOG)


def service_catalog_snapshot() -> dict[str, Any]:
    return delivery_catalog_snapshot()

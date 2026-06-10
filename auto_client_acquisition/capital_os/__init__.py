"""Capital OS — assets created per engagement (ledger-shaped, no I/O)."""

from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
from auto_client_acquisition.capital_os.capital_ledger import (
    CapitalAsset,
    CapitalLedgerEvent,
    add_asset,
    capital_ledger_event_valid,
    list_assets,
)

__all__ = [
    "CapitalAsset",
    "CapitalAssetType",
    "CapitalLedgerEvent",
    "add_asset",
    "capital_ledger_event_valid",
    "list_assets",
]

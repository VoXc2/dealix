"""Capital Asset Registry — tracks all reusable knowledge, automation, and
system assets generated for clients during engagements.

This builds the "value ledger" that justifies the retainer price by making
tangible the accumulation of client-specific intellectual property.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

AssetType = Literal["automation", "knowledge", "template", "workflow"]
AssetStatus = Literal["active", "archived"]

_DEFAULT_REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "capital_assets"
    / "registry.json"
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CapitalAsset(BaseModel):
    """A single capital asset record."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique asset identifier (UUID).",
    )
    account_id: str = Field(..., min_length=1, description="Client / account identifier.")
    asset_type: AssetType = Field(
        ..., description="Category: automation / knowledge / template / workflow."
    )
    title_ar: str = Field(..., min_length=1, description="Arabic asset title.")
    title_en: str = Field(..., min_length=1, description="English asset title.")
    value_estimate_sar: float = Field(
        default=0.0, ge=0.0, description="Estimated asset value in SAR."
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO-8601 UTC creation timestamp.",
    )
    status: AssetStatus = Field(default="active", description="active or archived.")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class CapitalAssetRegistry:
    """JSON-backed registry of capital assets.

    Thread-safety note: single-process safe only. For multi-worker deployments
    migrate to a database backend.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        self._path: Path = registry_path or _DEFAULT_REGISTRY_PATH

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self) -> list[dict]:
        if not self._path.exists():
            return []
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, records: list[dict]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, asset: CapitalAsset) -> CapitalAsset:
        """Add a new capital asset to the registry. Returns the asset with its
        assigned asset_id."""
        records = self._load()
        records.append(asset.model_dump())
        self._save(records)
        return asset

    def get_by_account(self, account_id: str) -> list[CapitalAsset]:
        """Return all assets for a given account_id (active and archived)."""
        records = self._load()
        return [
            CapitalAsset(**r)
            for r in records
            if r.get("account_id") == account_id
        ]

    def get_total_value_by_account(self, account_id: str) -> float:
        """Sum of value_estimate_sar for all active assets belonging to account."""
        assets = self.get_by_account(account_id)
        return round(
            sum(a.value_estimate_sar for a in assets if a.status == "active"),
            2,
        )

    def get_all(self) -> list[CapitalAsset]:
        """Return every asset in the registry."""
        return [CapitalAsset(**r) for r in self._load()]

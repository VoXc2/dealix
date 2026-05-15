"""Capital ledger — records reusable assets produced by governed delivery.

Two surfaces:

* :class:`CapitalLedgerEvent` + :func:`capital_ledger_event_valid` — the
  schema-stable validation row.
* :class:`CapitalAsset` + :func:`add_asset` / :func:`list_assets` — the
  JSONL-backed reusable-asset ledger keyed by ``DEALIX_CAPITAL_LEDGER_PATH``.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.capital_os.asset_types import CapitalAssetType


@dataclass(frozen=True, slots=True)
class CapitalLedgerEvent:
    capital_event_id: str
    project_id: str
    client_id: str
    asset_type: str
    title: str
    description: str
    evidence: str


def capital_ledger_event_valid(event: CapitalLedgerEvent) -> bool:
    return all(
        (
            event.capital_event_id.strip(),
            event.project_id.strip(),
            event.client_id.strip(),
            event.asset_type.strip(),
            event.title.strip(),
            event.description.strip(),
            event.evidence.strip(),
        ),
    )


_DEFAULT_PATH = "var/capital-ledger.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_CAPITAL_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _asset_type_value(t: str | CapitalAssetType) -> str:
    return t.value if isinstance(t, CapitalAssetType) else str(t)


@dataclass(frozen=True, slots=True)
class CapitalAsset:
    """A single reusable asset produced by a governed engagement."""

    asset_id: str
    customer_id: str
    engagement_id: str
    asset_type: str
    owner: str = ""
    reusable: bool = True
    asset_ref: str = ""
    notes: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def add_asset(
    *,
    customer_id: str,
    engagement_id: str,
    asset_type: str | CapitalAssetType,
    owner: str = "",
    reusable: bool = True,
    asset_ref: str = "",
    notes: str = "",
) -> CapitalAsset:
    """Append a reusable asset to the tenant-scoped capital ledger."""
    if not customer_id:
        raise ValueError("customer_id is required")
    if not engagement_id:
        raise ValueError("engagement_id is required")
    type_str = _asset_type_value(asset_type)
    if not type_str.strip():
        raise ValueError("asset_type is required")
    asset = CapitalAsset(
        asset_id=f"cap_{uuid.uuid4().hex[:12]}",
        customer_id=customer_id,
        engagement_id=engagement_id,
        asset_type=type_str,
        owner=owner or customer_id,
        reusable=bool(reusable),
        asset_ref=asset_ref,
        notes=notes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asset.to_dict(), ensure_ascii=False) + "\n")
    return asset


def list_assets(
    *,
    customer_id: str | None = None,
    engagement_id: str | None = None,
    limit: int = 200,
) -> list[CapitalAsset]:
    """List capital assets, optionally filtered by customer and engagement."""
    path = _path()
    if not path.exists():
        return []
    out: list[CapitalAsset] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    asset = CapitalAsset(**data)
                except Exception:  # noqa: BLE001
                    continue
                if customer_id is not None and asset.customer_id != customer_id:
                    continue
                if engagement_id is not None and asset.engagement_id != engagement_id:
                    continue
                out.append(asset)
    return out[-limit:] if limit else out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "CapitalAsset",
    "CapitalLedgerEvent",
    "add_asset",
    "capital_ledger_event_valid",
    "clear_for_test",
    "list_assets",
]

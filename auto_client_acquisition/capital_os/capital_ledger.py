"""Capital ledger — records reusable assets produced by governed delivery.

Persistence: append-only JSONL at ``DEALIX_CAPITAL_LEDGER_PATH`` (dev fallback).
Every asset carries ``customer_id`` and ``engagement_id`` for tenant-scoped reads.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/capital-ledger.jsonl"
_lock = threading.Lock()


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


@dataclass(slots=True)
class CapitalAsset:
    customer_id: str
    engagement_id: str
    asset_type: str
    title: str = ""
    description: str = ""
    owner: str = ""
    reusable: bool = True
    asset_ref: str = ""
    notes: str = ""
    asset_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    recorded_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_CAPITAL_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def add_asset(
    *,
    customer_id: str,
    engagement_id: str,
    asset_type: str,
    title: str = "",
    description: str = "",
    owner: str = "",
    reusable: bool = True,
    asset_ref: str = "",
    notes: str = "",
) -> CapitalAsset:
    if not customer_id:
        raise ValueError("customer_id is required")
    if not engagement_id:
        raise ValueError("engagement_id is required")
    if not asset_type:
        raise ValueError("asset_type is required")
    asset = CapitalAsset(
        customer_id=customer_id,
        engagement_id=engagement_id,
        asset_type=asset_type,
        title=title,
        description=description,
        owner=owner,
        reusable=reusable,
        asset_ref=asset_ref,
        notes=notes,
    )
    path = _path()
    _ensure_dir(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asset.to_dict(), ensure_ascii=False) + "\n")
    return asset


def _parse_asset(line: str) -> CapitalAsset | None:
    """Parse a single JSONL ledger line; returns None on malformed input."""
    try:
        data = json.loads(line)
        return CapitalAsset(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def list_assets(
    *,
    customer_id: str | None = None,
    engagement_id: str | None = None,
    limit: int = 1000,
) -> list[CapitalAsset]:
    """List capital assets, optionally filtered by customer and/or engagement."""
    path = _path()
    if not path.exists():
        return []
    out: list[CapitalAsset] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            asset = _parse_asset(line)
            if asset is None:
                continue
            if customer_id is not None and asset.customer_id != customer_id:
                continue
            if engagement_id is not None and asset.engagement_id != engagement_id:
                continue
            out.append(asset)
            if len(out) >= limit:
                break
    return out


def clear_for_test() -> None:
    """Dev/test helper — truncates the JSONL ledger file."""
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

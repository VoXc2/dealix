"""Capital ledger — records reusable assets produced by governed delivery.

A capital asset is a reusable artifact (scoring rule, draft template,
governance rule, ...) created during an engagement. Assets are persisted to
a JSONL file (``DEALIX_CAPITAL_LEDGER_PATH``), mirroring the friction-log
and value-ledger stores.

The structural ``CapitalLedgerEvent`` contract is retained for callers that
validate ledger-shaped records without I/O.
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
    """A reusable asset registered during an engagement."""

    engagement_id: str
    customer_id: str
    asset_type: str
    owner: str
    reusable: bool = True
    asset_ref: str = ""
    notes: str = ""
    asset_id: str = field(default_factory=lambda: f"cap_{uuid.uuid4().hex[:12]}")
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_CAPITAL_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def add_asset(
    *,
    engagement_id: str,
    customer_id: str,
    asset_type: str,
    owner: str,
    reusable: bool = True,
    asset_ref: str = "",
    notes: str = "",
) -> CapitalAsset:
    """Register a reusable capital asset for an engagement."""
    if not engagement_id or not customer_id:
        raise ValueError("engagement_id and customer_id are required")
    if not asset_type:
        raise ValueError("asset_type is required")
    asset = CapitalAsset(
        engagement_id=engagement_id,
        customer_id=customer_id,
        asset_type=str(asset_type),
        owner=owner or customer_id,
        reusable=bool(reusable),
        asset_ref=asset_ref,
        notes=notes,
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asset.to_dict(), ensure_ascii=False) + "\n")
    return asset


def list_assets(
    *,
    customer_id: str | None = None,
    engagement_id: str | None = None,
    limit: int = 200,
) -> list[CapitalAsset]:
    """List registered capital assets, optionally filtered by customer/engagement."""
    path = _path()
    if not path.exists():
        return []
    out: list[CapitalAsset] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                asset = CapitalAsset(**json.loads(line))
            except Exception:  # noqa: S112 — skip a corrupt ledger line
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
    """Wipe the capital ledger file — test isolation helper."""
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

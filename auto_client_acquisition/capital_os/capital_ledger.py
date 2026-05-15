"""Capital ledger — records reusable assets produced by governed delivery.

Storage: append-only JSONL at ``$DEALIX_CAPITAL_LEDGER_PATH`` (default
``var/capital-ledger.jsonl``), matching the value_ledger / friction_log
pattern so the swap to a DB-backed store is mechanical.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


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


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class CapitalAsset:
    """A reusable artifact registered against an engagement."""

    asset_id: str = field(default_factory=lambda: f"cap_{uuid4().hex[:12]}")
    engagement_id: str = ""
    customer_id: str = ""
    asset_type: str = ""
    owner: str = ""
    reusable: bool = True
    asset_ref: str = ""
    notes: str = ""
    registered_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def add_asset(
    *,
    engagement_id: str,
    customer_id: str,
    asset_type: str,
    owner: str = "",
    reusable: bool = True,
    asset_ref: str = "",
    notes: str = "",
) -> CapitalAsset:
    """Register a reusable capital asset and append it to the ledger."""
    if not customer_id:
        raise ValueError("customer_id is required")
    if not asset_type:
        raise ValueError("asset_type is required")
    asset = CapitalAsset(
        engagement_id=engagement_id,
        customer_id=customer_id,
        asset_type=asset_type,
        owner=owner or customer_id,
        reusable=bool(reusable),
        asset_ref=asset_ref,
        notes=notes,
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asset.to_dict(), ensure_ascii=False) + "\n")
    return asset


def list_assets(
    *,
    customer_id: str | None = None,
    engagement_id: str | None = None,
    limit: int = 1000,
) -> list[CapitalAsset]:
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
                    asset = CapitalAsset(**json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
                if customer_id and asset.customer_id != customer_id:
                    continue
                if engagement_id and asset.engagement_id != engagement_id:
                    continue
                out.append(asset)
                if len(out) >= limit:
                    break
    return out


def clear_for_test(customer_id: str | None = None) -> None:
    """Test-only: truncate the ledger file (or one customer's rows)."""
    path = _path()
    if not path.exists():
        return
    with _lock:
        if customer_id is None:
            path.write_text("", encoding="utf-8")
            return
        keep: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                if json.loads(line).get("customer_id") != customer_id:
                    keep.append(line)
            except Exception:  # noqa: BLE001
                keep.append(line)
        path.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")


__all__ = [
    "CapitalAsset",
    "CapitalLedgerEvent",
    "add_asset",
    "capital_ledger_event_valid",
    "clear_for_test",
    "list_assets",
]

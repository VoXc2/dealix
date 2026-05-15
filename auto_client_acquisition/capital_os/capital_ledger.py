"""Capital ledger — records reusable assets produced by governed delivery.

Backed by a JSONL file (env ``DEALIX_CAPITAL_LEDGER_PATH``) so it mirrors the
friction_log / value_ledger stores and stays append-only / auditable.

Every governed engagement registers >= 1 reusable Capital Asset. ``list_assets``
is consumed by the case-study exporter and the evidence gap detector.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
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


@dataclass(frozen=True, slots=True)
class CapitalAsset:
    """A persisted reusable asset row in the capital ledger."""

    customer_id: str
    engagement_id: str
    asset_type: str
    title: str
    description: str = ""
    evidence_ref: str = ""
    asset_id: str = field(default_factory=lambda: f"CAP-{uuid.uuid4().hex[:12]}")
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_CAPITAL_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def record_asset(
    *,
    customer_id: str,
    engagement_id: str,
    asset_type: str,
    title: str,
    description: str = "",
    evidence_ref: str = "",
) -> CapitalAsset:
    """Append one reusable Capital Asset to the ledger."""
    if not customer_id:
        raise ValueError("customer_id is required")
    if not engagement_id:
        raise ValueError("engagement_id is required")
    if not asset_type.strip():
        raise ValueError("asset_type is required")
    if not title.strip():
        raise ValueError("title is required")
    asset = CapitalAsset(
        customer_id=customer_id,
        engagement_id=engagement_id,
        asset_type=asset_type,
        title=title,
        description=description,
        evidence_ref=evidence_ref,
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
    """Return persisted Capital Assets, optionally scoped by tenant / engagement."""
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
                if customer_id is not None and asset.customer_id != customer_id:
                    continue
                if engagement_id is not None and asset.engagement_id != engagement_id:
                    continue
                out.append(asset)
                if len(out) >= limit:
                    break
    return out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "CapitalAsset",
    "CapitalLedgerEvent",
    "capital_ledger_event_valid",
    "clear_for_test",
    "list_assets",
    "record_asset",
]

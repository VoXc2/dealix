"""Capital ledger — reusable assets created per engagement.

``CapitalLedgerEvent`` is the lightweight proof-architecture event shape;
``CapitalAsset`` + ``add_asset`` / ``list_assets`` are the JSONL-backed
engagement ledger consumed by governed delivery.

Storage: $DEALIX_CAPITAL_LEDGER_PATH (default var/capital-ledger.jsonl).
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
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


# ── JSONL-backed engagement asset ledger ─────────────────────────────────

ALLOWED_ASSET_TYPES = frozenset({
    "scoring_rule",
    "draft_template",
    "governance_rule",
    "proof_example",
    "sector_insight",
    "productization_signal",
    "qa_rubric",
    "arabic_style_pattern",
})

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
    asset_id: str = field(default_factory=lambda: f"cap_{uuid4().hex[:12]}")
    engagement_id: str = ""
    customer_id: str = ""
    asset_type: str = ""
    owner: str = ""
    reusable: bool = True
    asset_ref: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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
    if asset_type not in ALLOWED_ASSET_TYPES:
        raise ValueError(
            f"asset_type {asset_type!r} not in {sorted(ALLOWED_ASSET_TYPES)}"
        )
    if not engagement_id:
        raise ValueError("engagement_id is required")
    if not customer_id:
        raise ValueError("customer_id is required")
    asset = CapitalAsset(
        engagement_id=engagement_id,
        customer_id=customer_id,
        asset_type=asset_type,
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


def list_assets(
    *,
    customer_id: str | None = None,
    engagement_id: str | None = None,
    asset_type: str | None = None,
    limit: int = 1000,
) -> list[CapitalAsset]:
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
                data = json.loads(line)
                a = CapitalAsset(**data)
            except Exception:  # noqa: S112 — best-effort: skip a corrupt ledger line
                continue
            if customer_id and a.customer_id != customer_id:
                continue
            if engagement_id and a.engagement_id != engagement_id:
                continue
            if asset_type and a.asset_type != asset_type:
                continue
            out.append(a)
            if len(out) >= limit:
                break
    return out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "ALLOWED_ASSET_TYPES",
    "CapitalAsset",
    "CapitalLedgerEvent",
    "add_asset",
    "capital_ledger_event_valid",
    "clear_for_test",
    "list_assets",
]

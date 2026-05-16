"""Revenue attribution paths — records value ledger events per commercial path."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.value_os.value_ledger import ValueEvent, add_event

_ATTRIBUTION_PATH = Path(__file__).resolve().parent / "attribution_paths.yaml"


def load_attribution_paths() -> dict[str, Any]:
    if not _ATTRIBUTION_PATH.exists():
        return {"paths": []}
    return yaml.safe_load(_ATTRIBUTION_PATH.read_text(encoding="utf-8")) or {}


def record_path_attribution(
    *,
    path_id: str,
    customer_id: str,
    amount: float,
    source_ref: str,
    tier: str = "estimated",
    notes: str = "",
) -> ValueEvent:
    """Record a value event tagged with a commercial attribution path."""
    catalog = load_attribution_paths()
    paths = {p["id"]: p for p in catalog.get("paths", []) if isinstance(p, dict) and p.get("id")}
    path = paths.get(path_id)
    kind = str(path.get("ledger_kind", "attributed_value")) if path else "attributed_value"
    note = f"path_id={path_id}; {notes}".strip()
    return add_event(
        customer_id=customer_id,
        kind=kind,
        amount=amount,
        tier=tier,
        source_ref=source_ref,
        notes=note,
    )

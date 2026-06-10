"""Transformation program read APIs — KPI baselines snapshot (read-only)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter

_REPO = Path(__file__).resolve().parents[2]
_BASELINES = _REPO / "dealix" / "transformation" / "kpi_baselines.yaml"
_REGISTRY = _REPO / "dealix" / "transformation" / "kpi_founder_commercial_registry.yaml"

router = APIRouter(prefix="/transformation", tags=["transformation"])


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@router.get("/kpi-snapshot")
def kpi_snapshot() -> dict[str, Any]:
    """Read-only KPI baselines + commercial registry status for dashboards."""
    baselines = _load_yaml(_BASELINES)
    registry = _load_yaml(_REGISTRY)
    commercial = registry.get("commercial_entries") or {}
    pending: list[str] = []
    ready: list[str] = []
    for key, row in commercial.items():
        val = row.get("value_numeric") if isinstance(row, dict) else None
        ref = (row.get("source_ref") or "").strip() if isinstance(row, dict) else ""
        if val is None or not ref:
            pending.append(key)
        else:
            ready.append(key)
    snapshots = baselines.get("snapshots") or {}
    return {
        "program": baselines.get("program", "global_ai_transformation"),
        "updated_period_iso": baselines.get("updated_period_iso"),
        "weekly_ops": baselines.get("weekly_ops"),
        "snapshots": snapshots,
        "commercial_registry": {
            "pending_keys": pending,
            "ready_keys": ready,
            "pending_count": len(pending),
            "ready_count": len(ready),
        },
        "notes_ar": (
            "قراءة فقط من kpi_baselines.yaml. "
            "للحقيقة التجارية: kpi_founder_commercial_import.yaml ثم apply_kpi_founder_commercial.py"
        ),
    }

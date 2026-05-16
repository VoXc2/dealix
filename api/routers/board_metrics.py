"""Board-level metrics read API (initiative 192)."""

from __future__ import annotations

from pathlib import Path

import yaml
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/board", tags=["board"])


@router.get("/metrics")
def get_board_metrics() -> dict:
    root = Path(__file__).resolve().parents[2]
    kpi = yaml.safe_load((root / "dealix/transformation/kpi_registry.yaml").read_text(encoding="utf-8"))
    reg = yaml.safe_load(
        (root / "dealix/transformation/strategic_initiatives_registry.yaml").read_text(encoding="utf-8")
    )
    initiatives = reg.get("initiatives") or []
    phase2_active = sum(1 for r in initiatives if r.get("phase") == 2 and r.get("status") == "active")
    return {
        "north_star_keys": [r.get("key") for r in (kpi.get("kpis") or {}).get("north_star", [])],
        "initiative_count": len(initiatives),
        "phase2_active_count": phase2_active,
        "program": reg.get("program", ""),
    }

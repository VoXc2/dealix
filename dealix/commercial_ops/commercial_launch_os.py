"""Commercial Launch OS — scoring snapshot with placeholder-safe evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    load_evidence_rows,
    real_evidence_rows,
)

_REPO = Path(__file__).resolve().parents[2]


def build_launch_snapshot(*, skip_live: bool = False) -> dict[str, Any]:
    """Offline-friendly launch readiness snapshot for founder gates."""
    rows = load_evidence_rows()
    real = real_evidence_rows(rows)
    counts = count_evidence_events(real, exclude_placeholders=True)
    checks: list[dict[str, Any]] = [
        {"id": "gtm_home", "ok": (_REPO / "frontend/src/components/gtm/CommercialLaunchHome.tsx").is_file()},
        {"id": "public_gtm_shell", "ok": (_REPO / "frontend/src/components/gtm/PublicGtmShell.tsx").is_file()},
        {"id": "root_redirect_ar", "ok": 'redirect("/ar")' in (_REPO / "frontend/src/app/page.tsx").read_text(encoding="utf-8")},
        {"id": "launch_comms_doc", "ok": (_REPO / "docs/commercial/operations/FOUNDER_LAUNCH_DAY_COMMS_AR.md").is_file()},
        {"id": "railway_doc", "ok": (_REPO / "docs/ops/RAILWAY_COMMERCIAL_SOFT_LAUNCH_AR.md").is_file()},
    ]
    points = sum(1 for c in checks if c["ok"])
    verdict = "PASS" if points >= len(checks) - 1 else "WARN" if points >= len(checks) - 2 else "FAIL"
    return {
        "schema_version": "1.0",
        "verdict": verdict,
        "launch_tier": "soft",
        "skip_live": skip_live,
        "score": {"points": points, "max": len(checks)},
        "checks": checks,
        "evidence_real_rows": len(real),
        "evidence_counts": counts,
    }


def evaluate_check(row: dict[str, Any], *, rag_tiles: dict[str, Any] | None = None, skip_live: bool = False) -> dict[str, Any]:
    """Evaluate a single checklist row (path existence)."""
    _ = rag_tiles, skip_live
    path = row.get("path", "")
    ok = (_REPO / path).is_file() if path else False
    return {"id": row.get("id", ""), "ok": ok, "rag": "green" if ok else "red", "path": path}

"""Founder weekly metrics — KPI import + Truth Matrix + evidence scorecard."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
from dealix.commercial_ops.paths import REPO_ROOT
from dealix.commercial_ops.weekly_scorecard_commercial import build_weekly_scorecard

_TRUTH_CANDIDATES = (
    REPO_ROOT / "dealix" / "transformation" / "founder_integration_truth.yaml",
)
_WEEKLY_DIR = REPO_ROOT / "data" / "founder_weekly"


def _truth_matrix_path() -> Path | None:
    for candidate in _TRUTH_CANDIDATES:
        if candidate.is_file():
            return candidate
    return None


def _iso_week(d: datetime | None = None) -> str:
    dt = d or datetime.now(UTC)
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"


def load_truth_matrix_summary() -> dict[str, Any]:
    truth_path = _truth_matrix_path()
    if truth_path is None:
        return {"exists": False, "red": [], "yellow": [], "green": []}
    data = yaml.safe_load(truth_path.read_text(encoding="utf-8")) or {}
    buckets: dict[str, list[str]] = {"red": [], "yellow": [], "green": []}
    for section in ("ladder", "integrations"):
        for row in data.get(section) or []:
            if not isinstance(row, dict):
                continue
            status = (row.get("status") or "").strip().lower()
            label = (row.get("id") or row.get("label_ar") or "?").strip()
            if status in buckets:
                buckets[status].append(label)
    return {
        "exists": True,
        "updated_note_ar": data.get("updated_note_ar"),
        **buckets,
    }


def build_founder_weekly_metrics(*, week_end: datetime | None = None) -> dict[str, Any]:
    """Single bundle for Sunday retro — no invented CRM numbers."""
    kpi = load_kpi_commercial_status()
    truth = load_truth_matrix_summary()
    scorecard = build_weekly_scorecard(week_end=week_end)
    iso_week = _iso_week(week_end)

    blockers: list[str] = []
    if kpi.get("pending"):
        blockers.append(
            f"{len(kpi['pending'])} KPI معلّقة — املأ kpi_founder_commercial_import.yaml من CRM"
        )
    if truth.get("red"):
        blockers.append(f"Truth Matrix red: {', '.join(truth['red'][:5])}")

    return {
        "iso_week": iso_week,
        "generated_at": datetime.now(UTC).isoformat(),
        "kpi_commercial": kpi,
        "truth_matrix": truth,
        "evidence_scorecard": scorecard,
        "blockers_ar": blockers,
        "verdict": "BLOCKED" if blockers else "READY",
        "sources": {
            "kpi_import": "dealix/transformation/kpi_founder_commercial_import.yaml",
            "truth_matrix": "dealix/transformation/founder_integration_truth.yaml",
            "evidence": "docs/commercial/operations/evidence_events_tracker.csv",
        },
    }


def write_weekly_metrics_artifact(blob: dict[str, Any] | None = None) -> Path:
    data = blob or build_founder_weekly_metrics()
    _WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    path = _WEEKLY_DIR / f"metrics_{data['iso_week']}.yaml"
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path

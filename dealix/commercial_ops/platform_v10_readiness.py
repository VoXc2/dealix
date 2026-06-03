"""Platform v10 readiness — blocked until Phase 0–1 gate PASS."""

from __future__ import annotations

from typing import Any

import yaml

from dealix.commercial_ops.paths import PLATFORM_V10_BACKLOG_YAML, REPO_ROOT
from dealix.commercial_ops.phase_01_close_path import build_phase_01_close_path

PLATFORM_V10_DOC = REPO_ROOT / "docs/commercial/FOUNDER_STRONGEST_PLAN_AR.md"


def load_platform_v10_backlog() -> dict[str, Any]:
    if not PLATFORM_V10_BACKLOG_YAML.is_file():
        return {"items": []}
    return yaml.safe_load(PLATFORM_V10_BACKLOG_YAML.read_text(encoding="utf-8")) or {}


def analyze_platform_v10_readiness() -> dict[str, Any]:
    phase = build_phase_01_close_path()
    backlog = load_platform_v10_backlog()
    items = backlog.get("items") or []

    if not phase.get("gate_open"):
        return {
            "verdict": "BLOCKED",
            "blocked_by": "phase_0_1_gate",
            "phase_01": phase,
            "message_ar": "Platform v10 ممنوع قبل PASS بوابة Phase 0–1",
            "backlog_count": len(items),
        }

    done = sum(1 for i in items if i.get("status") == "done")
    total = len(items)
    verdict = "PASS" if total and done == total else "IN_PROGRESS"
    return {
        "verdict": verdict,
        "blocked_by": None,
        "backlog_total": total,
        "backlog_done": done,
        "backlog_path": str(PLATFORM_V10_BACKLOG_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
    }

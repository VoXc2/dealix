"""Founder Excellence OS — RAG snapshot across strategic pillars."""

from __future__ import annotations

from typing import Any

import yaml

from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status
from dealix.commercial_ops.founder_north_star import build_north_star_status
from dealix.commercial_ops.founder_production_gates import build_founder_production_gates
from dealix.commercial_ops.paths import (
    FOUNDER_EXCELLENCE_OS_YAML,
    FOUNDER_WELLBEING_YAML,
    REPO_ROOT,
)

EXCELLENCE_DOC = REPO_ROOT / "docs/ops/FOUNDER_EXCELLENCE_OS_AR.md"


def _rag_from_verdict(verdict: str) -> str:
    v = (verdict or "").upper()
    if v in ("PASS", "OK", "CLOSED", "GREEN"):
        return "green"
    if v in ("WARN", "IN_PROGRESS", "PARTIAL", "DEGRADED", "AMBER"):
        return "amber"
    return "red"


def build_excellence_os_status(*, skip_live: bool = False) -> dict[str, Any]:
    prod = build_founder_production_gates(skip_live=skip_live)
    north = build_north_star_status()
    comprehensive = build_comprehensive_status()

    pillars = {
        "production": {"verdict": prod.get("verdict"), "rag": _rag_from_verdict(prod.get("verdict", ""))},
        "north_star": {"verdict": north.get("verdict"), "rag": _rag_from_verdict(north.get("verdict", ""))},
        "phase_gate": {
            "verdict": (comprehensive.get("phase_0_1_gate") or {}).get("verdict"),
            "rag": _rag_from_verdict((comprehensive.get("phase_0_1_gate") or {}).get("verdict", "")),
        },
    }

    reds = [k for k, v in pillars.items() if v.get("rag") == "red"]
    ambers = [k for k, v in pillars.items() if v.get("rag") == "amber"]
    overall = "green" if not reds and not ambers else ("amber" if not reds else "red")

    wellbeing_note = None
    if FOUNDER_WELLBEING_YAML.is_file():
        wb = yaml.safe_load(FOUNDER_WELLBEING_YAML.read_text(encoding="utf-8")) or {}
        wellbeing_note = wb.get("weekly_decision_cap")

    return {
        "verdict": "PASS" if overall == "green" else ("WARN" if overall == "amber" else "FAIL"),
        "overall_rag": overall,
        "pillars": pillars,
        "wellbeing_decision_cap": wellbeing_note or "≤3 strategic decisions/week",
        "doc": str(EXCELLENCE_DOC.relative_to(REPO_ROOT)).replace("\\", "/")
        if EXCELLENCE_DOC.is_file()
        else None,
    }

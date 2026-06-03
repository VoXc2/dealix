"""Founder north star metrics — queue P0 + evidence truth."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    load_evidence_rows,
    real_evidence_rows,
)
from dealix.commercial_ops.founder_agent_tasks import analyze_agent_queue_status
from dealix.commercial_ops.paths import FOUNDER_NORTH_STAR_YAML, REPO_ROOT

NORTH_STAR_DOC = REPO_ROOT / "docs/commercial/FOUNDER_NORTH_STAR_METRICS_AR.md"


def load_north_star_config() -> dict[str, Any]:
    if not FOUNDER_NORTH_STAR_YAML.is_file():
        return {}
    return yaml.safe_load(FOUNDER_NORTH_STAR_YAML.read_text(encoding="utf-8")) or {}


def build_north_star_status() -> dict[str, Any]:
    cfg = load_north_star_config()
    queue = analyze_agent_queue_status()
    real = real_evidence_rows(load_evidence_rows())
    counts = count_evidence_events(real)

    must = cfg.get("must_outcomes_90d") or {}
    targets = {
        "proof_packs_min": must.get("proof_packs_delivered_min", 5),
        "retainers_min": must.get("active_retainers_min", 3),
        "mrr_sar_min": must.get("mrr_sar_min", 8000),
    }

    proof_count = counts.get("proof_pack_delivered", 0)
    paid_count = counts.get("payment_received", 0)

    gaps: list[str] = []
    if proof_count < targets["proof_packs_min"]:
        gaps.append(f"proof packs: {proof_count}/{targets['proof_packs_min']}")
    if paid_count < 1:
        gaps.append("أول payment_received حقيقي مطلوب")
    if queue.get("p0_count", 0) == 0 and queue.get("task_count", 0) > 0:
        gaps.append("لا مهام P0 في طابور اليوم — راجع founder_agent_task_queue.yaml")

    verdict = "PASS" if not gaps and proof_count >= 1 and paid_count >= 1 else "IN_PROGRESS"
    if not cfg:
        verdict = "WARN"

    return {
        "verdict": verdict,
        "north_star_ar": cfg.get("north_star_ar"),
        "targets_90d": targets,
        "evidence_counts": counts,
        "real_evidence_rows": len(real),
        "queue_p0": queue.get("p0_count", 0),
        "queue_tasks": queue.get("task_count", 0),
        "gaps": gaps,
        "doc": str(NORTH_STAR_DOC.relative_to(REPO_ROOT)).replace("\\", "/")
        if NORTH_STAR_DOC.is_file()
        else None,
    }

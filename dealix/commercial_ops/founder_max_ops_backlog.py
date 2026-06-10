"""Load and summarize the 50+ founder max-ops backlog (YAML)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import FOUNDER_MAX_OPS_BACKLOG_YAML, REPO_ROOT

BACKLOG_YAML = FOUNDER_MAX_OPS_BACKLOG_YAML
BACKLOG_DOC = "docs/ops/FOUNDER_MAX_OPS_BACKLOG_AR.md"

VALID_STATUSES = frozenset({"open", "in_progress", "done", "blocked", "cancelled"})


def load_backlog() -> dict[str, Any]:
    if not BACKLOG_YAML.is_file():
        return {"version": 0, "tasks": [], "sections": {}}
    data = yaml.safe_load(BACKLOG_YAML.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {"tasks": []}


def _automation_probe(ref: str) -> str:
    """Suggest if repo artifact exists for task ref (read-only, no YAML write)."""
    rel = ref.split()[0] if ref else ""
    if not rel or rel.startswith("POST") or rel.startswith("GET"):
        return "manual"
    p = REPO_ROOT / rel.replace("/", "\\") if "\\" in rel else REPO_ROOT / rel
    if p.is_file():
        return "artifact_ok"
    if p.is_dir():
        return "artifact_ok"
    if rel.endswith(".py") and (REPO_ROOT / rel).is_file():
        return "artifact_ok"
    return "open"


def summarize_backlog() -> dict[str, Any]:
    data = load_backlog()
    tasks = data.get("tasks") if isinstance(data.get("tasks"), list) else []
    by_status: dict[str, int] = {}
    by_section: dict[str, int] = {}
    for t in tasks:
        if not isinstance(t, dict):
            continue
        st = str(t.get("status") or "open").lower()
        by_status[st] = by_status.get(st, 0) + 1
        sec = str(t.get("section") or "?")
        by_section[sec] = by_section.get(sec, 0) + 1
    total = len(tasks)
    done = by_status.get("done", 0)
    in_prog = by_status.get("in_progress", 0)
    open_ct = by_status.get("open", 0)
    pct = round(100.0 * done / total, 1) if total else 0.0
    if done == total and total > 0:
        verdict = "COMPLETE"
    elif in_prog > 0 or done > 0:
        verdict = "IN_PROGRESS"
    else:
        verdict = "OPEN"
    enriched: list[dict[str, Any]] = []
    for t in tasks:
        if not isinstance(t, dict):
            continue
        ref = str(t.get("ref") or "")
        enriched.append({**t, "automation_probe": _automation_probe(ref)})

    return {
        "verdict": verdict,
        "total": total,
        "done": done,
        "in_progress": in_prog,
        "open": open_ct,
        "percent_done": pct,
        "by_status": by_status,
        "by_section": by_section,
        "yaml_path": str(BACKLOG_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
        "doc": BACKLOG_DOC,
        "tasks": enriched,
    }

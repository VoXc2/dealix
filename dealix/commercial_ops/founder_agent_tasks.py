"""Founder agent task queue — seed daily tasks + export as work packets."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import (
    FOUNDER_AGENT_QUEUE_TODAY_JSON,
    FOUNDER_AGENT_QUEUE_YAML,
    REPO_ROOT,
)

AGENT_FLEET_DOC = REPO_ROOT / "docs/agentic_operations/AGENT_FLEET_OPERATING_SYSTEM_AR.md"


def load_task_queue_config() -> dict[str, Any]:
    if not FOUNDER_AGENT_QUEUE_YAML.is_file():
        return {"version": "1", "tasks": []}
    return yaml.safe_load(FOUNDER_AGENT_QUEUE_YAML.read_text(encoding="utf-8")) or {}


def _today_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def seed_today_queue(*, dry_run: bool = False) -> dict[str, Any]:
    """Build today's queue from YAML templates; write data/founder_briefs/queue_today.json."""
    cfg = load_task_queue_config()
    day = _today_iso()
    tasks: list[dict[str, Any]] = []
    for tpl in cfg.get("tasks") or []:
        cadence = (tpl.get("cadence") or "daily").lower()
        if cadence not in ("daily", "weekly", "always"):
            continue
        if cadence == "weekly" and datetime.now(UTC).weekday() != 6:
            continue
        tasks.append(
            {
                "id": tpl.get("id"),
                "agent": tpl.get("agent"),
                "priority": tpl.get("priority", "P1"),
                "title_ar": tpl.get("title_ar"),
                "outputs": tpl.get("outputs") or [],
                "verify_commands": tpl.get("verify_commands") or [],
                "date": day,
            }
        )

    payload = {
        "schema_version": "1.0",
        "date": day,
        "seeded_at": datetime.now(UTC).isoformat(),
        "tasks": tasks,
        "p0_count": sum(1 for t in tasks if t.get("priority") == "P0"),
    }
    if not dry_run:
        FOUNDER_AGENT_QUEUE_TODAY_JSON.parent.mkdir(parents=True, exist_ok=True)
        FOUNDER_AGENT_QUEUE_TODAY_JSON.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    payload["written_path"] = str(
        FOUNDER_AGENT_QUEUE_TODAY_JSON.relative_to(REPO_ROOT)
    ).replace("\\", "/")
    return payload


def templates_as_packets() -> dict[str, dict[str, Any]]:
    """Map task queue templates to daily_packets.yaml shape for print_agent_work_packets."""
    cfg = load_task_queue_config()
    packets: dict[str, dict[str, Any]] = {}
    for tpl in cfg.get("tasks") or []:
        tid = tpl.get("id") or "unknown"
        packets[tid] = {
            "agent": tpl.get("agent"),
            "cadence": tpl.get("cadence") or "daily",
            "inputs": tpl.get("inputs") or [],
            "outputs": tpl.get("outputs") or [],
            "verify_commands": tpl.get("verify_commands") or [],
        }
    return packets


def analyze_agent_queue_status() -> dict[str, Any]:
    seed = seed_today_queue(dry_run=True)
    cfg_exists = FOUNDER_AGENT_QUEUE_YAML.is_file()
    fleet_doc = AGENT_FLEET_DOC.is_file()
    today_file = FOUNDER_AGENT_QUEUE_TODAY_JSON.is_file()
    verdict = "PASS" if cfg_exists and seed.get("tasks") else "WARN"
    if not cfg_exists:
        verdict = "FAIL"
    return {
        "verdict": verdict,
        "config_path": str(FOUNDER_AGENT_QUEUE_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
        "config_exists": cfg_exists,
        "fleet_doc_exists": fleet_doc,
        "today_queue_exists": today_file,
        "p0_count": seed.get("p0_count", 0),
        "task_count": len(seed.get("tasks") or []),
        "tasks_preview": (seed.get("tasks") or [])[:5],
    }

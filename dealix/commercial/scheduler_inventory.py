"""Scheduler Inventory — canonical vs duplicate timer audit."""

from __future__ import annotations

import subprocess
from typing import Any

from pydantic import BaseModel, ConfigDict

class TimerEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    name: str
    schedule: str = "unknown"
    activates: str = ""
    status: str = "unknown"

def inventory_timers() -> list[TimerEntry]:
    try:
        r = subprocess.run(["systemctl", "list-timers", "--all", "--no-pager"], capture_output=True, text=True, timeout=10)
        lines = r.stdout.splitlines()
        entries = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 6 and "dealix" in line:
                entries.append(TimerEntry(name=parts[-2] if len(parts)>5 else line.strip()[:60], schedule=parts[0], activates=parts[-1]))
        return entries
    except Exception:
        return []

def classify_timers(timers: list[TimerEntry]) -> dict[str, Any]:
    # Simple classification: canonical if known good, duplicate if similar name
    canonical = [t for t in timers if "autonomous-company" in t.name or "president-recovery" in t.name]
    duplicate = []
    seen = {}
    for t in timers:
        key = t.activates or t.name
        if key in seen:
            duplicate.append(t.name)
        else:
            seen[key] = t
    return {"total": len(timers), "canonical": len(canonical), "potential_duplicates": duplicate, "timers": [t.model_dump() for t in timers]}

__all__ = ["TimerEntry", "inventory_timers", "classify_timers"]

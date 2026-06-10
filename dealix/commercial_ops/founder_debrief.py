"""Founder meeting debrief files — from YAML template."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import (
    FOUNDER_DEBRIEFS_DIR,
    GTM_DEBRIEF_TEMPLATE,
    REPO_ROOT,
)


def _slug(company: str) -> str:
    s = re.sub(r"[^\w\u0600-\u06FF]+", "-", company.strip(), flags=re.UNICODE)
    return s.strip("-")[:48] or "company"


def init_debrief(
    *,
    company: str,
    contact: str = "",
    motion: str = "A",
    offer_id: str = "",
    meeting_type: str = "discovery",
    date_str: str | None = None,
    out_dir: Path | None = None,
) -> Path:
    """Write data/founder_debriefs/debrief_{date}_{slug}.yaml from template."""
    if not GTM_DEBRIEF_TEMPLATE.is_file():
        raise FileNotFoundError(str(GTM_DEBRIEF_TEMPLATE))
    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    template = yaml.safe_load(GTM_DEBRIEF_TEMPLATE.read_text(encoding="utf-8"))
    if not isinstance(template, dict):
        raise ValueError("invalid debrief template")

    payload: dict[str, Any] = dict(template)
    meeting = dict(payload.get("meeting") or {})
    meeting.update(
        {
            "date": day,
            "company": company,
            "contact": contact,
            "motion": motion,
            "offer_id": offer_id,
            "type": meeting_type,
        }
    )
    payload["meeting"] = meeting
    debrief = dict(payload.get("debrief") or {})
    debrief["next_action_date"] = day
    payload["debrief"] = debrief

    d = out_dir or FOUNDER_DEBRIEFS_DIR
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"debrief_{day}_{_slug(company)}.yaml"
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path


def list_debriefs(limit: int = 20) -> list[dict[str, Any]]:
    d = FOUNDER_DEBRIEFS_DIR
    if not d.is_dir():
        return []
    files = sorted(d.glob("debrief_*.yaml"), key=lambda p: p.stat().st_mtime, reverse=True)
    out: list[dict[str, Any]] = []
    for p in files[:limit]:
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        meeting = (data or {}).get("meeting") or {}
        debrief = (data or {}).get("debrief") or {}
        out.append(
            {
                "path": str(p.relative_to(REPO_ROOT)).replace("\\", "/"),
                "company": meeting.get("company"),
                "date": meeting.get("date"),
                "one_decision": debrief.get("one_decision"),
                "next_action": debrief.get("next_action"),
            }
        )
    return out

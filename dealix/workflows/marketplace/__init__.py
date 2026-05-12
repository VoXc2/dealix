"""
Workflow marketplace — installable LangGraph + Inngest workflow
templates that a customer can pull into their tenant in one click.

Each entry under `dealix/workflows/marketplace/<workflow_id>/`:
- `workflow.yaml` — metadata (id, name, description, locale, agents
  used, expected billable events, install instructions).
- `graph.py` — actual LangGraph builder (optional; we ship the
  reference for `lead_to_booking` and `proposal_to_contract`).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from core.logging import get_logger

log = get_logger(__name__)

_HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Workflow:
    id: str
    name: str
    description: str
    agents: list[str]
    locale: str
    version: str


def list_all() -> list[Workflow]:
    out: list[Workflow] = []
    for child in _HERE.iterdir():
        cfg = child / "workflow.yaml"
        if not cfg.is_file():
            continue
        try:
            raw = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
            out.append(
                Workflow(
                    id=str(raw.get("id", child.name)),
                    name=str(raw.get("name", child.name)),
                    description=str(raw.get("description", "")),
                    agents=list(raw.get("agents", []) or []),
                    locale=str(raw.get("locale", "ar")),
                    version=str(raw.get("version", "v1")),
                )
            )
        except Exception:
            log.exception("workflow_marketplace_load_failed", path=str(cfg))
    return sorted(out, key=lambda w: w.id)


def by_id(workflow_id: str) -> Workflow | None:
    for w in list_all():
        if w.id == workflow_id:
            return w
    return None

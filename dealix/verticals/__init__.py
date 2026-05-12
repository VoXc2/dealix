"""
Industry vertical bundles — pre-configured agent + workflow + prompt
+ landing bundles per sector. Customers pick a vertical at onboarding
and everything is pre-set.

8 sectors shipped today:
    real-estate, hospitality, construction, healthcare, education,
    food-and-beverage, legal, financial-services.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from core.logging import get_logger

log = get_logger(__name__)

_HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Vertical:
    id: str
    label_ar: str
    label_en: str
    description_ar: str
    description_en: str
    agents: list[str]
    workflows: list[str]
    pricing_default_plan: str
    lead_form_fields: list[dict[str, Any]]


def _load_one(slug: str) -> Vertical | None:
    base = _HERE / slug
    config = base / "config.yaml"
    if not config.is_file():
        return None
    raw = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
    return Vertical(
        id=slug,
        label_ar=str(raw.get("label_ar", "")),
        label_en=str(raw.get("label_en", "")),
        description_ar=str(raw.get("description_ar", "")),
        description_en=str(raw.get("description_en", "")),
        agents=list(raw.get("agents", []) or []),
        workflows=list(raw.get("workflows", []) or []),
        pricing_default_plan=str(raw.get("pricing_default_plan", "starter")),
        lead_form_fields=list(raw.get("lead_form_fields", []) or []),
    )


def list_all() -> list[Vertical]:
    out: list[Vertical] = []
    for child in _HERE.iterdir():
        if not child.is_dir() or child.name.startswith("_"):
            continue
        v = _load_one(child.name)
        if v is not None:
            out.append(v)
    return sorted(out, key=lambda v: v.id)


def by_id(vertical_id: str) -> Vertical | None:
    return _load_one(vertical_id)

"""
Doctrine guard — no ungoverned engine.

Operationalizes two non-negotiables for the engine layer:
  * no_unbounded_agents  — every engine declares non-empty governance hooks.
  * no_silent_failures   — unbuilt capabilities raise, never fake a result.

It also scans the engine layer for forbidden scraping-style code.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from dealix.engines import ENGINE_REGISTRY
from dealix.engines.base import EngineSpec, EngineStatus, PlannedCapabilityError

_SUSPICIOUS_NAMES = ("scraper", "crawler", "harvest")


def test_every_engine_declares_governance_hooks() -> None:
    """no_unbounded_agents — no engine may act outside governance's reach."""
    for spec in ENGINE_REGISTRY.all():
        assert spec.governance_hooks, f"Engine '{spec.engine_id}' declares no governance hooks"


def test_engine_spec_rejects_empty_governance_hooks() -> None:
    """The spec contract itself forbids an ungoverned engine."""
    with pytest.raises(ValueError, match="governance hook"):
        EngineSpec(
            engine_id="rogue",
            number=1,
            name_en="Rogue",
            name_ar="مارق",
            responsibility="acts without governance",
            capabilities=("x",),
            status=EngineStatus.PLANNED,
            wraps=(),
            governance_hooks=(),  # forbidden
            roadmap_phase=9,
        )


def test_planned_capability_fails_loudly() -> None:
    """no_silent_failures — an unbuilt capability raises PlannedCapabilityError."""
    from dealix.engines.workflow import WorkflowEngine

    with pytest.raises(PlannedCapabilityError):
        WorkflowEngine().orchestrate()


def test_no_scraping_style_code_in_engine_layer() -> None:
    """The engine layer carries no scraping/crawling/harvesting code."""
    root = Path(__file__).resolve().parent.parent / "dealix" / "engines"
    offenders: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            path = Path(dirpath) / fname
            text = path.read_text(encoding="utf-8", errors="ignore")
            lowered = text.lower()
            if any(name in fname.lower() for name in _SUSPICIOUS_NAMES):
                offenders.append(f"{path} -> suspicious filename")
            if "requests.get(" in lowered and re.search(r"https?://", lowered):
                offenders.append(f"{path} -> outbound http fetch")
    assert not offenders, "Forbidden code in engine layer:\n" + "\n".join(offenders)

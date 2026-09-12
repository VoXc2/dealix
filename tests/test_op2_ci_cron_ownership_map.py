"""Contracts for the OP2 CI-cron ownership map (GitHub Actions cron plane)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data" / "commercial" / "op2_ci_cron_ownership_map_v1.json"


def _load_module():
    path = ROOT / "scripts" / "ops" / "op2_ci_cron_ownership_map.py"
    spec = importlib.util.spec_from_file_location("op2_ci_cron", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ci = _load_module()


def _payload() -> dict:
    return json.loads(MAP.read_text(encoding="utf-8"))


def test_map_covers_the_ci_cron_plane() -> None:
    payload = _payload()
    assert payload["scope"] == "GITHUB_ACTIONS_CRON_PLANE"
    assert payload["workflow_count"] >= 20


def test_duplicate_slots_are_flagged_for_review() -> None:
    payload = _payload()
    for cron, files in payload["duplicate_slots"].items():
        assert len(files) >= 2, cron
    flagged = [w for w in payload["workflows"] if w["classification"] == "COLLISION_REVIEW"]
    assert len(flagged) >= len(payload["duplicate_slots"])


def test_map_is_read_only_and_complementary() -> None:
    payload = _payload()
    assert payload["read_only"] is True
    assert "audit_dealix_schedulers" in payload["complements"]


def test_map_is_deterministic() -> None:
    rebuilt = ci.build_map()
    stored = _payload()
    assert rebuilt["workflow_count"] == stored["workflow_count"]
    assert rebuilt["duplicate_slots"].keys() == stored["duplicate_slots"].keys()

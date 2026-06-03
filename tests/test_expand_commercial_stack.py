"""Tests for commercial expansion scripts (targeting + social queue)."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import yaml

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV
from dealix.commercial_ops.targeting_csv import TARGET_FIELDS

ROOT = Path(__file__).resolve().parents[1]


def test_expand_agency_targets_wave2_on_copy(tmp_path: Path) -> None:
    dest = tmp_path / "agency_accounts_seed.csv"
    dest.write_text(AGENCY_TARGETS_CSV.read_text(encoding="utf-8"), encoding="utf-8")
    # Patch path via env not supported — test _append_rows via import after chdir
    from scripts.expand_agency_targets_seed import _append_rows

    with dest.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    before = len(rows)
    expanded = _append_rows(rows, need=95 - before, min_rows=95)
    assert len(expanded) >= 95
    assert expanded[0].keys() >= set(TARGET_FIELDS)


def test_expand_social_queue_adds_weeks_13_16() -> None:
    queue = Path("dealix/config/social_content_queue.yaml")
    data = yaml.safe_load(queue.read_text(encoding="utf-8")) or {}
    posts = data.get("posts") or []
    keys = {(int(p["week"]), int(p["day"])) for p in posts if "week" in p and "day" in p}
    assert (13, 0) in keys or data.get("cycle_weeks", 12) >= 13

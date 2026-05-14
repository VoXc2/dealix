"""The cap-table ratios MUST sum to exactly 100.0%.

Float tolerance: 0.001. Any drift indicates a missed entry or an
unallocated pool that needs reconciliation.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CAP_TABLE = REPO_ROOT / "data" / "cap_table.json"


def test_cap_table_file_exists():
    assert CAP_TABLE.exists()


def test_ratios_sum_to_exactly_100():
    data = json.loads(CAP_TABLE.read_text(encoding="utf-8"))
    holders = data.get("holders") or []
    total = sum(float(h.get("ratio_pct", 0.0)) for h in holders)
    assert abs(total - 100.0) < 0.001, (
        f"cap-table ratios sum to {total}, not 100.0. "
        f"Holders: {[(h.get('holder'), h.get('ratio_pct')) for h in holders]}"
    )


def test_every_holder_has_required_fields():
    data = json.loads(CAP_TABLE.read_text(encoding="utf-8"))
    for i, h in enumerate(data.get("holders") or []):
        for key in ("holder", "class", "ratio_pct"):
            assert key in h, f"holder[{i}] missing {key}"
        assert isinstance(h["ratio_pct"], (int, float))
        assert 0 <= h["ratio_pct"] <= 100


def test_doctrine_version_is_pinned():
    data = json.loads(CAP_TABLE.read_text(encoding="utf-8"))
    v = data.get("doctrine_version") or ""
    import re
    assert re.match(r"^v\d+\.\d+\.\d+$", v), (
        f"cap-table doctrine_version must be semver, got {v!r}"
    )

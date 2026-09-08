from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "config" / "oss" / "capability_top50_v1.tsv"
V2 = ROOT / "config" / "oss" / "capability_frontier_v2.tsv"

ALLOWED = {
    "ADOPT_NOW",
    "ADOPT_NOW_BOUNDED",
    "ADOPT_FOR_ACCEPTANCE",
    "ALREADY_BOUNDED",
    "PILOT_ISOLATED",
    "DEFER",
    "DEFER_MEASURED_GAP",
    "REJECT_DUPLICATE_DEFAULT",
}
OWNERS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_frontier_v2_contract() -> None:
    old = _read(V1)
    rows = _read(V2)
    assert len(old) == 50
    assert len(rows) == 50
    assert [int(row["rank"]) for row in rows] == list(range(51, 101))
    assert len({row["id"] for row in rows}) == 50
    assert len({row["repository"].lower() for row in rows}) == 50
    assert not ({row["decision"] for row in rows} - ALLOWED)
    assert not ({row["owner"] for row in rows} - OWNERS)

    old_ids = {row["id"].lower() for row in old}
    old_repos = {row["repository"].lower() for row in old}
    assert not (old_ids & {row["id"].lower() for row in rows})
    assert not (old_repos & {row["repository"].lower() for row in rows})

    for row in rows:
        for field in ("problem_solved", "duplication_guard", "benchmark", "acceptance", "rollback"):
            assert row[field].strip(), f"{row['id']} missing {field}"


def test_no_bulk_install_or_parallel_authority_language() -> None:
    text = V2.read_text(encoding="utf-8").lower()
    assert "bulk install" not in text
    assert "automatic dns mutation" not in text
    assert "no live outbound calling" in text or "no external dialing" in text

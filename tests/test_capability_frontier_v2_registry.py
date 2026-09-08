from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "config" / "oss" / "capability_top50_v1.tsv"
V2 = ROOT / "config" / "oss" / "capability_frontier_v2.tsv"
LICENSE_GATES = ROOT / "config" / "oss" / "capability_frontier_v2_license_gates.tsv"

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


def test_restrictive_conditional_or_unmaintained_tools_have_explicit_gates() -> None:
    gates = {row["id"]: row for row in _read(LICENSE_GATES)}
    assert gates["pymupdf"]["license_state"] == "HOLD_LICENSE_REVIEW"
    assert "AGPL" in gates["pymupdf"]["requirement"]
    assert gates["marker"]["license_state"] == "HOLD_MODEL_WEIGHT_LICENSE_REVIEW"
    assert "model-weight" in gates["marker"]["requirement"]
    assert gates["mineru"]["license_state"] == "PILOT_WITH_ATTRIBUTION_AND_THRESHOLD_CHECK"
    assert "attribution" in gates["mineru"]["requirement"].lower()
    assert gates["llm_guard"]["license_state"] == "REJECT_ARCHIVED_UPSTREAM"
    assert "archived" in gates["llm_guard"]["requirement"].lower()

"""Source attribution checks for tabular intake."""

from __future__ import annotations

from typing import Any


def row_has_source(row: dict[str, Any]) -> bool:
    return bool(str(row.get("source", "")).strip())


def source_coverage_ratio(rows: list[dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    ok = sum(1 for r in rows if row_has_source(r))
    return round(ok / len(rows), 4)


def summarize_sources(rows: list[dict[str, Any]], *, limit: int = 20) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for r in rows:
        s = str(r.get("source", "")).strip() or "(empty)"
        counts[s] = counts.get(s, 0) + 1
    top = sorted(counts.items(), key=lambda x: -x[1])[:limit]
    return {"distinct_sources": len(counts), "top_sources": top, "coverage": source_coverage_ratio(rows)}

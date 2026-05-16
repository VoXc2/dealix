"""Executive knowledge index — local docs metadata search (no scraping)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def build_docs_index(repo_root: Path | None = None) -> list[dict[str, Any]]:
    root = repo_root or Path(__file__).resolve().parents[2]
    docs = root / "docs"
    if not docs.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        title = path.stem.replace("_", " ")
        rows.append({"path": rel, "title": title, "bytes": path.stat().st_size})
    return rows


def search_docs(query: str, *, limit: int = 20, repo_root: Path | None = None) -> list[dict[str, Any]]:
    q = query.strip().lower()
    if not q:
        return []
    hits: list[dict[str, Any]] = []
    for row in build_docs_index(repo_root):
        hay = f"{row['path']} {row['title']}".lower()
        if q in hay:
            hits.append(row)
        if len(hits) >= limit:
            break
    return hits

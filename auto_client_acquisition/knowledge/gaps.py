"""Knowledge gap tracking.

A gap = a query the KB could not answer with an approved article. Gaps
feed the founder a backlog of articles to write. Repeated identical
queries increment ``hit_count`` instead of creating duplicate rows.
"""

from __future__ import annotations

import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = REPO_ROOT / "data" / "knowledge"


def _now() -> datetime:
    return datetime.now(UTC)


class KnowledgeGap(BaseModel):
    """An unanswered query awaiting a founder-authored article."""

    model_config = ConfigDict(extra="forbid")

    gap_id: str = Field(default_factory=lambda: f"gap_{uuid4().hex[:12]}")
    query_text: str
    normalized: str = ""
    hit_count: int = 1
    status: str = "open"  # open | resolved
    resolved_article_id: str | None = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


def _normalize(query: str) -> str:
    return " ".join((query or "").lower().split())


class GapStore:
    """Thread-safe gap store with JSONL persistence."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, KnowledgeGap] = {}
        self._base = Path(base_dir) if base_dir else DEFAULT_DIR
        self._base.mkdir(parents=True, exist_ok=True)
        self._log = self._base / "gaps.jsonl"
        self._load()

    def _load(self) -> None:
        if not self._log.exists():
            return
        try:
            with self._log.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        gap = KnowledgeGap.model_validate_json(line)
                    except Exception:  # noqa: BLE001
                        continue
                    self._items[gap.gap_id] = gap
        except OSError:
            pass

    def _persist(self, gap: KnowledgeGap) -> None:
        try:
            with self._log.open("a", encoding="utf-8") as fh:
                fh.write(gap.model_dump_json() + "\n")
        except OSError:
            pass

    def record(self, query: str) -> KnowledgeGap:
        """Record an unanswered query — increments an existing open gap if any."""
        normalized = _normalize(query)
        with self._lock:
            for gap in self._items.values():
                if gap.status == "open" and gap.normalized == normalized:
                    gap.hit_count += 1
                    gap.updated_at = _now()
                    self._persist(gap)
                    return gap
            gap = KnowledgeGap(query_text=query, normalized=normalized)
            self._items[gap.gap_id] = gap
            self._persist(gap)
            return gap

    def resolve(self, gap_id: str, article_id: str | None = None) -> KnowledgeGap:
        with self._lock:
            gap = self._items.get(gap_id)
            if gap is None:
                raise ValueError(f"knowledge gap {gap_id} not found")
            gap.status = "resolved"
            gap.resolved_article_id = article_id
            gap.updated_at = _now()
            self._persist(gap)
        return gap

    def list(self, *, status: str | None = None) -> list[KnowledgeGap]:
        with self._lock:
            rows = list(self._items.values())
        if status:
            rows = [g for g in rows if g.status == status]
        rows.sort(key=lambda g: (g.hit_count, g.updated_at), reverse=True)
        return rows

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            try:
                if self._log.exists():
                    self._log.unlink()
            except OSError:
                pass


_DEFAULT: GapStore | None = None


def get_default_gap_store() -> GapStore:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = GapStore(os.getenv("DEALIX_KNOWLEDGE_DIR"))
    return _DEFAULT


def reset_default_gap_store() -> None:
    global _DEFAULT
    _DEFAULT = None


def record_gap(query: str) -> KnowledgeGap:
    """Record an unanswered query in the default gap store."""
    return get_default_gap_store().record(query)

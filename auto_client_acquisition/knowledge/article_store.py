"""Knowledge article store — in-memory with JSONL persistence.

Articles are mutable (draft → approved, content edits, soft-delete), so
unlike the append-only evidence ledger this store keeps a live dict.
Durability: every mutation appends the article's full current state to a
JSONL log; on load the log is replayed with last-write-wins per id.
"""

from __future__ import annotations

import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = REPO_ROOT / "data" / "knowledge"

VALID_STATUSES: frozenset[str] = frozenset({"draft", "approved", "archived"})
_EDITABLE_FIELDS: frozenset[str] = frozenset(
    {"title_ar", "title_en", "body_ar", "body_en", "tags", "category", "source"}
)


def _now() -> datetime:
    return datetime.now(UTC)


class KnowledgeArticle(BaseModel):
    """One knowledge-base article (bilingual)."""

    model_config = ConfigDict(extra="forbid")

    article_id: str = Field(default_factory=lambda: f"kb_{uuid4().hex[:12]}")
    tenant_id: str | None = None
    slug: str = ""
    title_ar: str = ""
    title_en: str = ""
    body_ar: str = ""
    body_en: str = ""
    tags: list[str] = Field(default_factory=list)
    category: str = "general"
    status: str = "draft"
    source: str = ""
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    deleted_at: datetime | None = None


class ArticleStore:
    """Thread-safe knowledge article store with JSONL persistence."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, KnowledgeArticle] = {}
        self._base = Path(base_dir) if base_dir else DEFAULT_DIR
        self._base.mkdir(parents=True, exist_ok=True)
        self._log = self._base / "articles.jsonl"
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
                        art = KnowledgeArticle.model_validate_json(line)
                    except Exception:  # noqa: BLE001 — skip corrupt lines
                        continue
                    self._items[art.article_id] = art
        except OSError:
            pass

    def _persist(self, art: KnowledgeArticle) -> None:
        try:
            with self._log.open("a", encoding="utf-8") as fh:
                fh.write(art.model_dump_json() + "\n")
        except OSError:
            pass

    # ─── Mutations ───────────────────────────────────────────────

    def create(self, art: KnowledgeArticle) -> KnowledgeArticle:
        """Persist a new article. New articles always start as ``draft``."""
        art.status = "draft"
        art.created_at = _now()
        art.updated_at = art.created_at
        with self._lock:
            self._items[art.article_id] = art
            self._persist(art)
        return art

    def update(self, article_id: str, patch: dict[str, Any]) -> KnowledgeArticle:
        """Edit content fields. Never flips ``status`` (use ``set_status``)."""
        with self._lock:
            art = self._require(article_id)
            for key, value in patch.items():
                if key in _EDITABLE_FIELDS:
                    setattr(art, key, value)
            art.updated_at = _now()
            self._persist(art)
        return art

    def set_status(self, article_id: str, status: str) -> KnowledgeArticle:
        """Transition status. Called by the approval-gated publish flow."""
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {status}")
        with self._lock:
            art = self._require(article_id)
            art.status = status
            art.updated_at = _now()
            self._persist(art)
        return art

    def soft_delete(self, article_id: str) -> KnowledgeArticle:
        with self._lock:
            art = self._require(article_id)
            art.deleted_at = _now()
            art.updated_at = art.deleted_at
            self._persist(art)
        return art

    # ─── Reads ───────────────────────────────────────────────────

    def get(self, article_id: str, *, include_deleted: bool = False) -> KnowledgeArticle | None:
        with self._lock:
            art = self._items.get(article_id)
        if art is None:
            return None
        if art.deleted_at is not None and not include_deleted:
            return None
        return art

    def list(
        self,
        *,
        status: str | None = None,
        category: str | None = None,
        tenant_id: str | None = None,
        include_deleted: bool = False,
    ) -> list[KnowledgeArticle]:
        with self._lock:
            rows = list(self._items.values())
        out = []
        for art in rows:
            if art.deleted_at is not None and not include_deleted:
                continue
            if status and art.status != status:
                continue
            if category and art.category != category:
                continue
            if tenant_id and art.tenant_id != tenant_id:
                continue
            out.append(art)
        out.sort(key=lambda a: a.updated_at, reverse=True)
        return out

    # ─── Test helpers ────────────────────────────────────────────

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            try:
                if self._log.exists():
                    self._log.unlink()
            except OSError:
                pass

    def _require(self, article_id: str) -> KnowledgeArticle:
        art = self._items.get(article_id)
        if art is None:
            raise ValueError(f"knowledge article {article_id} not found")
        return art


_DEFAULT: ArticleStore | None = None


def get_default_article_store() -> ArticleStore:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = ArticleStore(os.getenv("DEALIX_KNOWLEDGE_DIR"))
    return _DEFAULT


def reset_default_article_store() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT
    _DEFAULT = None

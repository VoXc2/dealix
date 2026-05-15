"""Personal Operator memory store.

In-memory by default; **persistent** when constructed with a ``path`` (or
via ``load_operator_memory``) — append-only JSONL, the value_ledger store
pattern. Items carry a ``tenant_id`` so a workspace can load only its own
memory. Secret-like content is refused on write.
"""

from __future__ import annotations

import json
import os
import re
import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4


class MemoryType(StrEnum):
    PROFILE = "profile"
    GOAL = "goal"
    PREFERENCE = "preference"
    RELATIONSHIP = "relationship"
    OPPORTUNITY = "opportunity"
    DECISION = "decision"
    MEETING = "meeting"
    FOLLOWUP = "followup"
    LAUNCH_NOTE = "launch_note"
    PROJECT_NOTE = "project_note"


_SECRET_PATTERNS = (
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.I),
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
    re.compile(r"Bearer\s+[a-zA-Z0-9\-_.]{20,}", re.I),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
    re.compile(r"xox[baprs]-[a-zA-Z0-9\-]{10,}", re.I),
)

_DEFAULT_PATH = "var/operator-memory.jsonl"
_lock = threading.Lock()


@dataclass
class PersonalMemoryItem:
    id: str
    memory_type: MemoryType
    title: str
    body: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)
    tenant_id: str = ""


@dataclass
class PersonalOperatorMemory:
    """Operator memory. Pass ``path`` to persist; omit it to stay in-memory."""

    items: list[PersonalMemoryItem] = field(default_factory=list)
    path: Path | None = None
    tenant_id: str | None = None

    def __post_init__(self) -> None:
        if self.path is not None and not self.items:
            self.items = _load_items(self.path, self.tenant_id)

    def add(self, item: PersonalMemoryItem) -> PersonalMemoryItem:
        self.items.append(item)
        if self.path is not None:
            _append_item(self.path, item)
        return item


def looks_like_secret(text: str) -> bool:
    """Return True if text resembles API keys or private material."""
    return any(pattern.search(text) for pattern in _SECRET_PATTERNS)


def add_memory(
    store: PersonalOperatorMemory,
    *,
    memory_type: MemoryType,
    title: str,
    body: str,
    metadata: dict[str, Any] | None = None,
    tenant_id: str = "",
) -> dict[str, Any]:
    if looks_like_secret(body) or looks_like_secret(title):
        return {
            "ok": False,
            "error": "secret_like_content_blocked",
            "message": "Do not store API keys or tokens in operator memory.",
        }
    item = PersonalMemoryItem(
        id=f"mem_{uuid4().hex[:12]}",
        memory_type=memory_type,
        title=title.strip(),
        body=body.strip(),
        metadata=dict(metadata or {}),
        tenant_id=tenant_id or (store.tenant_id or ""),
    )
    store.add(item)
    return {"ok": True, "item": _item_to_dict(item)}


def list_memories(
    store: PersonalOperatorMemory,
    *,
    memory_type: MemoryType | None = None,
    tenant_id: str | None = None,
) -> list[dict[str, Any]]:
    items = store.items
    if memory_type is not None:
        items = [i for i in items if i.memory_type == memory_type]
    if tenant_id is not None:
        items = [i for i in items if i.tenant_id == tenant_id]
    return [_item_to_dict(i) for i in items]


def search_memories(
    store: PersonalOperatorMemory, query: str, limit: int = 20
) -> list[dict[str, Any]]:
    q = query.lower().strip()
    if not q:
        return []
    hits: list[tuple[int, PersonalMemoryItem]] = []
    for item in store.items:
        hay = f"{item.title}\n{item.body}".lower()
        score = sum(hay.count(term) for term in q.split() if len(term) > 1)
        if score:
            hits.append((score, item))
    hits.sort(key=lambda x: x[0], reverse=True)
    return [_item_to_dict(i) for _, i in hits[:limit]]


def summarize_memory(store: PersonalOperatorMemory) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    for item in store.items:
        k = item.memory_type.value
        by_type[k] = by_type.get(k, 0) + 1
    return {
        "total": len(store.items),
        "by_type": by_type,
        "latest_titles": [i.title for i in store.items[-5:]],
    }


# ── Persistence ───────────────────────────────────────────────────────


def _resolve_path(path: Path | str | None) -> Path:
    p = Path(path or os.environ.get("DEALIX_OPERATOR_MEMORY_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        # memory.py → personal_operator → auto_client_acquisition → repo root
        p = Path(__file__).resolve().parents[2] / p
    return p


def load_operator_memory(
    path: Path | str | None = None, tenant_id: str | None = None
) -> PersonalOperatorMemory:
    """Load a persistent operator memory (creates the file lazily on first write)."""
    return PersonalOperatorMemory(path=_resolve_path(path), tenant_id=tenant_id)


def _append_item(path: Path, item: PersonalMemoryItem) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_item_to_dict(item), ensure_ascii=False) + "\n")


def _load_items(path: Path, tenant_id: str | None) -> list[PersonalMemoryItem]:
    if not path.exists():
        return []
    out: list[PersonalMemoryItem] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = _item_from_dict(json.loads(line))
            except Exception:  # noqa: S112 — best-effort: skip a corrupt line
                continue
            if tenant_id is not None and item.tenant_id != tenant_id:
                continue
            out.append(item)
    return out


def clear_for_test(path: Path | str | None = None) -> None:
    """Test-only: truncate the JSONL store."""
    p = _resolve_path(path)
    if p.exists():
        with _lock:
            p.write_text("", encoding="utf-8")


def _item_to_dict(item: PersonalMemoryItem) -> dict[str, Any]:
    return {
        "id": item.id,
        "memory_type": item.memory_type.value,
        "title": item.title,
        "body": item.body,
        "created_at": item.created_at.isoformat(),
        "metadata": item.metadata,
        "tenant_id": item.tenant_id,
    }


def _item_from_dict(data: dict[str, Any]) -> PersonalMemoryItem:
    return PersonalMemoryItem(
        id=data["id"],
        memory_type=MemoryType(data["memory_type"]),
        title=data.get("title", ""),
        body=data.get("body", ""),
        created_at=datetime.fromisoformat(data["created_at"])
        if data.get("created_at")
        else datetime.now(UTC),
        metadata=dict(data.get("metadata") or {}),
        tenant_id=data.get("tenant_id", ""),
    )

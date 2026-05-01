"""Project Intelligence layer for Dealix v3.

Inspired by tools like SocraticCode, but implemented as a Dealix-owned core:
- index project files
- chunk code/docs
- prepare deterministic local embeddings hooks
- answer architectural questions with source-aware context

Production storage target: Supabase/Postgres + pgvector via the migration in
supabase/migrations/202605010001_v3_project_memory.sql.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable

TEXT_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".txt", ".sql", ".json", ".yaml", ".yml", ".html", ".css", ".toml", ".ini", ".env.example",
}

IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules", ".next", "dist", "build", "__pycache__", ".pytest_cache", ".mypy_cache",
}


@dataclass(frozen=True)
class ProjectDocument:
    path: str
    source_type: str
    content: str
    content_hash: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "source_type": self.source_type,
            "content_hash": self.content_hash,
            "metadata": self.metadata,
            "chars": len(self.content),
        }


@dataclass(frozen=True)
class ProjectChunk:
    path: str
    chunk_index: int
    content: str
    token_estimate: int
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "chunk_index": self.chunk_index,
            "content": self.content,
            "token_estimate": self.token_estimate,
            "metadata": self.metadata,
        }


def classify_path(path: str) -> str:
    p = path.lower()
    if p.startswith("api/"):
        return "api"
    if p.startswith("auto_client_acquisition/"):
        return "revenue_engine"
    if p.startswith("db/") or "migration" in p:
        return "database"
    if p.startswith("landing/") or p.endswith(".html"):
        return "frontend_landing"
    if p.startswith("docs/") or p.endswith(".md"):
        return "documentation"
    if p.startswith("tests/"):
        return "tests"
    return "code"


def should_index(path: Path) -> bool:
    if any(part in IGNORE_DIRS for part in path.parts):
        return False
    if path.is_dir():
        return False
    if path.name == ".env":
        return False
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return True
    return path.name.endswith(".env.example")


def scan_project(root: str | Path) -> list[ProjectDocument]:
    root_path = Path(root)
    docs: list[ProjectDocument] = []
    for path in root_path.rglob("*"):
        if not should_index(path):
            continue
        rel = str(path.relative_to(root_path)).replace("\\", "/")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if not content.strip():
            continue
        docs.append(
            ProjectDocument(
                path=rel,
                source_type=classify_path(rel),
                content=content,
                content_hash=sha256(content.encode("utf-8")).hexdigest(),
                metadata={"extension": path.suffix.lower(), "chars": len(content)},
            )
        )
    return docs


def chunk_text(document: ProjectDocument, *, max_chars: int = 1800, overlap: int = 180) -> list[ProjectChunk]:
    content = document.content
    chunks: list[ProjectChunk] = []
    start = 0
    index = 0
    while start < len(content):
        end = min(len(content), start + max_chars)
        window = content[start:end]
        # Prefer to cut on line boundary when possible.
        if end < len(content):
            newline = window.rfind("\n")
            if newline > max_chars * 0.55:
                end = start + newline
                window = content[start:end]
        chunks.append(
            ProjectChunk(
                path=document.path,
                chunk_index=index,
                content=window.strip(),
                token_estimate=max(1, len(window) // 4),
                metadata={"source_type": document.source_type, "content_hash": document.content_hash},
            )
        )
        index += 1
        start = max(end - overlap, end)
    return chunks


def build_index_summary(documents: Iterable[ProjectDocument]) -> dict[str, Any]:
    docs = list(documents)
    by_type: dict[str, int] = {}
    total_chars = 0
    for doc in docs:
        by_type[doc.source_type] = by_type.get(doc.source_type, 0) + 1
        total_chars += len(doc.content)
    return {
        "documents": len(docs),
        "total_chars": total_chars,
        "by_type": by_type,
        "recommended_next_step": "Generate embeddings and upsert into Supabase project_chunks.",
    }


def naive_search(documents: Iterable[ProjectDocument], query: str, limit: int = 10) -> list[dict[str, Any]]:
    terms = [term.lower() for term in query.split() if len(term) > 2]
    scored: list[tuple[int, ProjectDocument]] = []
    for doc in documents:
        text = f"{doc.path}\n{doc.content}".lower()
        score = sum(text.count(term) for term in terms)
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {"score": score, **doc.to_dict()}
        for score, doc in scored[:limit]
    ]


def explain_project_intelligence_stack() -> dict[str, Any]:
    return {
        "purpose": "Make Dealix understand its own codebase, docs, strategy, and relationships.",
        "storage": "Supabase Postgres + pgvector",
        "embedding_dimensions": 384,
        "embedding_model_options": ["gte-small local/edge", "OpenAI text-embedding-3-small", "bge-small"],
        "search_modes": ["keyword", "semantic", "hybrid", "relationship-aware"],
        "best_use": [
            "Ask what is missing before launch",
            "Find files related to a feature",
            "Generate implementation plans grounded in code",
            "Power Sami Personal Operator memory",
            "Let agents understand project relationships before editing",
        ],
    }

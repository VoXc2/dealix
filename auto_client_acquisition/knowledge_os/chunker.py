"""Deterministic, Arabic-safe text chunker.

Pure function — same input always yields the same chunks. Splits on
paragraph boundaries first, then packs paragraphs into windows bounded by
``max_chars`` with a character ``overlap`` so retrieval never loses a fact
that straddles a boundary.
"""
from __future__ import annotations

__all__ = ["chunk_text"]


def _split_paragraphs(text: str) -> list[str]:
    parts = [p.strip() for p in text.replace("\r\n", "\n").split("\n\n")]
    return [p for p in parts if p]


def chunk_text(text: str, *, max_chars: int = 900, overlap: int = 120) -> list[str]:
    """Split ``text`` into overlapping chunks no longer than ``max_chars``.

    Operates on characters (no word-boundary assumptions) so Arabic, English,
    and mixed scripts all chunk identically.
    """
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap must be >= 0 and < max_chars")

    clean = text.strip()
    if not clean:
        return []

    # Pack paragraphs greedily into chunks.
    chunks: list[str] = []
    current = ""
    for para in _split_paragraphs(clean):
        if not current:
            current = para
        elif len(current) + 2 + len(para) <= max_chars:
            current = f"{current}\n\n{para}"
        else:
            chunks.append(current)
            current = para
        # A single paragraph longer than max_chars: hard-window it.
        while len(current) > max_chars:
            cut = current.rfind(" ", 0, max_chars)
            if cut <= 0:
                cut = max_chars
            chunks.append(current[:cut].strip())
            current = current[max(0, cut - overlap):].strip()
    if current:
        chunks.append(current)
    return [c for c in chunks if c]

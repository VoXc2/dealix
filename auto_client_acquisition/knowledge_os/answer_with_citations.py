"""Answer with explicit sources (no source => no answer policy at API boundary)."""

from __future__ import annotations

from typing import Any


def answer_with_citations(
    question: str,
    *,
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Deterministic policy: if no sources, return insufficient_evidence.

    ``sources`` items should include ``id`` and ``excerpt`` (or ``text``).
    """
    if not sources:
        return {
            "question": question,
            "answer": "",
            "citations": [],
            "insufficient_evidence": True,
        }
    citations = []
    for s in sources:
        sid = str(s.get("id", "source"))
        excerpt = str(s.get("excerpt") or s.get("text") or "")[:800]
        citations.append({"id": sid, "excerpt": excerpt})
    # Minimal answer: concatenate excerpts with separators (deterministic, not LLM).
    merged = "\n---\n".join(c["excerpt"] for c in citations if c["excerpt"])
    return {
        "question": question,
        "answer": merged[:4000],
        "citations": citations,
        "insufficient_evidence": False,
    }

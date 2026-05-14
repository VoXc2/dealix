"""Lightweight eval helpers for knowledge policy."""

from __future__ import annotations

from auto_client_acquisition.knowledge_os.answer_with_citations import answer_with_citations


def eval_no_source_policy() -> bool:
    """Return True if empty sources always block."""
    out = answer_with_citations("test", sources=[])
    return bool(out.get("insufficient_evidence"))

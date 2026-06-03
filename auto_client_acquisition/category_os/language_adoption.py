"""Language adoption — preferred vs avoided positioning terms."""

from __future__ import annotations

PREFERRED_CATEGORY_TERMS: tuple[str, ...] = (
    "governed ai operations",
    "revenue intelligence",
    "company brain",
    "proof pack",
    "capability score",
    "transformation gap",
    "governance runtime",
    "ai control plane",
    "capital ledger",
    "dealix method",
)

AVOIDED_POSITIONING_TERMS: tuple[str, ...] = (
    "chatbot agency",
    "automation agency",
    "lead scraper",
    "cold whatsapp",
    "guaranteed roi",
    "ai tool only",
)


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def preferred_term_hits(text: str) -> int:
    """Count how many preferred phrases appear in text (non-overlapping greedy skipped — simple contains)."""
    lowered = _normalize(text)
    return sum(1 for term in PREFERRED_CATEGORY_TERMS if term in lowered)


def avoided_term_hits(text: str) -> int:
    lowered = _normalize(text)
    return sum(1 for term in AVOIDED_POSITIONING_TERMS if term in lowered)


def language_adoption_index(text: str) -> tuple[int, int]:
    """Return (preferred_hits, avoided_hits) for quick dashboards."""
    return preferred_term_hits(text), avoided_term_hits(text)

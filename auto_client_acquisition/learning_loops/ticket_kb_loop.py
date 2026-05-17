"""Learning loop (b) — recurring support tickets to KB-article candidates.

Reads support tickets (from ``support_inbox.state_store`` or the
``data/support_tickets.jsonl`` store) and turns recurring ticket
categories into knowledge-base gap article candidates.

Pure-function core for aggregation. The JSONL read is isolated in one
helper and respects the ``DEALIX_SUPPORT_TICKETS_PATH`` env override
so tests stay hermetic. The result is a suggestion set — nothing is
auto-published.
"""
from __future__ import annotations

import json
import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# A ticket category becomes a KB-gap candidate once it recurs at least
# this many times — repetition is the signal of a real knowledge gap.
DEFAULT_RECURRENCE_THRESHOLD = 3

# Human-readable article-title suggestions per support category.
_CATEGORY_ARTICLE_HINT: dict[str, dict[str, str]] = {
    "onboarding": {
        "en": "Onboarding walkthrough — first 7 days",
        "ar": "دليل البدء — أول 7 أيام",
    },
    "billing": {
        "en": "Billing FAQ — invoices and charges explained",
        "ar": "أسئلة الفوترة — شرح الفواتير والرسوم",
    },
    "payment": {
        "en": "Payment methods and troubleshooting",
        "ar": "طرق الدفع وحل المشكلات",
    },
    "technical_issue": {
        "en": "Common technical issues and fixes",
        "ar": "المشكلات التقنية الشائعة وحلولها",
    },
    "connector_setup": {
        "en": "Connector setup guide",
        "ar": "دليل إعداد الموصّلات",
    },
    "diagnostic_question": {
        "en": "Understanding your diagnostic results",
        "ar": "فهم نتائج التشخيص",
    },
    "proof_pack_question": {
        "en": "What is in a Proof Pack",
        "ar": "ماذا يحتوي Proof Pack",
    },
    "privacy_pdpl": {
        "en": "Privacy and PDPL compliance overview",
        "ar": "نظرة عامة على الخصوصية وامتثال PDPL",
    },
    "refund": {
        "en": "Refund policy and how to request one",
        "ar": "سياسة الاسترداد وكيفية طلبه",
    },
    "upgrade_question": {
        "en": "Plan comparison and upgrade guide",
        "ar": "مقارنة الباقات ودليل الترقية",
    },
}


@dataclass
class KBArticleCandidate:
    """A candidate KB article suggested by recurring tickets."""

    category: str
    ticket_count: int
    suggested_title_en: str
    suggested_title_ar: str
    priority: str  # high / medium

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "ticket_count": self.ticket_count,
            "suggested_title_en": self.suggested_title_en,
            "suggested_title_ar": self.suggested_title_ar,
            "priority": self.priority,
        }


def _support_tickets_path() -> Path:
    """Resolve the support-tickets JSONL path (env override aware)."""
    raw = os.environ.get("DEALIX_SUPPORT_TICKETS_PATH")
    if raw:
        return Path(raw)
    return Path("data") / "support_tickets.jsonl"


def load_ticket_categories() -> list[str]:
    """Read support-ticket categories from the JSONL store.

    Returns an empty list when the store does not exist yet — the loop
    then reports no candidates rather than crashing.
    """
    path = _support_tickets_path()
    if not path.exists():
        return []
    categories: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        cat = str(row.get("category") or "unknown")
        categories.append(cat)
    return categories


def _category_of(ticket: Any) -> str:
    if isinstance(ticket, str):
        return ticket
    if isinstance(ticket, dict):
        return str(ticket.get("category") or "unknown")
    return str(getattr(ticket, "category", "unknown") or "unknown")


def build_kb_candidates(
    tickets: Iterable[Any],
    *,
    recurrence_threshold: int = DEFAULT_RECURRENCE_THRESHOLD,
) -> list[KBArticleCandidate]:
    """Aggregate recurring ticket categories into KB-article candidates.

    ``tickets`` may be Ticket objects, dicts, or plain category
    strings. A category becomes a candidate once it recurs at least
    ``recurrence_threshold`` times. ``unknown`` is excluded — it points
    to a classifier gap, not a KB gap.
    """
    counts: dict[str, int] = {}
    for ticket in tickets:
        category = _category_of(ticket)
        if category == "unknown":
            continue
        counts[category] = counts.get(category, 0) + 1

    candidates: list[KBArticleCandidate] = []
    for category, count in counts.items():
        if count < recurrence_threshold:
            continue
        hint = _CATEGORY_ARTICLE_HINT.get(
            category,
            {
                "en": f"Knowledge article for '{category}'",
                "ar": f"مقال معرفي لـ '{category}'",
            },
        )
        candidates.append(
            KBArticleCandidate(
                category=category,
                ticket_count=count,
                suggested_title_en=hint["en"],
                suggested_title_ar=hint["ar"],
                priority="high" if count >= recurrence_threshold * 2 else "medium",
            )
        )
    return sorted(candidates, key=lambda c: (-c.ticket_count, c.category))


__all__ = [
    "DEFAULT_RECURRENCE_THRESHOLD",
    "KBArticleCandidate",
    "build_kb_candidates",
    "load_ticket_categories",
]

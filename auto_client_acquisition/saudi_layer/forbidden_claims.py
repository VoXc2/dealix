"""Forbidden Arabic marketing claims (substring checks)."""

from __future__ import annotations


def forbidden_arabic_claim_detected(text: str) -> bool:
    blob = text.lower()
    needles = ("نضمن لك", "نضمن لكم", "ضمان مبيعات", "ربح مؤكد")
    return any(n in blob for n in needles)


__all__ = ["forbidden_arabic_claim_detected"]

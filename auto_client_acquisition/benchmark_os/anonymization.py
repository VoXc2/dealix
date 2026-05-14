"""Benchmark anonymization helpers (no PII leaves this function)."""

from __future__ import annotations

import hashlib
import re


def anonymize_label(label: str) -> str:
    s = label.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if not s:
        return "unknown"
    return hashlib.sha256(s.encode()).hexdigest()[:10]


__all__ = ["anonymize_label"]

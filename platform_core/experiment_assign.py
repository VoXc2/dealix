"""Internal experiment assignment (initiative 142)."""

from __future__ import annotations

import hashlib


def assign_variant(*, experiment_id: str, subject_id: str, variants: tuple[str, ...] = ("control", "treatment")) -> str:
    if not variants:
        return "control"
    digest = hashlib.sha256(f"{experiment_id}:{subject_id}".encode()).hexdigest()
    idx = int(digest[:8], 16) % len(variants)
    return variants[idx]

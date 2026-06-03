"""Benchmark anonymization helpers (no PII leaves this function)."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from typing import Any

# Minimum distinct contributors required before an aggregate may be published.
K_ANONYMITY_THRESHOLD = 5


def anonymize_label(label: str) -> str:
    s = label.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if not s:
        return "unknown"
    return hashlib.sha256(s.encode()).hexdigest()[:10]


def is_k_anonymous(
    *,
    contributor_count: int,
    threshold: int = K_ANONYMITY_THRESHOLD,
) -> bool:
    """Return True when an aggregate has enough distinct contributors."""
    return contributor_count >= threshold


def aggregate_with_k_anonymity(
    *,
    rows: Sequence[Mapping[str, Any]],
    bucket_key: str,
    value_key: str,
    contributor_key: str = "customer_id",
    threshold: int = K_ANONYMITY_THRESHOLD,
) -> dict[str, dict[str, Any]]:
    """Aggregate ``rows`` by ``bucket_key`` and suppress small buckets.

    A bucket whose number of distinct contributors is below ``threshold``
    is marked ``suppressed`` and its mean is withheld — k-anonymity guard
    so no individual customer can be re-identified from a benchmark.
    """
    buckets: dict[str, list[tuple[Any, float]]] = {}
    for row in rows:
        bucket = str(row.get(bucket_key, "unknown"))
        contributor = row.get(contributor_key, "")
        try:
            value = float(row.get(value_key, 0.0))
        except (TypeError, ValueError):
            continue
        buckets.setdefault(bucket, []).append((contributor, value))

    out: dict[str, dict[str, Any]] = {}
    for bucket, entries in buckets.items():
        contributors = {c for c, _ in entries if c not in ("", None)}
        contributor_count = len(contributors)
        suppressed = not is_k_anonymous(
            contributor_count=contributor_count, threshold=threshold,
        )
        result: dict[str, Any] = {
            "contributors": contributor_count,
            "sample_size": len(entries),
            "suppressed": suppressed,
        }
        if suppressed:
            result["mean"] = None
            result["reason"] = "below_k_anonymity_threshold"
        else:
            values = [v for _, v in entries]
            result["mean"] = round(sum(values) / len(values), 2)
        out[bucket] = result
    return out


__all__ = [
    "K_ANONYMITY_THRESHOLD",
    "aggregate_with_k_anonymity",
    "anonymize_label",
    "is_k_anonymous",
]

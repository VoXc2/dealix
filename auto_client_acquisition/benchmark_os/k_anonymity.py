"""K-anonymity aggregation for benchmark rows (suppress small buckets)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

K_ANONYMITY_THRESHOLD = 5


def is_k_anonymous(*, contributor_count: int) -> bool:
    """Return True when a bucket has enough distinct contributors to publish."""
    return contributor_count >= K_ANONYMITY_THRESHOLD


def aggregate_with_k_anonymity(
    *,
    rows: list[dict[str, Any]],
    bucket_key: str,
    value_key: str,
) -> dict[str, dict[str, Any]]:
    """Aggregate ``rows`` into buckets, suppressing buckets below the k threshold.

    Contributors are counted by distinct ``customer_id`` where present, otherwise
    by row. Each bucket entry carries ``suppressed``, ``mean`` and ``contributors``.
    """
    values: dict[str, list[float]] = defaultdict(list)
    contributors: dict[str, set[str]] = defaultdict(set)
    for index, row in enumerate(rows):
        bucket = str(row[bucket_key])
        values[bucket].append(float(row[value_key]))
        contributor = str(row.get("customer_id", f"row-{index}"))
        contributors[bucket].add(contributor)

    result: dict[str, dict[str, Any]] = {}
    for bucket, bucket_values in values.items():
        contributor_count = len(contributors[bucket])
        if not is_k_anonymous(contributor_count=contributor_count):
            result[bucket] = {
                "suppressed": True,
                "mean": 0.0,
                "contributors": contributor_count,
            }
            continue
        result[bucket] = {
            "suppressed": False,
            "mean": round(sum(bucket_values) / len(bucket_values), 4),
            "contributors": contributor_count,
        }
    return result


__all__ = [
    "K_ANONYMITY_THRESHOLD",
    "aggregate_with_k_anonymity",
    "is_k_anonymous",
]

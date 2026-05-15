"""K-anonymity guard for benchmark aggregates.

Doctrine: no benchmark bucket may be published unless at least
``K_ANONYMITY_THRESHOLD`` distinct customers contributed to it. Buckets
below the threshold are suppressed (no mean, no count detail leaks).
"""

from __future__ import annotations

from typing import Any

K_ANONYMITY_THRESHOLD = 5


def is_k_anonymous(*, contributor_count: int) -> bool:
    """True when the distinct-contributor count meets the k-anonymity threshold."""
    return contributor_count >= K_ANONYMITY_THRESHOLD


def aggregate_with_k_anonymity(
    *,
    rows: list[dict[str, Any]],
    bucket_key: str,
    value_key: str,
    contributor_key: str = "customer_id",
) -> dict[str, dict[str, Any]]:
    """Aggregate ``rows`` into buckets, suppressing any bucket below k.

    Each result entry carries ``suppressed``; non-suppressed buckets also
    expose ``mean`` and ``contributors`` (distinct customer count).
    """
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        bucket = str(row.get(bucket_key, "unknown"))
        slot = grouped.setdefault(bucket, {"values": [], "contributors": set()})
        try:
            slot["values"].append(float(row.get(value_key, 0.0)))
        except (TypeError, ValueError):
            continue
        contributor = row.get(contributor_key)
        if contributor is not None:
            slot["contributors"].add(str(contributor))

    result: dict[str, dict[str, Any]] = {}
    for bucket, slot in grouped.items():
        contributors = len(slot["contributors"])
        if not is_k_anonymous(contributor_count=contributors):
            result[bucket] = {
                "suppressed": True,
                "reason": "below_k_anonymity_threshold",
                "k_anonymity_threshold": K_ANONYMITY_THRESHOLD,
            }
            continue
        values = slot["values"]
        mean = round(sum(values) / len(values), 2) if values else 0.0
        result[bucket] = {
            "suppressed": False,
            "mean": mean,
            "contributors": contributors,
            "sample_size": len(values),
        }
    return result


__all__ = [
    "K_ANONYMITY_THRESHOLD",
    "aggregate_with_k_anonymity",
    "is_k_anonymous",
]

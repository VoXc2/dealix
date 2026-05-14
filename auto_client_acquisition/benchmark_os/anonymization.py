"""Anonymization helpers — k-anonymity ≥ 5, aggregate-only reports.

A bucket is "safe to publish" iff it contains at least K (default 5)
distinct contributing customers. Anything below is suppressed.
"""
from __future__ import annotations

from typing import Any


K_DEFAULT = 5


def is_k_anonymous(*, contributor_count: int, k: int = K_DEFAULT) -> bool:
    return contributor_count >= k


def aggregate_with_k_anonymity(
    *,
    rows: list[dict[str, Any]],
    bucket_key: str,
    value_key: str,
    contributor_key: str = "customer_id",
    k: int = K_DEFAULT,
) -> dict[str, dict[str, Any]]:
    """Group `rows` by `bucket_key`, compute aggregate stats over `value_key`,
    suppress any bucket with fewer than `k` distinct contributors.

    Returns:
        {
          "<bucket>": {
            "count": N,
            "sum": float,
            "mean": float,
            "p_min": float, "p_max": float,
            "contributors": K,
            "suppressed": False
          },
          ...
        }
    """
    buckets: dict[str, dict[str, Any]] = {}
    for row in rows:
        bucket = str(row.get(bucket_key, "unknown"))
        contributor = str(row.get(contributor_key, ""))
        value = float(row.get(value_key, 0) or 0)
        entry = buckets.setdefault(
            bucket,
            {"_values": [], "_contributors": set()},
        )
        entry["_values"].append(value)
        if contributor:
            entry["_contributors"].add(contributor)

    result: dict[str, dict[str, Any]] = {}
    for bucket, entry in buckets.items():
        values: list[float] = entry["_values"]
        contributors = entry["_contributors"]
        n_contrib = len(contributors)
        safe = is_k_anonymous(contributor_count=n_contrib, k=k)
        if not safe:
            result[bucket] = {
                "count": len(values),
                "contributors": n_contrib,
                "suppressed": True,
                "reason": f"below_k_anonymity_threshold:{k}",
            }
        else:
            result[bucket] = {
                "count": len(values),
                "sum": round(sum(values), 2),
                "mean": round(sum(values) / max(1, len(values)), 2),
                "p_min": round(min(values), 2) if values else 0.0,
                "p_max": round(max(values), 2) if values else 0.0,
                "contributors": n_contrib,
                "suppressed": False,
            }
    return result


__all__ = ["K_DEFAULT", "aggregate_with_k_anonymity", "is_k_anonymous"]

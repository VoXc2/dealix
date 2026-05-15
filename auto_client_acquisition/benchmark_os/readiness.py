"""Safe market benchmark reports — k-anonymity + synthetic-aggregate framing.

A bucket is published only when at least ``K_ANONYMITY_THRESHOLD`` distinct
customers contribute to it; smaller buckets are suppressed so no single
customer can be re-identified from an aggregate.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.benchmark_os.methodology import methodology_footer

K_ANONYMITY_THRESHOLD = 5

_DISCLAIMER_AR = "القيمة التقديرية ليست قيمة مُتحقَّقة"
_LIMITATIONS: tuple[str, ...] = (
    "Figures are SYNTHETIC + AGGREGATED — not a verified per-company benchmark.",
    "Buckets with fewer than 5 contributing customers are suppressed (k-anonymity).",
    "The sample is non-random — drawn from Dealix engagements, not the whole market.",
    f"Estimated value is not verified value / {_DISCLAIMER_AR}.",
)


def is_k_anonymous(*, contributor_count: int) -> bool:
    """True iff a bucket has enough distinct contributors to publish safely."""
    return contributor_count >= K_ANONYMITY_THRESHOLD


def aggregate_with_k_anonymity(
    *,
    rows: Iterable[dict[str, Any]],
    bucket_key: str,
    value_key: str,
) -> dict[str, dict[str, Any]]:
    """Bucket ``rows`` by ``bucket_key``; suppress buckets below k-anonymity.

    A non-suppressed bucket reports ``mean``, ``count`` and ``contributors``;
    a suppressed bucket reports only ``suppressed`` + ``contributors``.
    """
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get(bucket_key, "")), []).append(row)

    out: dict[str, dict[str, Any]] = {}
    for bucket, brows in grouped.items():
        contributors = {
            str(r.get("customer_id", "")) for r in brows if r.get("customer_id")
        }
        n = len(contributors)
        if not is_k_anonymous(contributor_count=n):
            out[bucket] = {"suppressed": True, "contributors": n}
            continue
        values = [float(r.get(value_key, 0) or 0) for r in brows]
        out[bucket] = {
            "suppressed": False,
            "contributors": n,
            "count": len(values),
            "mean": round(sum(values) / len(values), 2) if values else 0.0,
        }
    return out


@dataclass
class ReadinessReport:
    """A safe, aggregate market-readiness report."""

    title: str = "Saudi AI Operations Readiness Report v1"
    k_anonymity_threshold: int = K_ANONYMITY_THRESHOLD
    governance_decision: str = "allow_with_review"
    methodology: str = field(default_factory=methodology_footer)
    limitations: list[str] = field(default_factory=lambda: list(_LIMITATIONS))
    buckets: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            "**SYNTHETIC + AGGREGATED** — not a verified per-company benchmark.",
            "",
            "## Methodology",
            self.methodology,
            f"k-anonymity threshold: {self.k_anonymity_threshold} contributors per bucket.",
            "",
            "## Limitations",
            *[f"- {lim}" for lim in self.limitations],
            "",
            f"> {_DISCLAIMER_AR}",
        ]
        return "\n".join(lines) + "\n"


def generate_readiness_report(
    *,
    rows: Iterable[dict[str, Any]] | None = None,
    bucket_key: str = "sector",
    value_key: str = "score",
) -> ReadinessReport:
    """Build a market-readiness report; aggregates ``rows`` when provided."""
    buckets = (
        aggregate_with_k_anonymity(rows=rows, bucket_key=bucket_key, value_key=value_key)
        if rows is not None
        else {}
    )
    return ReadinessReport(buckets=buckets)


__all__ = [
    "K_ANONYMITY_THRESHOLD",
    "ReadinessReport",
    "aggregate_with_k_anonymity",
    "generate_readiness_report",
    "is_k_anonymous",
]

"""Saudi AI Operations Readiness Report — deterministic, aggregated, governed.

The report only ever publishes synthetic + aggregated figures behind a
k-anonymity guard. No client-confidential data is ever surfaced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.benchmark_os.k_anonymity import (
    K_ANONYMITY_THRESHOLD,
    aggregate_with_k_anonymity,
)
from auto_client_acquisition.benchmark_os.methodology import methodology_footer

_REPORT_TITLE = "Saudi AI Operations Readiness Report v1"
_DISCLAIMER_AR = "القيمة التقديرية ليست قيمة مُتحقَّقة"
_DISCLAIMER_EN = "Estimated value is not verified value."

_LIMITATIONS: tuple[str, ...] = (
    "Figures are synthetic and aggregated; they are not individual advice.",
    "Buckets with fewer than the k-anonymity threshold of contributors are suppressed.",
    "Sample skews toward Dealix early adopters and is not nationally representative.",
    "Estimated outcomes are not guaranteed outcomes.",
)


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    """A governed, aggregated readiness report ready for markdown rendering."""

    title: str
    methodology: str
    k_anonymity_threshold: int
    limitations: tuple[str, ...]
    buckets: dict[str, dict[str, Any]] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            "Status: SYNTHETIC + AGGREGATED",
            "",
            "## Methodology",
            self.methodology,
            f"K-anonymity threshold: {self.k_anonymity_threshold}",
            "",
            "## Aggregated Buckets",
        ]
        if not self.buckets:
            lines.append("- No buckets met the publication threshold.")
        else:
            for bucket, stats in sorted(self.buckets.items()):
                if stats.get("suppressed"):
                    lines.append(f"- {bucket}: suppressed (below k-anonymity threshold)")
                else:
                    lines.append(
                        f"- {bucket}: mean={stats.get('mean')} "
                        f"contributors={stats.get('contributors')}"
                    )
        lines.append("")
        lines.append("## Limitations")
        for item in self.limitations:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("---")
        lines.append(f"{_DISCLAIMER_EN} / {_DISCLAIMER_AR}")
        return "\n".join(lines)


def generate_readiness_report(
    *,
    rows: list[dict[str, Any]] | None = None,
    bucket_key: str = "sector",
    value_key: str = "score",
) -> ReadinessReport:
    """Build the readiness report, k-anonymity-suppressing any thin bucket."""
    buckets: dict[str, dict[str, Any]] = {}
    if rows:
        buckets = aggregate_with_k_anonymity(
            rows=rows, bucket_key=bucket_key, value_key=value_key
        )
    return ReadinessReport(
        title=_REPORT_TITLE,
        methodology=methodology_footer(),
        k_anonymity_threshold=K_ANONYMITY_THRESHOLD,
        limitations=_LIMITATIONS,
        buckets=buckets,
        governance_decision="allow_with_review",
    )


__all__ = [
    "ReadinessReport",
    "generate_readiness_report",
]

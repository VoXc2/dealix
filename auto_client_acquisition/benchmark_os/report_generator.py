"""Benchmark report skeleton + Saudi AI Operations Readiness Report."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.benchmark_os.anonymization import (
    K_ANONYMITY_THRESHOLD,
    aggregate_with_k_anonymity,
)
from auto_client_acquisition.benchmark_os.methodology import (
    METHODOLOGY_VERSION,
    methodology_footer,
)

_READINESS_TITLE = "Saudi AI Operations Readiness Report v1"

_DISCLAIMER = (
    "Estimated value is not realised value / القيمة التقديرية ليست قيمة مُتحقَّقة."
)

_DEFAULT_LIMITATIONS: tuple[str, ...] = (
    "Figures are SYNTHETIC + AGGREGATED — not advice for any single firm.",
    "Buckets with fewer than five distinct contributors are suppressed.",
    "Benchmarks reflect Dealix-observed signals only, not the whole market.",
    "Estimated outcomes are not guaranteed outcomes.",
)


def benchmark_report_skeleton(*, title: str) -> dict[str, str]:
    return {
        "title": title,
        "methodology": "aggregated_anonymized",
        "limitations": "not_individual_advice",
        "body": "",
    }


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    """Saudi AI Operations Readiness Report — aggregated + governed."""

    title: str
    methodology: str
    k_anonymity_threshold: int
    limitations: tuple[str, ...]
    buckets: dict[str, dict[str, Any]] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "methodology": self.methodology,
            "k_anonymity_threshold": self.k_anonymity_threshold,
            "limitations": list(self.limitations),
            "buckets": self.buckets,
            "governance_decision": self.governance_decision,
            "disclaimer": _DISCLAIMER,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            "_SYNTHETIC + AGGREGATED — for orientation only._",
            "",
            "## Methodology",
            self.methodology,
            f"K-anonymity threshold: {self.k_anonymity_threshold} contributors.",
            "",
            "## Benchmarks",
        ]
        if self.buckets:
            for bucket, stats in sorted(self.buckets.items()):
                if stats.get("suppressed"):
                    lines.append(f"- {bucket}: suppressed (below k-anonymity)")
                else:
                    lines.append(
                        f"- {bucket}: mean {stats.get('mean')} "
                        f"({stats.get('contributors')} contributors)"
                    )
        else:
            lines.append("- No qualifying buckets yet.")
        lines.append("")
        lines.append("## Limitations")
        for item in self.limitations:
            lines.append(f"- {item}")
        lines.append("")
        lines.append(f"_{_DISCLAIMER}_")
        return "\n".join(lines)


def generate_readiness_report(
    *,
    rows: Sequence[Mapping[str, Any]] | None = None,
    bucket_key: str = "sector",
    value_key: str = "score",
) -> ReadinessReport:
    """Build the Saudi AI Operations Readiness Report.

    When ``rows`` are supplied they are aggregated under the k-anonymity
    guard; otherwise an empty (but well-formed) report is returned.
    """
    buckets: dict[str, dict[str, Any]] = {}
    if rows:
        buckets = aggregate_with_k_anonymity(
            rows=rows, bucket_key=bucket_key, value_key=value_key,
        )
    methodology = (
        f"{methodology_footer()} Methodology version {METHODOLOGY_VERSION}."
    )
    return ReadinessReport(
        title=_READINESS_TITLE,
        methodology=methodology,
        k_anonymity_threshold=K_ANONYMITY_THRESHOLD,
        limitations=_DEFAULT_LIMITATIONS,
        buckets=buckets,
        governance_decision="allow_with_review",
    )


__all__ = [
    "ReadinessReport",
    "benchmark_report_skeleton",
    "generate_readiness_report",
]

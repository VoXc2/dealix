"""Benchmark report generator — Saudi AI Operations Readiness.

Generates a markdown + JSON report. Always labels itself
SYNTHETIC + AGGREGATED. Methodology + limitations explicit.

This module DOES NOT pull real customer data. Callers supply
pre-aggregated synthetic rows OR explicitly-consented anonymized data.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.benchmark_os.anonymization import (
    K_DEFAULT,
    aggregate_with_k_anonymity,
)


@dataclass
class BenchmarkReport:
    report_id: str
    title: str
    generated_at: str
    methodology: str
    limitations: list[str] = field(default_factory=list)
    dimensions: dict[str, dict[str, Any]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    k_anonymity_threshold: int = K_DEFAULT
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# {self.title}")
        lines.append("")
        lines.append("> **SYNTHETIC + AGGREGATED DATA ONLY**")
        lines.append("> _No real customer metrics. Methodology disclosed below._")
        lines.append("")
        lines.append(f"_Report ID:_ `{self.report_id}`")
        lines.append(f"_Generated:_ {self.generated_at}")
        lines.append(f"_K-anonymity threshold:_ ≥ {self.k_anonymity_threshold}")
        lines.append("")
        lines.append("## Methodology")
        lines.append(self.methodology)
        lines.append("")
        if self.limitations:
            lines.append("## Limitations")
            for lim in self.limitations:
                lines.append(f"- {lim}")
            lines.append("")
        for dim, bucket_data in self.dimensions.items():
            lines.append(f"## {dim}")
            for bucket, stats in bucket_data.items():
                if stats.get("suppressed"):
                    lines.append(f"- **{bucket}**: suppressed ({stats.get('reason', '')})")
                else:
                    lines.append(
                        f"- **{bucket}**: mean {stats.get('mean')} "
                        f"(range {stats.get('p_min')}–{stats.get('p_max')}, "
                        f"n={stats.get('count')}, contributors={stats.get('contributors')})"
                    )
            lines.append("")
        if self.notes:
            lines.append("## Notes")
            for n in self.notes:
                lines.append(f"- {n}")
            lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._"
        )
        return "\n".join(lines)


_SAUDI_DEFAULT_METHODOLOGY = (
    "Aggregated synthetic data only. Five readiness dimensions: "
    "Leadership Alignment, Workflow Clarity, Data Readiness, Human "
    "Capability, Governance Maturity. Each dimension scored 0–100 across "
    "20+ synthetic Saudi B2B/training/healthcare/real-estate/logistics "
    "personas. K-anonymity threshold ≥ 5 contributors per bucket; any "
    "bucket with fewer is suppressed. This report is methodology + "
    "patterns, NOT customer attribution."
)


def _default_limitations() -> list[str]:
    return [
        "Synthetic data may not reflect real Saudi market distributions.",
        "Self-reported maturity ratings overstate readiness; observed work "
        "would lower scores by an estimated 10-20 points.",
        "K-anonymity ≥ 5 suppresses small-bucket signal; useful only at scale.",
        "Estimated values are model-derived ranges, not invoiced revenue.",
    ]


def generate_readiness_report(
    *,
    title: str = "Saudi AI Operations Readiness Report v1",
    report_id: str = "saudi-ai-ops-readiness-v1",
    synthetic_rows: list[dict[str, Any]] | None = None,
    dimensions: tuple[str, ...] = (
        "leadership_alignment",
        "workflow_clarity",
        "data_readiness",
        "human_capability",
        "governance_maturity",
    ),
    bucket_key: str = "sector",
) -> BenchmarkReport:
    """Generate the report.

    If `synthetic_rows` is None, returns a methodology-only report
    (useful for first-publish bootstrap).
    """
    dimension_buckets: dict[str, dict[str, Any]] = {}
    if synthetic_rows:
        for dim in dimensions:
            dimension_buckets[dim] = aggregate_with_k_anonymity(
                rows=synthetic_rows,
                bucket_key=bucket_key,
                value_key=dim,
                contributor_key="customer_id",
                k=K_DEFAULT,
            )
    return BenchmarkReport(
        report_id=report_id,
        title=title,
        generated_at=datetime.now(timezone.utc).isoformat(),
        methodology=_SAUDI_DEFAULT_METHODOLOGY,
        limitations=_default_limitations(),
        dimensions=dimension_buckets,
        notes=[
            "Sectors: Saudi B2B services, training academies, logistics, "
            "real estate services, healthcare admin.",
            "References the open Dealix Governed AI Operations Standard.",
        ],
        k_anonymity_threshold=K_DEFAULT,
    )


__all__ = ["BenchmarkReport", "generate_readiness_report"]

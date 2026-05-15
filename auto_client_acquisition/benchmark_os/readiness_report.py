"""Saudi AI Operations Readiness Report — synthetic, aggregated, governed."""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.benchmark_os.k_anonymity import K_ANONYMITY_THRESHOLD
from auto_client_acquisition.benchmark_os.methodology import methodology_footer

READINESS_REPORT_TITLE = "Saudi AI Operations Readiness Report v1"

_DISCLAIMER_AR = "القيمة التقديرية ليست قيمة مُتحقَّقة"


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    """Deterministic readiness report carrying methodology and limitations."""

    title: str
    k_anonymity_threshold: int
    governance_decision: str
    methodology: str
    limitations: tuple[str, ...]
    sections: tuple[str, ...] = field(default_factory=tuple)

    def to_markdown(self) -> str:
        lines: list[str] = [
            f"# {self.title}",
            "",
            "Data basis: SYNTHETIC + AGGREGATED. No individual customer is identifiable.",
            "",
            "## Methodology",
            self.methodology,
            f"K-anonymity threshold: {self.k_anonymity_threshold}.",
            "",
            "## Limitations",
        ]
        lines.extend(f"- {item}" for item in self.limitations)
        lines.extend(
            [
                "",
                "## Disclaimer",
                "Estimated value is not verified value.",
                _DISCLAIMER_AR,
            ]
        )
        return "\n".join(lines)


def generate_readiness_report() -> ReadinessReport:
    """Build the readiness report skeleton (no live customer rows required)."""
    limitations = (
        "Data is synthetic and aggregated; not individual advice.",
        f"Buckets below {K_ANONYMITY_THRESHOLD} contributors are suppressed.",
        "Estimated outcomes are not guaranteed outcomes.",
        "Report reflects observed signals only, not future performance.",
    )
    return ReadinessReport(
        title=READINESS_REPORT_TITLE,
        k_anonymity_threshold=K_ANONYMITY_THRESHOLD,
        governance_decision="allow_with_review",
        methodology=methodology_footer(),
        limitations=limitations,
        sections=(
            "operations_readiness",
            "governance_posture",
            "data_maturity",
        ),
    )


__all__ = [
    "READINESS_REPORT_TITLE",
    "ReadinessReport",
    "generate_readiness_report",
]

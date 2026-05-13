"""Case-Safe Proof Summary — anonymized version of a Proof Pack."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CaseSafeProofSummary:
    sector: str
    problem_pattern: str
    work_performed: str
    anonymized_metrics: str
    lessons: str
    general_insight: str
    client_name_disclosed: bool = False
    consent_to_publish: bool = False

    def __post_init__(self) -> None:
        if self.client_name_disclosed and not self.consent_to_publish:
            raise ValueError("client_name_disclosure_requires_consent")


def redact_to_case_safe(
    *,
    sector: str,
    problem_pattern: str,
    work_performed: str,
    anonymized_metrics: str,
    lessons: str,
    general_insight: str,
) -> CaseSafeProofSummary:
    """Construct a case-safe summary that is publishable by default."""

    return CaseSafeProofSummary(
        sector=sector,
        problem_pattern=problem_pattern,
        work_performed=work_performed,
        anonymized_metrics=anonymized_metrics,
        lessons=lessons,
        general_insight=general_insight,
        client_name_disclosed=False,
        consent_to_publish=False,
    )

"""Upsell Logic — the Proof Pack writes the upsell."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UpsellRecommendation:
    upsell_offer: str
    reason: str


_UPSELL_MAP: tuple[tuple[str, str], ...] = (
    ("data_issues", "Data Readiness Retainer"),
    ("follow_up_gaps", "Monthly RevOps OS"),
    ("knowledge_gaps", "Company Brain"),
    ("policy_risks", "Monthly Governance"),
    ("manual_reporting", "Executive Reporting Automation"),
)


def recommend_upsell(proof_signals: frozenset[str]) -> tuple[UpsellRecommendation, ...]:
    """Return upsell recommendations triggered by detected signals in the Proof Pack."""

    recommendations: list[UpsellRecommendation] = []
    for signal, offer in _UPSELL_MAP:
        if signal in proof_signals:
            recommendations.append(
                UpsellRecommendation(
                    upsell_offer=offer,
                    reason=f"proof_signal_{signal}",
                )
            )
    return tuple(recommendations)

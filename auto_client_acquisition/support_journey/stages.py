"""7-stage journey taxonomy."""
from __future__ import annotations

from typing import Literal

JourneyStage = Literal[
    "pre_sales",
    "onboarding",
    "delivery",
    "billing",
    "proof",
    "renewal",
    "privacy",
]

JOURNEY_STAGES: tuple[str, ...] = (
    "pre_sales",
    "onboarding",
    "delivery",
    "billing",
    "proof",
    "renewal",
    "privacy",
)

# SLA in hours per stage (founder approval-required gates apply on top)
STAGE_SLA_HOURS: dict[str, int] = {
    "pre_sales": 4,    # fast — sales velocity matters
    "onboarding": 8,   # same business day
    "delivery": 24,    # within 24h
    "billing": 1,      # urgent — financial
    "proof": 48,       # 2 days OK
    "renewal": 24,     # within 24h
    "privacy": 1,      # urgent — PDPL
}


def is_known_stage(stage: str) -> bool:
    return stage in JOURNEY_STAGES

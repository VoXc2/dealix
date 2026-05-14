"""Proof economy — kinds and retainer mapping."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

RecommendTag = Literal["continue", "expand", "pause"]


class ProofKind(StrEnum):
    REVENUE = "revenue"
    TIME = "time"
    QUALITY = "quality"
    RISK = "risk"
    KNOWLEDGE = "knowledge"


PROOF_KIND_TO_RECURRING: dict[ProofKind, str] = {
    ProofKind.REVENUE: "Monthly RevOps OS",
    ProofKind.KNOWLEDGE: "Monthly Company Brain",
    ProofKind.RISK: "Monthly Governance",
    ProofKind.TIME: "Monthly AI Ops",
    ProofKind.QUALITY: "Monthly AI Ops",
}

PROOF_PACK_SECTIONS: tuple[str, ...] = (
    "problem",
    "inputs",
    "work_completed",
    "metrics",
    "before_after",
    "ai_outputs",
    "governance_events",
    "business_value",
    "risks",
    "recommended_next_step",
)


def recurring_offer_for_proof(kind: ProofKind) -> str:
    return PROOF_KIND_TO_RECURRING[kind]


def proof_to_retainer_hint(proof_strength: str) -> RecommendTag:
    key = proof_strength.strip().lower()
    if key in {"strong", "high"}:
        return "expand"
    if key in {"medium", "moderate"}:
        return "continue"
    return "pause"

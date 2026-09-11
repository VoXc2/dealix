"""Realistic Money-Now — real relationships, real problems, realistic time-to-cash, no hype."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.relationship_graph import RelationshipGraph, RelationshipRecord, RelationshipStage
from dealix.commercial.financial_os import FinancialOS, FinancialRecord, FinancialState
from dealix.commercial.probability_engine import ProbBand

UNKNOWN = "UNKNOWN"

class RealisticMoneyNowCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str
    relationship_id: str
    entity: str
    buyer: str
    problem: str
    buyer_evidence: str = UNKNOWN
    problem_evidence: str = UNKNOWN
    expected_gross_profit_sar: str = UNKNOWN  # range, not precise
    time_to_cash_days: str = UNKNOWN  # range
    probability: ProbBand = ProbBand.MEDIUM
    next_action: str = UNKNOWN
    owner: str = "dealix-sales"
    founder_minutes: int = 15
    kill_condition: str = UNKNOWN
    is_real: bool = False

class RealisticMoneyNowEngine:
    def rank(self, graph: RelationshipGraph, financial: FinancialOS) -> list[RealisticMoneyNowCandidate]:
        # Realistic: only WARM relationships with real interaction, not RESEARCH
        candidates: list[RealisticMoneyNowCandidate] = []
        for rec in graph.records.values():
            if rec.commercial_stage not in (RelationshipStage.CONVERSATION, RelationshipStage.QUALIFIED, RelationshipStage.DIAGNOSTIC):
                continue
            if rec.trust_score < 3:
                continue
            if not rec.evidence_refs:
                continue
            # Realistic value: small, verifiable, not hype
            candidates.append(RealisticMoneyNowCandidate(
                candidate_id=f"real_{rec.record_id}",
                relationship_id=rec.record_id,
                entity=rec.entity_name,
                buyer=rec.role,
                problem=rec.open_loop,
                buyer_evidence=rec.evidence_refs[0] if rec.evidence_refs else UNKNOWN,
                problem_evidence=rec.evidence_refs[0] if rec.evidence_refs else UNKNOWN,
                expected_gross_profit_sar="5,000–15,000 SAR (estimate, requires scope)",
                time_to_cash_days="14–30 days (if discovery→quote→pilot)",
                probability=ProbBand.MEDIUM,
                next_action=f"Prepare discovery draft for {rec.entity_name} — evidence: {rec.evidence_refs[0] if rec.evidence_refs else UNKNOWN}",
                founder_minutes=15,
                kill_condition="No reply after 2 follow-ups with value-add → PAUSE",
                is_real=True,
            ))
        # Realistic: if no real relationships, return empty with honest UNKNOWN, not fake
        if not candidates:
            return []
        return sorted(candidates, key=lambda c: c.probability.value, reverse=True)[:3]

    def to_dict(self, candidates: list[RealisticMoneyNowCandidate]) -> dict[str, Any]:
        return {"candidates": [c.model_dump(mode="json") for c in candidates], "count": len(candidates), "realistic": True}

__all__ = ["RealisticMoneyNowEngine", "RealisticMoneyNowCandidate", "UNKNOWN"]

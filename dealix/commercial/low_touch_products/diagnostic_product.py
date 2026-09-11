"""Low-Touch Diagnostic Product — self-serve, automated delivery, low marginal cost."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth
from dealix.commercial.diagnostic_self_serve import DiagnosticInput, SelfServeDiagnostic

UNKNOWN = "UNKNOWN"

class DiagnosticProductRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    locale: str = "ar"
    sector: str = UNKNOWN
    company_size: str = "sme"
    buyer_role: str = "ceo"
    workflow: str = UNKNOWN
    problem: str = UNKNOWN
    email: str = UNKNOWN
    consent: bool = False

class DiagnosticProductResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    sector: str
    diagnostic_families: list[str]
    bottleneck_map: list[str]
    automation_candidates: list[str]
    expected_impact_range: str
    next_step: str
    price_sar: int = 0
    delivery: str = "automated_pdf"
    proof_ref: str = ""

class DiagnosticProductEngine:
    def __init__(self) -> None:
        self.factory = UniversalDiagnosticFactory()
        self.diagnostic = SelfServeDiagnostic()

    def price(self, sector: str, depth: DiagnosticDepth) -> int:
        # Low-touch: free mini diagnostic for lead, paid deep diagnostic
        if depth == DiagnosticDepth.D0_SIGNAL_SCAN:
            return 0
        if depth == DiagnosticDepth.D1_RAPID:
            return 0  # free mini
        return 2500  # D2+ paid

    def run(self, req: DiagnosticProductRequest) -> DiagnosticProductResult:
        families = self.factory.compose(req.sector, req.company_size, req.buyer_role, req.problem, DiagnosticDepth.D1_RAPID)
        # Use self-serve diagnostic for quick wins
        inp = DiagnosticInput(
            diagnostic_id=req.request_id,
            locale=req.locale,
            sector=req.sector,
            company_size=req.company_size,
            buyer_role=req.buyer_role,
            workflow=req.workflow,
            problem=req.problem,
            manual_steps=6,
            delay_days=7,
            cost_hypothesis_sar=30000,
            consent=req.consent,
        )
        out = self.diagnostic.assess(inp)
        price = self.price(req.sector, DiagnosticDepth.D1_RAPID)
        return DiagnosticProductResult(
            request_id=req.request_id,
            sector=req.sector,
            diagnostic_families=[f.family_id for f in families[:3]],
            bottleneck_map=out.bottleneck_map,
            automation_candidates=out.automation_candidates,
            expected_impact_range=out.expected_impact_range,
            next_step=out.recommended_next_step,
            price_sar=price,
            proof_ref=f"diag_{hashlib.sha256(req.request_id.encode()).hexdigest()[:8]}",
        )

    def to_dict(self, result: DiagnosticProductResult) -> dict[str, Any]:
        return result.model_dump(mode="json")

__all__ = ["DiagnosticProductEngine", "DiagnosticProductRequest", "DiagnosticProductResult"]

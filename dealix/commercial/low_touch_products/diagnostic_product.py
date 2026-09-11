"""Low-Touch Diagnostic Product — self-serve, automated delivery, low marginal cost."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.diagnostic_self_serve import DiagnosticInput, SelfServeDiagnostic
from dealix.commercial.universal_diagnostic_factory import (
    FAMILY_AR,
    FREE_DEPTHS,
    DiagnosticDepth,
    UniversalDiagnosticFactory,
)

UNKNOWN = "UNKNOWN"

QUOTE_REQUIRED = "quote_required_after_qualified_discovery"

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
    depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID

class DiagnosticProductResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    sector: str
    depth: str = DiagnosticDepth.D1_RAPID.value
    diagnostic_families: list[str]
    problem_map: list[dict[str, Any]] = Field(default_factory=list)
    maturity_score: dict[str, Any] = Field(default_factory=dict)
    bottleneck_map: list[str]
    automation_candidates: list[str]
    evidence_gaps: list[str] = Field(default_factory=list)
    risk_opportunity_map: list[dict[str, Any]] = Field(default_factory=list)
    priority_actions: list[str] = Field(default_factory=list)
    safe_recommendations: list[str] = Field(default_factory=list)
    next_step: str
    next_step_cta: str = UNKNOWN
    qualified_discovery_path: str = UNKNOWN
    expected_impact_range: str
    opportunity_event: dict[str, Any] = Field(default_factory=dict)
    proof_receipt: dict[str, Any] = Field(default_factory=dict)
    price_sar: int = 0
    pricing_basis: str = "free_d0_d2"
    delivery: str = "automated_pdf"
    proof_ref: str = ""

class DiagnosticProductEngine:
    def __init__(self) -> None:
        self.factory = UniversalDiagnosticFactory()
        self.diagnostic = SelfServeDiagnostic()

    def price(self, sector: str, depth: DiagnosticDepth) -> int:
        # Founder policy: D0-D2 genuinely free (no card, no fake urgency).
        # Deeper depths are never priced here; they need a customer-specific
        # quote after qualified discovery.
        return 0

    def pricing_basis(self, depth: DiagnosticDepth) -> str:
        return "free_d0_d2" if depth in FREE_DEPTHS else QUOTE_REQUIRED

    def evidence_gaps(self, req: DiagnosticProductRequest, out: Any) -> list[str]:
        gaps: list[str] = []
        for field_name in ("workflow", "problem", "frequency", "current_tools", "risk", "desired_state"):
            if getattr(req, field_name, UNKNOWN) == UNKNOWN:
                gaps.append(f"missing::{field_name}")
        gaps.append("evidence::system_export")
        gaps.append("evidence::interview")
        if not req.consent:
            gaps.append("consent::not_granted")
        return gaps

    def maturity_score(self, req: DiagnosticProductRequest, gaps: list[str]) -> dict[str, Any]:
        dimensions = 8
        missing_inputs = sum(1 for gap in gaps if gap.startswith("missing::"))
        score = max(0, round((dimensions - missing_inputs) / dimensions * 100))
        return {
            "score": score,
            "scale": "0-100",
            "truth_class": "ESTIMATED",
            "is_measured_fact": False,
            "basis": "input_completeness_only",
            "label_ar": "تقدير — ليس قياسًا مؤكدًا",
            "label_en": "ESTIMATED — not a measured fact",
        }

    def problem_map(self, families: list[Any]) -> list[dict[str, Any]]:
        return [
            {
                "family_id": family.family_id,
                "area_ar": FAMILY_AR.get(family.family_id, family.name),
                "area_en": family.name,
                "depth": family.depth.value,
                "truth_class": "PATTERN",
            }
            for family in families[:6]
        ]

    def risk_opportunity_map(self, out: Any) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for risk in out.risk_notes:
            items.append({"kind": "RISK", "item": risk, "truth_class": "PATTERN"})
        for opportunity in list(out.quick_wins) + list(out.automation_candidates):
            items.append({"kind": "OPPORTUNITY", "item": opportunity, "truth_class": "PATTERN"})
        return items

    def opportunity_event(self, req: DiagnosticProductRequest) -> dict[str, Any]:
        return {
            "event_type": "diagnostic_completed",
            "event_id": f"diag_evt_{hashlib.sha256(req.request_id.encode()).hexdigest()[:12]}",
            "sector": req.sector,
            "buyer_role": req.buyer_role,
            "problem": req.problem,
            "truth_class": "INTERNAL_SIGNAL",
            "counts_as_pipeline": False,
            "requires_human_review": True,
        }

    def proof_receipt(self, req: DiagnosticProductRequest, depth: DiagnosticDepth, pricing_basis: str) -> dict[str, Any]:
        return {
            "receipt_id": f"diag_{hashlib.sha256(req.request_id.encode()).hexdigest()[:8]}",
            "engine": "UniversalDiagnosticFactory",
            "depth": depth.value,
            "price_sar": 0,
            "pricing_basis": pricing_basis,
            "truth_class": "PATTERN",
            "is_customer_fact": False,
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def run(self, req: DiagnosticProductRequest) -> DiagnosticProductResult:
        depth = req.depth
        families = self.factory.compose(req.sector, req.company_size, req.buyer_role, req.problem, depth)
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
        price = self.price(req.sector, depth)
        basis = self.pricing_basis(depth)
        gaps = self.evidence_gaps(req, out)
        cta_ar = "ابدأ جلسة اكتشاف (15 دقيقة) بعد الموافقة"
        cta_en = "Start a 15-minute discovery session after approval"
        return DiagnosticProductResult(
            request_id=req.request_id,
            sector=req.sector,
            depth=depth.value,
            diagnostic_families=[f.family_id for f in families[:3]],
            problem_map=self.problem_map(families),
            maturity_score=self.maturity_score(req, gaps),
            bottleneck_map=out.bottleneck_map,
            automation_candidates=out.automation_candidates,
            evidence_gaps=gaps,
            risk_opportunity_map=self.risk_opportunity_map(out),
            priority_actions=list(out.quick_wins) + ["collect_system_export_evidence"],
            safe_recommendations=list(out.non_ai_candidates)
            + list(out.ai_candidates)
            + ["no_automation_without_human_approval_gate"],
            next_step=out.recommended_next_step,
            next_step_cta=cta_ar if req.locale == "ar" else cta_en,
            qualified_discovery_path="discovery" if req.consent else "request_consent_then_discovery",
            expected_impact_range=out.expected_impact_range,
            opportunity_event=self.opportunity_event(req),
            proof_receipt=self.proof_receipt(req, depth, basis),
            price_sar=price,
            pricing_basis=basis,
            proof_ref=f"diag_{hashlib.sha256(req.request_id.encode()).hexdigest()[:8]}",
        )

    def to_dict(self, result: DiagnosticProductResult) -> dict[str, Any]:
        return result.model_dump(mode="json")

__all__ = [
    "DiagnosticProductEngine",
    "DiagnosticProductRequest",
    "DiagnosticProductResult",
    "QUOTE_REQUIRED",
]

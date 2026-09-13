"""
Public intake endpoints — unauthenticated and rate-limited.

The legacy custom-AI request remains founder-reviewed. The canonical website
entry point is POST /api/v1/public/execution-diagnostic: it captures a
customer-initiated Free Execution Diagnostic, creates an internal handoff for
the canonical Omega V3 Agentic Holding, and mirrors the intake into the ONE
Revenue Ops Autopilot store. Historical executor aliases are compatibility
metadata only and never fleet-size or architecture authority.

No customer message, publication, payment, binding quote, production mutation,
or marketing consent is created by either endpoint.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Literal, TypeVar
from uuid import uuid4

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from api.security.rate_limit import LIMITS, limiter
from auto_client_acquisition.diagnostic_intake_orchestrator import (
    build_agent_handoff,
    mirror_to_revenue_autopilot,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/public", tags=["public-intake"])

VAR_DIR = Path("var")
_F = TypeVar("_F", bound=Callable)


def _public_intake_limit(func: _F) -> _F:
    """Use the canonical lead-creation throttle; no silent custom limiter."""
    if limiter is None:
        return func
    return limiter.limit(LIMITS["leads_create"])(func)


class CustomAIRequest(BaseModel):
    sector: Literal[
        "real_estate", "retail", "logistics", "professional_services", "other"
    ] = Field(..., description="Industry sector")
    use_case: str = Field(..., min_length=10, max_length=2000)
    data_volume: Literal["<1K rows", "1K-100K", "100K+"] = Field(...)
    data_sensitivity: Literal["public", "internal", "confidential"] = Field(...)
    timeline: Literal["<1 month", "1-3 months", "3+ months"] = Field(...)
    budget_band: Literal["5K-10K", "10K-25K", "25K+"] = Field(...)


class ExecutionDiagnosticIntake(BaseModel):
    """Customer-initiated intake for the Free Execution Diagnostic."""

    name: str = Field(..., min_length=2, max_length=160)
    email: str = Field(..., min_length=5, max_length=320)
    phone: str = Field(default="", max_length=64)
    company: str = Field(..., min_length=2, max_length=220)
    role: str = Field(default="", max_length=160)
    sector: str = Field(default="other", min_length=2, max_length=120)
    website: str = Field(default="", max_length=400)

    workflow: str = Field(..., min_length=10, max_length=2400)
    decision_owner: str = Field(default="", max_length=1000)
    tools_data: str = Field(default="", max_length=1800)
    business_impact: str = Field(default="", max_length=1800)
    proof_metric: str = Field(default="", max_length=1000)
    baseline: str = Field(default="", max_length=1000)
    target_outcome: str = Field(default="", max_length=1200)
    urgency: str = Field(default="", max_length=500)

    preferred_contact: Literal["email", "phone", "whatsapp", "either"] = "email"
    # Purpose-specific service follow-up must be explicit. This is not
    # durable/direct-marketing consent and is never promoted to such.
    followup_requested: bool = False
    language_preference: Literal["ar", "en", "ar_en"] = "ar_en"


@router.post("/custom-ai-request")
@_public_intake_limit
def submit_custom_ai_request(request: Request, payload: CustomAIRequest) -> dict:
    """Accept the legacy Rung-4 Custom AI intake for founder review."""
    del request  # required by the canonical slowapi decorator
    VAR_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "submitted_at": datetime.now(UTC).isoformat(),
        "sector": payload.sector,
        "use_case": payload.use_case,
        "data_volume": payload.data_volume,
        "data_sensitivity": payload.data_sensitivity,
        "timeline": payload.timeline,
        "budget_band": payload.budget_band,
        "governance_decision": "queued_for_founder_review",
        "status": "pending_founder_approval",
        "disclaimer": "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة",
    }

    intake_file = VAR_DIR / "custom_ai_requests.jsonl"
    with intake_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    logger.info(
        "custom_ai_request queued sector=%s timeline=%s budget=%s",
        payload.sector,
        payload.timeline,
        payload.budget_band,
    )

    return {
        "status": "queued",
        "governance_decision": "queued_for_founder_review",
        "message": (
            "شكراً — تم استلام طلبك وسيُراجعه المؤسس قبل أي إجراء. "
            "Thank you — your request has been received and will be reviewed by the founder before any action."
        ),
    }


@router.post("/execution-diagnostic")
@_public_intake_limit
def submit_execution_diagnostic(request: Request, payload: ExecutionDiagnosticIntake) -> dict:
    """Start the internal evidence-first diagnostic workflow for an inbound lead.

    This endpoint performs only internal, reversible work: capture, evidence-gap
    analysis and canonical Agentic Holding handoff. It deliberately does not
    auto-send a reply, declare a qualified problem, create an opportunity, issue
    a quote, charge, publish, or mutate production infrastructure.
    """
    del request  # required by the canonical slowapi decorator
    intake_id = f"webdiag_{uuid4().hex[:16]}"
    submitted_at = datetime.now(UTC).isoformat()
    diagnostic_context = {
        "role": payload.role.strip(),
        "website": payload.website.strip(),
        "workflow": payload.workflow.strip(),
        "decision_owner": payload.decision_owner.strip(),
        "tools_data": payload.tools_data.strip(),
        "business_impact": payload.business_impact.strip(),
        "proof_metric": payload.proof_metric.strip(),
        "baseline": payload.baseline.strip(),
        "target_outcome": payload.target_outcome.strip(),
        "urgency": payload.urgency.strip(),
        "preferred_contact": payload.preferred_contact,
        "followup_requested": str(bool(payload.followup_requested)).lower(),
        "language_preference": payload.language_preference,
    }
    record = {
        "id": intake_id,
        "submitted_at": submitted_at,
        "source": "dealix_website_execution_diagnostic",
        "name": payload.name.strip(),
        "email": payload.email.strip(),
        "phone": payload.phone.strip(),
        "company": payload.company.strip(),
        "role": payload.role.strip(),
        "sector": payload.sector.strip(),
        "diagnostic_context": diagnostic_context,
        # Keep these distinct. A customer asking for a response to this request
        # does not silently become a durable direct-marketing opt-in.
        "followup_requested": bool(payload.followup_requested),
        "marketing_consent": False,
        "customer_proof_consent": False,
    }

    handoff = build_agent_handoff(record)
    mirror = mirror_to_revenue_autopilot(record, handoff)

    logger.info(
        "execution_diagnostic_received intake=%s company=%s completeness=%s",
        intake_id,
        payload.company.strip(),
        handoff.get("evidence_completeness_pct"),
    )

    holding = handoff.get("agentic_holding") or {}
    return {
        "status": "received",
        "intake_id": intake_id,
        "workflow_state": "AGENT_INTAKE_STARTED_INTERNAL_ONLY",
        "problem_state": handoff.get("problem_state"),
        "evidence_completeness_pct": handoff.get("evidence_completeness_pct"),
        "next_questions": handoff.get("next_questions"),
        "agent_handoff": {
            "architecture": holding.get("architecture"),
            "logical_agents": holding.get("logical_agents"),
            "sector_companies": holding.get("sector_companies"),
            "arm_pods": holding.get("arm_pods"),
            "fixed_five_authority": False,
            "routing_authority": handoff.get("routing_authority"),
            "work_packets_created": len(handoff.get("work_packets") or []),
        },
        "revenue_ops": mirror,
        "truth": handoff.get("truth"),
        "external_action": "none",
        "message": (
            "تم استلام التشخيص وبدأت المعالجة الداخلية القائمة على الأدلة. "
            "Received — Dealix has created the internal evidence-first diagnostic work packet."
        ),
    }
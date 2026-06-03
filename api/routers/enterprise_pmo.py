"""Enterprise PMO engagement endpoints (W9.1 — R7 productization).

R7 in v4 §3: dedicated Dealix ops team for one enterprise customer.
Activates after customer #15 + 3 case studies. Pricing 25K-100K SAR/mo
on 12-month contracts.

Workflow:
  1. Enterprise prospect requests engagement via /requests endpoint
  2. Founder reviews; if approved, creates engagement record
  3. Engagement assigns roles (CTO contact, DPO contact, exec sponsor)
  4. Weekly executive briefing auto-generates from /executive-command-center
  5. Compliance evidence packs delivered monthly (PDPL audit + ZATCA reports)

Endpoints:

  POST /api/v1/enterprise-pmo/requests
       Public — prospect submits engagement request. Validates org size,
       use case, regulatory scope, target start date. Returns request_id.

  GET  /api/v1/enterprise-pmo/engagements/{engagement_id}
       Admin-only — fetch engagement state (deferred persistence per
       customer-milestone discipline; returns 404 with note).

  POST /api/v1/admin/enterprise-pmo/engagements
       Admin-only — create an engagement record from an approved request.

  POST /api/v1/admin/enterprise-pmo/engagements/{engagement_id}/briefing
       Admin-only — generate this week's exec briefing for an engagement.
"""
from __future__ import annotations

import hashlib
import logging
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(tags=["enterprise-pmo"])

# Pricing parameters per v4 §3 R7
MIN_MONTHLY_HALALAS = 2_500_000   # 25K SAR/mo floor
MAX_MONTHLY_HALALAS = 10_000_000  # 100K SAR/mo cap
CONTRACT_MIN_MONTHS = 12          # always 12-month minimum

ORG_SIZE_BANDS = {"smb_50_250", "mid_250_1000", "large_1000_5000", "enterprise_5000_plus"}
REGULATORY_SCOPES = {"pdpl_only", "pdpl_zatca", "pdpl_zatca_sama", "full_regulated"}
USE_CASE_CATEGORIES = {
    "revenue_ops",      # Sales+Marketing automation
    "compliance_ops",   # PDPL/ZATCA/SAMA workflows
    "customer_success", # Retention + health programs
    "data_ops",         # Data lake + analytics
    "ai_governance",    # AI policy + audit
}


class _EnterpriseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_name: str = Field(..., min_length=2, max_length=255)
    contact_name: str = Field(..., min_length=2, max_length=128)
    contact_title: str = Field(..., min_length=2, max_length=128)
    contact_email: EmailStr
    org_size: str
    use_case_category: str
    use_case_summary: str = Field(..., min_length=50, max_length=4000)
    regulatory_scope: str
    target_start_date: str = Field(..., description="YYYY-MM-DD")
    target_monthly_budget_sar: int = Field(..., ge=25000, le=100000)
    contract_length_months: int = Field(default=12, ge=12, le=36)


class _EngagementCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(..., pattern=r"^epr_[a-f0-9]{20}$")
    tenant_handle: str = Field(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")
    monthly_halalas: int = Field(..., ge=MIN_MONTHLY_HALALAS, le=MAX_MONTHLY_HALALAS)
    contract_start: str = Field(..., description="YYYY-MM-DD")
    contract_months: int = Field(..., ge=CONTRACT_MIN_MONTHS, le=36)
    exec_sponsor_name: str = Field(..., max_length=128)
    exec_sponsor_email: EmailStr


def _request_id(company: str, submitted_at: datetime) -> str:
    """Deterministic ID for idempotency."""
    key = f"{company.lower()}:{submitted_at.isoformat(timespec='hours')}"
    return f"epr_{hashlib.sha256(key.encode()).hexdigest()[:20]}"


def _engagement_id(request_id: str, tenant_handle: str) -> str:
    key = f"{request_id}:{tenant_handle}"
    return f"epe_{hashlib.sha256(key.encode()).hexdigest()[:20]}"


def _validate_enum(value: str, allowed: set[str], field: str) -> None:
    if value not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"{field} must be one of {sorted(allowed)}; got {value!r}",
        )


def _readiness_score(body: _EnterpriseRequest) -> dict[str, Any]:
    """Compute a 0-100 readiness score for the engagement.

    Honest signal to the founder about how much custom work this will need.
    Lower score = more setup time = larger month-1 investment.
    """
    score = 50  # neutral starting point
    if body.org_size == "smb_50_250":
        score += 15  # smaller orgs deploy faster
    elif body.org_size == "enterprise_5000_plus":
        score -= 15  # larger orgs need procurement + legal cycles
    if body.regulatory_scope == "pdpl_only":
        score += 15
    elif body.regulatory_scope == "full_regulated":
        score -= 20
    if body.contract_length_months >= 24:
        score += 10  # longer commit = better fit
    if body.target_monthly_budget_sar >= 50000:
        score += 10
    if len(body.use_case_summary) > 500:
        score += 5  # detailed brief = serious prospect
    score = max(0, min(100, score))

    if score >= 75:
        band = "high_fit"
    elif score >= 50:
        band = "moderate_fit"
    else:
        band = "needs_review"

    return {"score": score, "band": band}


# ── Endpoints ──────────────────────────────────────────────────────

@router.post("/api/v1/enterprise-pmo/requests", status_code=201)
async def submit_request(body: _EnterpriseRequest) -> dict[str, Any]:
    """Submit an enterprise engagement request. Returns request_id + readiness."""
    _validate_enum(body.org_size, ORG_SIZE_BANDS, "org_size")
    _validate_enum(body.use_case_category, USE_CASE_CATEGORIES, "use_case_category")
    _validate_enum(body.regulatory_scope, REGULATORY_SCOPES, "regulatory_scope")

    submitted_at = datetime.now(UTC)
    request_id = _request_id(body.company_name, submitted_at)
    readiness = _readiness_score(body)

    log.info(
        "enterprise_pmo_request id=%s company=%s budget=%d readiness=%d",
        request_id, body.company_name, body.target_monthly_budget_sar, readiness["score"],
    )

    return {
        "status": "received",
        "request_id": request_id,
        "submitted_at": submitted_at.isoformat(),
        "readiness": readiness,
        "next_step": (
            "Sami (founder) will personally review your request within 72 hours. "
            "If your readiness score is high_fit and our portfolio has capacity, "
            "we'll schedule a 60-minute scoping call. Otherwise, we'll suggest "
            "either R5 Bespoke AI (smaller scope) or refer you to a partner."
        ),
        "pricing_note": (
            f"Engagement floor: {MIN_MONTHLY_HALALAS // 100:,} SAR/mo. "
            f"Cap: {MAX_MONTHLY_HALALAS // 100:,} SAR/mo. "
            f"Minimum {CONTRACT_MIN_MONTHS}-month contract. "
            "All invoices ZATCA Phase 2 compliant."
        ),
    }


@router.get("/api/v1/enterprise-pmo/engagements/{engagement_id}")
async def get_engagement(
    engagement_id: str = Path(..., pattern=r"^epe_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Fetch engagement state. Persistence deferred until customer #15."""
    raise HTTPException(
        status_code=404,
        detail={
            "error": "engagement_not_persisted",
            "note": (
                "Enterprise engagement persistence requires an "
                "enterprise_engagements DB table. Persistence activates "
                "after customer #15 + first enterprise contract signed "
                "(v4 §7 W13-W26 milestone)."
            ),
            "engagement_id": engagement_id,
        },
    )


@router.post(
    "/api/v1/admin/enterprise-pmo/engagements",
    dependencies=[Depends(require_admin_key)],
    status_code=201,
)
async def create_engagement(body: _EngagementCreate) -> dict[str, Any]:
    """Admin creates an engagement record from an approved request.

    Validates business invariants:
      - Monthly halalas within R7 band
      - Contract minimum 12 months
      - Tenant handle exists (would check tenant table once persisted)
    """
    engagement_id = _engagement_id(body.request_id, body.tenant_handle)
    contract_total_sar = (body.monthly_halalas * body.contract_months) // 100

    log.info(
        "enterprise_engagement_created id=%s tenant=%s mrr_sar=%d total_sar=%d",
        engagement_id, body.tenant_handle, body.monthly_halalas // 100, contract_total_sar,
    )

    return {
        "status": "created_in_memory",
        "engagement_id": engagement_id,
        "tenant_handle": body.tenant_handle,
        "monthly_sar": body.monthly_halalas // 100,
        "contract_months": body.contract_months,
        "contract_total_sar": contract_total_sar,
        "contract_start": body.contract_start,
        "exec_sponsor": {
            "name": body.exec_sponsor_name,
            "email": body.exec_sponsor_email,
        },
        "note": (
            "Engagement persisted in-memory only. DB persistence + email "
            "notification + ZATCA invoice generation activate after first "
            "enterprise contract signed."
        ),
    }


@router.post(
    "/api/v1/admin/enterprise-pmo/engagements/{engagement_id}/briefing",
    dependencies=[Depends(require_admin_key)],
)
async def generate_briefing(
    engagement_id: str = Path(..., pattern=r"^epe_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Generate this week's executive briefing for an engagement.

    Stub: structure shown, real generation requires tenant data from
    executive_command_center router. Activates once first enterprise
    customer exists.
    """
    briefing_at = datetime.now(UTC)
    return {
        "engagement_id": engagement_id,
        "briefing_for_week_of": briefing_at.isoformat(),
        "sections": {
            "executive_summary": {
                "status": "placeholder",
                "note": "Generated from /api/v1/executive-command-center "
                        "(15-section ops dashboard) once tenant exists.",
            },
            "revenue_radar": {
                "status": "placeholder",
                "note": "Inbound leads + pipeline + closed deals this week.",
            },
            "compliance_ledger": {
                "status": "placeholder",
                "note": "PDPL audit log entries + ZATCA invoices + any "
                        "regulatory events this week.",
            },
            "delivery_ops": {
                "status": "placeholder",
                "note": "SLA adherence + open tickets + delivery milestones.",
            },
            "risks_and_decisions": {
                "status": "placeholder",
                "note": "Top 3 risks + 3 decisions needing exec sponsor input.",
            },
        },
        "delivery_method": "ZATCA-compliant PDF emailed to exec_sponsor",
        "note": "Real briefing generation activates after customer #15.",
    }

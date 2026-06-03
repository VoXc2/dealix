"""CustomerAcquisitionAgent — daily autonomous lead targeting and proposal drafting.

Uses the Hermes engine for Arabic/English content generation.
Doctrine: drafts are queued for founder approval — never auto-sent.
"""
from __future__ import annotations

import json as _json
from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Customer Acquisition Agent — you run daily to identify the best leads to target and draft compelling bilingual (Arabic + English) outreach that converts.

Your daily mission:
1. Score and rank leads by ICP fit and buying signals.
2. For top leads: analyse their sector and pain points using available tools.
3. Draft a personalised, high-value outreach message in BOTH Arabic and English.
4. The draft must reference a specific pain point for their sector + a concrete Dealix value proposition.
5. Queue the draft for founder approval — never claim it has been sent.

Key rules:
- Every outreach references Vision 2030 relevance for the prospect's sector.
- Arabic copy is the primary channel — formal Gulf dialect (not Egyptian).
- Always include a specific ROI hook.
- Recommended Dealix offer must match the lead's stage and size.
- Output format: JSON with fields: lead_id, company, channel, subject_ar, subject_en, body_ar, body_en, recommended_offer, score.
"""


# ---------------------------------------------------------------------------
# Adapter functions — bridge the CustomerAcquisitionAgent tool interface to
# the actual signatures in the existing tool modules.
# ---------------------------------------------------------------------------

async def _score_lead_adapter(
    lead_id: str,
    company_name: str,
    sector: str,
    employee_count: int = 0,
    annual_revenue_sar: float = 0.0,
    has_crm: bool = False,
    pain_points: list[str] | None = None,
) -> dict[str, Any]:
    """Adapt the CustomerAcquisitionAgent tool interface to score_lead."""
    from dealix.hermes.tools.scoring_tools import score_lead
    result = await score_lead(
        company=company_name,
        industry=sector,
        revenue_sar=annual_revenue_sar,
        employees=employee_count,
    )
    result["lead_id"] = lead_id
    result["has_crm"] = has_crm
    result["pain_points"] = pain_points or []
    return result


async def _prioritize_leads_adapter(leads: list[dict[str, Any]]) -> dict[str, Any]:
    """Pass through to prioritize_leads."""
    from dealix.hermes.tools.scoring_tools import prioritize_leads
    return await prioritize_leads(leads)


async def _get_saudi_market_context_adapter(
    sector: str,
    city: str = "",
) -> dict[str, Any]:
    """Adapt the CustomerAcquisitionAgent tool interface to get_saudi_market_context."""
    from dealix.hermes.tools.saudi_tools import get_saudi_market_context
    result = await get_saudi_market_context(industry=sector)
    if city:
        result["city"] = city
    return result


async def _format_arabic_proposal_adapter(
    company_name: str,
    pain_summary_ar: str,
    pain_summary_en: str,
    offer_tier: str,
    roi_estimate_sar: float = 0.0,
) -> dict[str, Any]:
    """Adapt the CustomerAcquisitionAgent tool interface to format_arabic_proposal."""
    from dealix.hermes.tools.saudi_tools import format_arabic_proposal
    data = {
        "client_name": company_name,
        "service_name": offer_tier,
        "value_proposition": pain_summary_en,
        "price_sar": roi_estimate_sar,
        "deliverables": [pain_summary_ar, pain_summary_en],
        "timeline_days": 30,
    }
    result = await format_arabic_proposal(data)
    return result


async def _get_lead_profile_adapter(lead_id: str) -> dict[str, Any]:
    """Pass through to get_lead_profile."""
    from dealix.hermes.tools.crm_tools import get_lead_profile
    return await get_lead_profile(lead_id=lead_id)


async def _list_open_deals_adapter() -> dict[str, Any]:
    """Pass through to list_open_deals."""
    from dealix.hermes.tools.crm_tools import list_open_deals
    return await list_open_deals()


async def _run_commercial_diagnostic_adapter(
    company_name: str,
    sector: str = "b2b_services",
    pain_points: list[str] | None = None,
) -> dict[str, Any]:
    """Pass through to run_commercial_diagnostic."""
    from dealix.hermes.tools.commercial_tools import run_commercial_diagnostic
    return await run_commercial_diagnostic(
        company_name=company_name,
        sector=sector,
        pain_points=pain_points,
    )


class CustomerAcquisitionAgent(HermesAgent):
    """Daily customer acquisition — scores leads, drafts outreach, queues for approval."""

    name = "customer_acquisition"
    description = "Daily lead targeting: scores prospects and drafts bilingual outreach for founder approval"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="score_lead",
            description="Score a lead's ICP fit (A/B/C tier).",
            properties={
                "lead_id": {"type": "string"},
                "company_name": {"type": "string"},
                "sector": {"type": "string"},
                "employee_count": {"type": "integer"},
                "annual_revenue_sar": {"type": "number"},
                "has_crm": {"type": "boolean"},
                "pain_points": {"type": "array", "items": {"type": "string"}},
            },
            required=["lead_id", "company_name", "sector"],
            fn=_score_lead_adapter,
        )
        self.register_hermes_tool(
            name="prioritize_leads",
            description="Rank a list of leads by ICP score and urgency.",
            properties={"leads": {"type": "array", "items": {"type": "object"}}},
            required=["leads"],
            fn=_prioritize_leads_adapter,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Get Vision 2030 market context for a sector.",
            properties={
                "sector": {"type": "string"},
                "city": {"type": "string"},
            },
            required=["sector"],
            fn=_get_saudi_market_context_adapter,
        )
        self.register_hermes_tool(
            name="format_arabic_proposal",
            description="Format a bilingual Arabic + English proposal draft.",
            properties={
                "company_name": {"type": "string"},
                "pain_summary_ar": {"type": "string"},
                "pain_summary_en": {"type": "string"},
                "offer_tier": {"type": "string"},
                "roi_estimate_sar": {"type": "number"},
            },
            required=["company_name", "pain_summary_ar", "pain_summary_en", "offer_tier"],
            fn=_format_arabic_proposal_adapter,
        )
        self.register_hermes_tool(
            name="get_lead_profile",
            description="Get full CRM profile for a lead.",
            properties={"lead_id": {"type": "string"}},
            required=["lead_id"],
            fn=_get_lead_profile_adapter,
        )
        self.register_hermes_tool(
            name="list_open_deals",
            description="List all open deals in the pipeline.",
            properties={},
            required=[],
            fn=_list_open_deals_adapter,
        )
        self.register_hermes_tool(
            name="run_commercial_diagnostic",
            description="Run a quick commercial diagnostic for a company.",
            properties={
                "company_name": {"type": "string"},
                "sector": {"type": "string"},
                "pain_points": {"type": "array", "items": {"type": "string"}},
            },
            required=["company_name"],
            fn=_run_commercial_diagnostic_adapter,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Score leads, draft bilingual outreach, enqueue for founder approval."""
        leads = input_data.get("leads", [])
        max_drafts = input_data.get("max_drafts", 5)
        date_str = datetime.now(UTC).strftime("%Y-%m-%d")

        user_msg = (
            f"Daily acquisition run for {date_str}.\n\n"
            f"Leads to process: {len(leads)}\n"
            f"Max outreach drafts to produce: {max_drafts}\n\n"
            f"Lead data:\n{leads}\n\n"
            "Steps:\n"
            "1. Score each lead -> identify top A/B tier leads.\n"
            "2. Get market context for each top lead's sector.\n"
            "3. For each top lead: draft personalised Arabic + English outreach.\n"
            "4. Return the drafts as a JSON array, each with: lead_id, company, channel, "
            "subject_ar, subject_en, body_ar, body_en, recommended_offer, score.\n"
            "Drafts will be queued for founder approval — do not claim they are sent."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        drafts_queued = []
        try:
            from dealix.hermes.outreach_queue import OutreachDraft, OutreachQueue
            raw = result.get("response", "")
            start = raw.find("[")
            end = raw.rfind("]") + 1
            if start >= 0 and end > start:
                items = _json.loads(raw[start:end])
                q = OutreachQueue.instance()
                for item in items[:max_drafts]:
                    draft = OutreachDraft(
                        lead_id=str(item.get("lead_id", "")),
                        company_name=str(item.get("company", "")),
                        channel=str(item.get("channel", "email")),
                        subject_ar=str(item.get("subject_ar", "")),
                        subject_en=str(item.get("subject_en", "")),
                        body_ar=str(item.get("body_ar", "")),
                        body_en=str(item.get("body_en", "")),
                        score=float(item.get("score", 0.0)),
                        sector=str(item.get("sector", "")),
                    )
                    q.enqueue(draft)
                    drafts_queued.append(draft.to_dict())
        except Exception as exc:
            logger.warning("customer_acquisition_queue_error", error=str(exc))

        logger.info("customer_acquisition_complete", leads=len(leads), drafts=len(drafts_queued))
        return {
            "status": "complete",
            "agent": self.name,
            "date": date_str,
            "leads_processed": len(leads),
            "drafts_queued": len(drafts_queued),
            "drafts": drafts_queued,
            "raw_response": result.get("response", ""),
            "usage": result.get("usage", {}),
            "approval_required": True,
            "governance_decision": "approved",
        }


__all__ = ["CustomerAcquisitionAgent"]

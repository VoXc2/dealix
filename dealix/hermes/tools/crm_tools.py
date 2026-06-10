"""CRM tool functions — async wrappers that simulate HubSpot calls.

When a real HubSpot integration is wired up, replace the simulated
responses with live API calls without changing the function signatures.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

_VALID_STAGES = (
    "prospect",
    "qualified",
    "proposal",
    "negotiation",
    "closed_won",
    "closed_lost",
    "churned",
)

# In-memory fake store — replaced by a real HubSpot client when available
_LEADS: dict[str, dict[str, Any]] = {}
_DEALS: dict[str, dict[str, Any]] = {}
_ACTIVITIES: list[dict[str, Any]] = []


async def get_lead_profile(lead_id: str) -> dict[str, Any]:
    """Retrieve full lead profile from CRM.

    Parameters
    ----------
    lead_id:
        Unique CRM lead identifier.

    Returns
    -------
    dict
        Lead profile including company, industry, stage, and last activity.
    """
    if lead_id in _LEADS:
        return {"found": True, "lead": _LEADS[lead_id]}

    # Simulate a CRM lookup with mock data
    profile = {
        "lead_id": lead_id,
        "company": f"Company_{lead_id[:6]}",
        "industry": "technology",
        "stage": "prospect",
        "revenue_sar": 1_500_000.0,
        "employees": 25,
        "last_activity_days": 14,
        "nps": 7,
        "created_at": datetime.now(UTC).isoformat(),
        "source": "inbound",
    }
    _LEADS[lead_id] = profile
    logger.info("crm_lead_profile_fetched", lead_id=lead_id)
    return {"found": True, "lead": profile}


async def update_lead_stage(
    lead_id: str,
    stage: str,
    notes: str = "",
) -> dict[str, Any]:
    """Move a lead to a new pipeline stage.

    Parameters
    ----------
    lead_id:
        Unique CRM lead identifier.
    stage:
        Target stage name. Must be one of the valid pipeline stages.
    notes:
        Optional notes explaining the stage change.

    Returns
    -------
    dict
        Confirmation with previous and new stage.
    """
    if stage not in _VALID_STAGES:
        return {
            "updated": False,
            "error": f"invalid_stage: {stage!r}",
            "valid_stages": list(_VALID_STAGES),
        }

    result = await get_lead_profile(lead_id)
    lead = result["lead"]
    previous_stage = lead.get("stage", "unknown")
    lead["stage"] = stage
    lead["stage_notes"] = notes
    lead["stage_updated_at"] = datetime.now(UTC).isoformat()
    _LEADS[lead_id] = lead

    logger.info(
        "crm_lead_stage_updated",
        lead_id=lead_id,
        previous_stage=previous_stage,
        new_stage=stage,
    )
    return {
        "updated": True,
        "lead_id": lead_id,
        "previous_stage": previous_stage,
        "new_stage": stage,
        "notes": notes,
    }


async def create_deal(
    company: str,
    value_sar: float,
    stage: str = "prospect",
) -> dict[str, Any]:
    """Create a new deal record in the CRM.

    Parameters
    ----------
    company:
        Company name for the deal.
    value_sar:
        Estimated deal value in Saudi Riyals.
    stage:
        Initial pipeline stage.

    Returns
    -------
    dict
        New deal record with generated deal_id.
    """
    if stage not in _VALID_STAGES:
        stage = "prospect"

    deal_id = str(uuid.uuid4())[:8]
    deal = {
        "deal_id": deal_id,
        "company": company,
        "value_sar": value_sar,
        "stage": stage,
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat(),
        "probability": 0.1,
    }
    _DEALS[deal_id] = deal
    logger.info("crm_deal_created", deal_id=deal_id, company=company, value_sar=value_sar)
    return {"created": True, "deal": deal}


async def list_open_deals(limit: int = 10) -> dict[str, Any]:
    """Return a list of open (non-closed) deals.

    Parameters
    ----------
    limit:
        Maximum number of deals to return.

    Returns
    -------
    dict
        List of open deals with summary counts.
    """
    closed_stages = {"closed_won", "closed_lost", "churned"}
    open_deals = [
        d for d in _DEALS.values() if d.get("stage") not in closed_stages
    ][:limit]

    if not open_deals:
        # Simulate a realistic pipeline for demo purposes
        open_deals = [
            {
                "deal_id": f"demo_{i}",
                "company": f"Demo Company {i}",
                "value_sar": 5_000.0 * (i + 1),
                "stage": _VALID_STAGES[i % 4],
                "probability": round(0.2 * (i + 1), 2),
                "created_at": datetime.now(UTC).isoformat(),
            }
            for i in range(min(limit, 5))
        ]

    total_value = sum(d.get("value_sar", 0) for d in open_deals)
    logger.info("crm_open_deals_listed", count=len(open_deals))
    return {
        "deals": open_deals,
        "total_count": len(open_deals),
        "total_value_sar": total_value,
    }


async def log_activity(
    entity_id: str,
    activity_type: str,
    notes: str = "",
) -> dict[str, Any]:
    """Log a CRM activity against a lead or deal.

    Parameters
    ----------
    entity_id:
        Lead or deal identifier.
    activity_type:
        One of: call, email, meeting, note, task.
    notes:
        Free-text activity notes (will be stored as-is).

    Returns
    -------
    dict
        Activity record with generated activity_id.
    """
    valid_types = {"call", "email", "meeting", "note", "task"}
    if activity_type not in valid_types:
        return {
            "logged": False,
            "error": f"invalid_activity_type: {activity_type!r}",
            "valid_types": sorted(valid_types),
        }

    activity = {
        "activity_id": str(uuid.uuid4())[:8],
        "entity_id": entity_id,
        "activity_type": activity_type,
        "notes": notes,
        "logged_at": datetime.now(UTC).isoformat(),
    }
    _ACTIVITIES.append(activity)
    logger.info("crm_activity_logged", entity_id=entity_id, activity_type=activity_type)
    return {"logged": True, "activity": activity}


__all__ = [
    "create_deal",
    "get_lead_profile",
    "list_open_deals",
    "log_activity",
    "update_lead_stage",
]

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...core.database import get_db
from ...models import Lead, Deal, Affiliate, Meeting
router = APIRouter()

@router.get("/executive")
async def exec_dashboard(db: AsyncSession = Depends(get_db)):
    leads = (await db.execute(select(func.count(Lead.id)))).scalar() or 0
    qualified = (await db.execute(select(func.count(lead.id).where(Lead.stage == "QUALIFIED"))).scalar() or 0
    meetings = (await db.execute(select(func.count(Meeting.id)).where(Meeting.status == "SCHEDULED")).scalar() or 0
    deals = (await db.execute(select(func.count(Deal.id)).where(Deal.status == "COMPLETED")).scalar() or 0
    revenue = (await db.execute(select(func.sum(Deal.value).where(Deal.status == "COMPLETED"))).scalar() or 0
    affiliates = (await db.execute(select(func.count(Affiliate.id)).where(Affiliate.status == "ACTIVE"))).scalar() or 0
    pipeline = {}
    for s in ["NEW","ATTEMPTED","CONNECTED","QUALIFIED","MEETING_BOOKED","PROPOSAL_SENT","NEGOTIATION","WON","LOST"]:
        pipeline[s] = (await db.execute(select(func.count(Lead.id).where(Lead.stage == s))).scalar() or 0
    return {"total_leads": leads, "qualified_leads": qualified, "booked_meetings": meetings, "closed_deals": deals, "monthly_revenue": revenue or 0, "active_affiliates": affiliates, "pipeline_by_stage": pipeline, "alerts": {"needs_attention": [], "high_intent": [], "risk": []}}

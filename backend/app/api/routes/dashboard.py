"""Dealix - Dashboard Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.deal import Deal
from app.models.lead import Lead
from app.models.affiliate import AffiliateProfile, AffiliatePayout
from app.schemas.dashboard import DashboardResponse, DashboardStats, DealFunnel, RevenueChart, TopPerformer

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


STAGE_NAMES = {
    "new": "جديد", "contacted": "تم التواصل", "qualified": "مؤهل",
    "proposal": "عرض مقدم", "negotiation": "تفاوض",
    "closed_won": "مكتمل", "closed_lost": "خاسر"
}


@router.get("", response_model=DashboardResponse)
async def get_dashboard(db: AsyncSession = Depends(get_async_db),
                        user: User = Depends(get_current_user)):
    # Stats
    total_deals = (await db.execute(select(func.count(Deal.id)))).scalar() or 0
    active_deals = (await db.execute(select(func.count(Deal.id)).where(Deal.is_active == True))).scalar() or 0
    closed_deals = (await db.execute(select(func.count(Deal.id)).where(Deal.stage == "closed_won"))).scalar() or 0
    total_leads = (await db.execute(select(func.count(Lead.id)))).scalar() or 0
    total_affiliates = (await db.execute(select(func.count(AffiliateProfile.id)))).scalar() or 0
    pending_payouts = (await db.execute(
        select(func.coalesce(func.sum(AffiliatePayout.amount), 0)).where(AffiliatePayout.status == "pending")
    )).scalar() or 0

    stats = DashboardStats(
        total_deals=total_deals, active_deals=active_deals, closed_deals=closed_deals,
        total_revenue=0.0, total_commissions=0.0, total_leads=total_leads,
        new_leads_this_month=0, conversion_rate=0.0, total_affiliates=total_affiliates,
        active_affiliates=0, pending_payouts=float(pending_payouts), upcoming_meetings=0
    )

    # Funnel
    funnel = []
    for stage, name in STAGE_NAMES.items():
        count = (await db.execute(select(func.count(Deal.id)).where(Deal.stage == stage))).scalar() or 0
        funnel.append(DealFunnel(stage=stage, stage_name_ar=name, count=count, value=0.0, percentage=0.0))

    return DashboardResponse(
        stats=stats, funnel=funnel, revenue_chart=[], top_performers=[], recent_activities=[]
    )

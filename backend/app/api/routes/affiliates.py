"""Dealix - Affiliate Routes"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.affiliate import AffiliateProfile, AffiliateLink, AffiliateClick, AffiliatePayout
from app.schemas.affiliate import (
    AffiliateProfileUpdate, AffiliateProfileResponse,
    AffiliateLinkCreate, AffiliateLinkResponse, AffiliateDashboardResponse, PayoutRequest
)

router = APIRouter(prefix="/affiliates", tags=["Affiliates"])


@router.get("/dashboard", response_model=AffiliateDashboardResponse)
async def affiliate_dashboard(db: AsyncSession = Depends(get_async_db),
                              user: User = Depends(get_current_user)):
    result = await db.execute(select(AffiliateProfile).where(AffiliateProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="ملف الأفلييت غير موجود")
    conversion_rate = (profile.total_conversions / profile.total_clicks * 100) if profile.total_clicks > 0 else 0
    return AffiliateDashboardResponse(
        total_earnings=profile.total_earnings, total_clicks=profile.total_clicks,
        total_conversions=profile.total_conversions, conversion_rate=round(conversion_rate, 2),
        active_links=0, recent_clicks=[], top_deals=[], monthly_earnings=[]
    )


@router.get("/profile", response_model=AffiliateProfileResponse)
async def get_profile(db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(AffiliateProfile).where(AffiliateProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="ملف الأفلييت غير موجود")
    return AffiliateProfileResponse.model_validate(profile)


@router.put("/profile", response_model=AffiliateProfileResponse)
async def update_profile(data: AffiliateProfileUpdate, db: AsyncSession = Depends(get_async_db),
                         user: User = Depends(get_current_user)):
    result = await db.execute(select(AffiliateProfile).where(AffiliateProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = AffiliateProfile(user_id=user.id)
        db.add(profile)
    update_data = data.model_dump(exclude_unset=True)
    if "social_links" in update_data and isinstance(update_data["social_links"], dict):
        import json
        update_data["social_links"] = json.dumps(update_data["social_links"])
    for field, value in update_data.items():
        setattr(profile, field, value)
    await db.flush()
    await db.refresh(profile)
    return AffiliateProfileResponse.model_validate(profile)


@router.post("/links", response_model=AffiliateLinkResponse, status_code=201)
async def create_link(data: AffiliateLinkCreate, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(AffiliateProfile).where(AffiliateProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="ملف الأفلييت غير موجود")
    slug = f"d{data.deal_id}-{uuid.uuid4().hex[:8]}"
    link = AffiliateLink(
        affiliate_id=profile.id, deal_id=data.deal_id, slug=slug,
        destination_url=f"/deals/{data.deal_id}?ref={slug}",
        utm_source=data.utm_source, utm_medium=data.utm_medium, utm_campaign=data.utm_campaign
    )
    db.add(link)
    await db.flush()
    await db.refresh(link)
    return AffiliateLinkResponse.model_validate(link)


@router.get("/links", response_model=list[AffiliateLinkResponse])
async def list_links(db: AsyncSession = Depends(get_async_db),
                     user: User = Depends(get_current_user)):
    result = await db.execute(select(AffiliateProfile).where(AffiliateProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        return []
    links_result = await db.execute(select(AffiliateLink).where(AffiliateLink.affiliate_id == profile.id))
    return [AffiliateLinkResponse.model_validate(l) for l in links_result.scalars().all()]


@router.post("/payouts/request")
async def request_payout(data: PayoutRequest, db: AsyncSession = Depends(get_async_db),
                         user: User = Depends(get_current_user)):
    result = await db.execute(select(AffiliateProfile).where(AffiliateProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="ملف الأفلييت غير موجود")
    if data.amount > profile.total_earnings:
        raise HTTPException(status_code=400, detail="المبلغ المطلوب أكبر من الأرباح المتاحة")
    payout = AffiliatePayout(
        affiliate_id=profile.id, amount=data.amount,
        payment_method=data.payment_method, currency="SAR"
    )
    db.add(payout)
    await db.flush()
    return {"message": "تم تقديم طلب السحب بنجاح", "payout_id": payout.id}

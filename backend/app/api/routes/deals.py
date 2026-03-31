"""Dealix - Deal Routes"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.deal import Deal, DealRedemption
from app.schemas.deal import DealCreate, DealUpdate, DealResponse, DealListResponse, DealRedemptionCreate, DealRedemptionResponse

router = APIRouter(prefix="/deals", tags=["Deals"])


def _slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[\s]+", "-", text)
    text = re.sub(r"[^\w\-]", "", text)
    return text + "-" + uuid.uuid4().hex[:8]


@router.get("", response_model=DealListResponse)
async def list_deals(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    stage: str | None = None,
    category: str | None = None,
    is_active: bool | None = None,
    is_featured: bool | None = None,
    search: str | None = None,
    db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
):
    query = select(Deal)
    count_query = select(func.count(Deal.id))
    if stage:
        query = query.where(Deal.stage == stage)
        count_query = count_query.where(Deal.stage == stage)
    if category:
        query = query.where(Deal.category == category)
        count_query = count_query.where(Deal.category == category)
    if is_active is not None:
        query = query.where(Deal.is_active == is_active)
        count_query = count_query.where(Deal.is_active == is_active)
    if is_featured is not None:
        query = query.where(Deal.is_featured == is_featured)
        count_query = count_query.where(Deal.is_featured == is_featured)
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(Deal.title.ilike(pattern), Deal.description.ilike(pattern)))
        count_query = count_query.where(or_(Deal.title.ilike(pattern), Deal.description.ilike(pattern)))

    total = (await db.execute(count_query)).scalar()
    query = query.order_by(Deal.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    items = [DealResponse.model_validate(d) for d in result.scalars().all()]
    return DealListResponse(items=items, total=total, page=page, per_page=per_page, pages=max(1, (total + per_page - 1) // per_page))


@router.post("", response_model=DealResponse, status_code=201)
async def create_deal(data: DealCreate, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    deal = Deal(**data.model_dump(), slug=_slugify(data.title), organization_id=user.id)
    db.add(deal)
    await db.flush()
    await db.refresh(deal)
    return DealResponse.model_validate(deal)


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: int, db: AsyncSession = Depends(get_async_db),
                   user: User = Depends(get_current_user)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="الصفقة غير موجودة")
    return DealResponse.model_validate(deal)


@router.put("/{deal_id}", response_model=DealResponse)
async def update_deal(deal_id: int, data: DealUpdate, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="الصفقة غير موجودة")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(deal, field, value)
    await db.flush()
    await db.refresh(deal)
    return DealResponse.model_validate(deal)


@router.delete("/{deal_id}")
async def delete_deal(deal_id: int, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="الصفقة غير موجودة")
    deal.is_active = False
    await db.flush()
    return {"message": "تم حذف الصفقة"}


@router.post("/{deal_id}/redemptions", response_model=DealRedemptionResponse, status_code=201)
async def create_redemption(deal_id: int, data: DealRedemptionCreate,
                            db: AsyncSession = Depends(get_async_db),
                            user: User = Depends(get_current_user)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="الصفقة غير موجودة")
    import secrets
    code = secrets.token_hex(6).upper()
    redemption = DealRedemption(
        deal_id=deal_id, redemption_code=code,
        **data.model_dump(exclude={"deal_id"}),
        commission_earned=data.amount * (deal.commission_amount / 100) if deal.commission_type == "percentage" else deal.commission_amount
    )
    deal.current_redemptions += 1
    db.add(redemption)
    await db.flush()
    await db.refresh(redemption)
    return DealRedemptionResponse.model_validate(redemption)

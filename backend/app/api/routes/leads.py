"""Dealix - Lead Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadListResponse

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("", response_model=LeadListResponse)
async def list_leads(
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    status: str | None = None, score: str | None = None, source: str | None = None,
    search: str | None = None, db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
):
    query = select(Lead).where(Lead.is_active == True)
    count_query = select(func.count(Lead.id)).where(Lead.is_active == True)
    if status:
        query = query.where(Lead.status == status)
        count_query = count_query.where(Lead.status == status)
    if score:
        query = query.where(Lead.score == score)
        count_query = count_query.where(Lead.score == score)
    if source:
        query = query.where(Lead.source == source)
        count_query = count_query.where(Lead.source == source)
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(Lead.full_name.ilike(pattern), Lead.company.ilike(pattern), Lead.email.ilike(pattern)))
        count_query = count_query.where(or_(Lead.full_name.ilike(pattern), Lead.company.ilike(pattern), Lead.email.ilike(pattern)))
    total = (await db.execute(count_query)).scalar()
    query = query.order_by(Lead.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    items = [LeadResponse.model_validate(l) for l in result.scalars().all()]
    return LeadListResponse(items=items, total=total, page=page, per_page=per_page, pages=max(1, (total + per_page - 1) // per_page))


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(data: LeadCreate, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    lead = Lead(**data.model_dump())
    db.add(lead)
    await db.flush()
    await db.refresh(lead)
    return LeadResponse.model_validate(lead)


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: int, db: AsyncSession = Depends(get_async_db),
                   user: User = Depends(get_current_user)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="العميل المحتمل غير موجود")
    return LeadResponse.model_validate(lead)


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: int, data: LeadUpdate, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="العميل المحتمل غير موجود")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    await db.flush()
    await db.refresh(lead)
    return LeadResponse.model_validate(lead)


@router.delete("/{lead_id}")
async def delete_lead(lead_id: int, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="العميل المحتمل غير موجود")
    lead.is_active = False
    await db.flush()
    return {"message": "تم حذف العميل المحتمل"}

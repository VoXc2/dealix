from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...core.database import get_db
from ...models import Lead
router = APIRouter()

@router.post("/")
async def create_lead(req: dict, db: AsyncSession = Depends(get_db)):
    lead = Lead(**{k: v for k, v in req.items() if k in Lead.__table__.columns})
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return {"success": True, "id": lead.id, "stage": lead.stage}

@router.get("/")
async def list_leads(stage: str = None, source: str = None, affiliate_id: int = None, page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    q = select(Lead)
    if stage: q = q.where(Lead.stage == stage)
    if source: q = q.where(Lead.source == source)
    if affiliate_id: q = q.where(Lead.affiliate_id == affiliate_id)
    total = (await db.execute(select(func.count(Lead.id)))).scalar() or 0
    return {"success": True, "data": (await db.execute(q.offset((page-1)*limit).limit(limit))).scalars().all(), "pagination": {"page": page, "limit": limit, "total": total}}

@router.get("/{id}")
async def get_lead(id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Lead).where(Lead.id == id))
    lead = r.scalar_one_or_none()
    if not lead: raise HTTPException(404, "Not found")
    return {"success": True, "data": lead}

@router.patch("/{id}/stage")
async def update_stage(id: int, req: dict, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Lead).where(Lead.id == id))
    lead = r.scalar_one_or_none()
    if not lead: raise HTTPException(404, "Not found")
    lead.stage = req.get("stage", lead.stage)
    await db.commit()
    return {"success": True, "id": id, "stage": lead.stage}

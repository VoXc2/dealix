from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...core.database import get_db
from ...models import Deal, Commission, Lead
router = APIRouter()

@router.post("/")
async def create_deal(req: dict, db: AsyncSession = Depends(get_db)):
    d = Deal(**{k: v for k, v in req.items() if k in Deal.__table__.columns})
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return {"success": True, "id": d.id, "stage": d.stage}

@router.get("/")
async def list_deals(status: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Deal)
    if status: q = q.where(Deal.status == status)
    return {"success": True, "data": (await db.execute(q)).scalars().all()}

@router.patch("/{id}/win")
async def win_deal(id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Deal).where(Deal.id == id))
    d = r.scalar_one_or_none()
    if not d: raise HTTPException(404, "Not found")
    d.status = "COMPLETED"
    d.stage = "PAYMENT_RECEIVED"
    if d.primary_attribution == "AFFILIATE" and d.primary_attribution_id:
        c = Commission(affiliate_id=d.primary_attribution_id, deal_id=d.id, lead_id=d.lead_id, status="PENDING", deal_value=d.value, commission_rate=10.0, commission_amount=d.value * 0.10)
        db.add(c)
    lr = await db.execute(select(Lead).where(Lead.id == d.lead_id))
    lead = lr.scalar_one_or_none()
    if lead:
        lead.stage = "WON"
        lead.deal_won = True
    await db.commit()
    return {"success": True, "id": id, "status": "COMPLETED"}

@router.get("/summary")
async def summary(db: AsyncSession = Depends(get_db)):
    total = (await db.execute(select(func.count(Deal.id))).scalar() or 0
    won = (await db.execute(select(func.count(Deal.id).where(Deal.status == "COMPLETED"))).scalar() or 0
    rev = (await db.execute(select(func.sum(Deal.value).where(Deal.status == "COMPLETED"))).scalar() or 0
    pipe = (await db.execute(select(func.sum(Deal.value).where(Deal.status == "ACTIVE"))).scalar() or 0
    return {"success": True, "total_deals": total, "won_deals": won, "total_revenue": rev or 0, "pipeline_value": pipe or 0}

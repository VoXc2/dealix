from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...core.database import get_db
from ...models import Meeting
router = APIRouter()

@router.post("/")
async def create_meeting(req: dict, db: AsyncSession = Depends(get_db)):
    m = Meeting(**{k: v for k, v in req.items() if k in Meeting.__table__.columns})
    db.add(m)
    await db.commit()
    await db.refresh(m)
    return {"success": True, "id": m.id, "status": m.status}

@router.get("/")
async def list_meetings(status: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Meeting)
    if status: q = q.where(Meeting.status == status)
    return {"success": True, "data": (await db.execute(q)).scalars().all()}

@router.patch("/{id}/complete")
async def complete(id: int, req: dict, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Meeting).where(Meeting.id == id))
    m = r.scalar_one_or_none()
    if not m: raise HTTPException(404, "Not found")
    m.status = req.get("status", "COMPLETED")
    m.outcome = req.get("outcome")
    await db.commit()
    return {"success": True, "id": id, "status": m.status}

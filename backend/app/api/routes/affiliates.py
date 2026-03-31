from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...core.database import get_db
from ...core.security import hash_pw
from ...models import User, Affiliate
import uuid
router = APIRouter()

@router.post("/apply")
async def apply(req: dict, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == req.get("email")))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Email exists")
    user = User(email=req["email"], name=req["full_name"], hashed_password=hash_pw(str(uuid.uuid4())[:12]), role="AFFILIATE", phone=req.get("phone"), city=req.get("city"))
    db.add(user)
    await db.flush()
    aff = Affiliate(user_id=user.id, affiliate_code=f"DIX-{uuid.uuid4().hex[:8].upper()}", city=req.get("city"), arabic_level=req.get("arabic_level"), english_level=req.get("english_level"), preferred_channels=req.get("preferred_channels", []), can_do_calls=req.get("can_do_calls", False), can_do_whatsapp=req.get("can_do_whatsapp", True), can_do_field=req.get("can_do_field", False))
    db.add(aff)
    await db.commit()
    return {"success": True, "affiliate_code": aff.affiliate_code, "status": "APPLIED"}

@router.get("/")
async def list_affiliates(status: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Affiliate)
    if status: q = q.where(Affiliate.status == status)
    return {"success": True, "data": (await db.execute(q)).scalars().all()}

@router.get("/{id}")
async def get_affiliate(id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Affiliate).where(Affiliate.id == id))
    aff = r.scalar_one_or_none()
    if not aff: raise HTTPException(404, "Not found")
    return {"success": True, "data": aff}

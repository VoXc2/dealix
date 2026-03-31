from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...core.database import get_db
from ...core.security import hash_pw, verify_pw, create_token
from ...models import User
router = APIRouter()

@router.post("/login")
async def login(req: dict, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(User).where(User.email == req.get("email", "")))
    user = r.scalar_one_or_none()
    if not user or not verify_pw(req.get("password", ""), user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token({"sub": user.id, "role": user.role}), "user": {"id": user.id, "email": user.email, "name": user.name, "role": user.role}}

@router.post("/register")
async def register(req: dict, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == req.get("email")))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Email exists")
    user = User(email=req["email"], name=req["name"], hashed_password=hash_pw(req["password"]), role=req.get("role", "VIEWER"))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "email": user.email}

"""Dealix - Meeting Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse, MeetingListResponse

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.get("", response_model=MeetingListResponse)
async def list_meetings(
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    status: str | None = None, db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
):
    query = select(Meeting).where(Meeting.created_by == user.id)
    count_query = select(func.count(Meeting.id)).where(Meeting.created_by == user.id)
    if status:
        query = query.where(Meeting.status == status)
        count_query = count_query.where(Meeting.status == status)
    total = (await db.execute(count_query)).scalar()
    query = query.order_by(Meeting.scheduled_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    items = [MeetingResponse.model_validate(m) for m in result.scalars().all()]
    return MeetingListResponse(items=items, total=total)


@router.post("", response_model=MeetingResponse, status_code=201)
async def create_meeting(data: MeetingCreate, db: AsyncSession = Depends(get_async_db),
                         user: User = Depends(get_current_user)):
    import json
    meeting = Meeting(**data.model_dump(), created_by=user.id,
                      attendees=json.dumps(data.attendees) if data.attendees else None)
    db.add(meeting)
    await db.flush()
    await db.refresh(meeting)
    return MeetingResponse.model_validate(meeting)


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(meeting_id: int, db: AsyncSession = Depends(get_async_db),
                      user: User = Depends(get_current_user)):
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="الاجتماع غير موجود")
    return MeetingResponse.model_validate(meeting)


@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(meeting_id: int, data: MeetingUpdate, db: AsyncSession = Depends(get_async_db),
                         user: User = Depends(get_current_user)):
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="الاجتماع غير موجود")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(meeting, field, value)
    await db.flush()
    await db.refresh(meeting)
    return MeetingResponse.model_validate(meeting)


@router.delete("/{meeting_id}")
async def delete_meeting(meeting_id: int, db: AsyncSession = Depends(get_async_db),
                         user: User = Depends(get_current_user)):
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="الاجتماع غير موجود")
    meeting.status = "cancelled"
    await db.flush()
    return {"message": "تم إلغاء الاجتماع"}

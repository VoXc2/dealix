"""Dealix - Meeting Schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MeetingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    description: Optional[str] = None
    meeting_type: str = "video_call"
    scheduled_at: datetime
    duration_minutes: int = Field(ge=15, le=480, default=30)
    location: Optional[str] = None
    video_link: Optional[str] = None
    phone_number: Optional[str] = None
    deal_id: Optional[int] = None
    lead_id: Optional[int] = None
    attendees: Optional[List[str]] = None
    agenda: Optional[str] = None


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    meeting_type: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    video_link: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_notes: Optional[str] = None


class MeetingResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    meeting_type: str
    status: str
    scheduled_at: datetime
    duration_minutes: int
    actual_duration_minutes: Optional[int]
    location: Optional[str]
    video_link: Optional[str]
    created_by: int
    deal_id: Optional[int]
    lead_id: Optional[int]
    attendees: Optional[str]
    agenda: Optional[str]
    outcome: Optional[str]
    reminder_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MeetingListResponse(BaseModel):
    items: List[MeetingResponse]
    total: int

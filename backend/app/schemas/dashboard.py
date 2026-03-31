"""Dealix - Dashboard Schemas"""
from typing import Optional, List
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_deals: int
    active_deals: int
    closed_deals: int
    total_revenue: float
    total_commissions: float
    total_leads: int
    new_leads_this_month: int
    conversion_rate: float
    total_affiliates: int
    active_affiliates: int
    pending_payouts: float
    upcoming_meetings: int


class DealFunnel(BaseModel):
    stage: str
    stage_name_ar: str
    count: int
    value: float
    percentage: float


class RevenueChart(BaseModel):
    month: str
    revenue: float
    commissions: float
    deals_count: int


class TopPerformer(BaseModel):
    id: int
    name: str
    deals_closed: int
    revenue: float
    conversion_rate: float


class DashboardResponse(BaseModel):
    stats: DashboardStats
    funnel: List[DealFunnel]
    revenue_chart: List[RevenueChart]
    top_performers: List[TopPerformer]
    recent_activities: List[dict]

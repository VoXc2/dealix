"""
Analytics domain — growth, company brain, market intelligence, radar.
مجال التحليلات — النمو، دماغ الشركة، ذكاء السوق، الرادار.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    company_brain,
    company_growth_beast,
    full_ops_radar as full_ops_radar_router,
    growth_beast,
    growth_os,
    growth_v10,
    gtm_os,
    partnership_os,
    proof_to_market,
    radar_events as radar_events_router,
    revenue_pipeline,
    search_radar,
    unified_operating_graph as unified_operating_graph_router,
)

_ROUTERS = [
    growth_os.router,
    growth_v10.router,
    growth_beast.router,
    company_growth_beast.router,
    company_brain.router,
    gtm_os.router,
    search_radar.router,
    radar_events_router.router,
    full_ops_radar_router.router,
    unified_operating_graph_router.router,
    partnership_os.router,
    proof_to_market.router,
]


def get_routers() -> list[APIRouter]:
    """Return all analytics-domain routers."""
    return _ROUTERS

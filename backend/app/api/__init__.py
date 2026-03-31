from fastapi import APIRouter
from .routes import health, auth, affiliates, leads, meetings, deals, dashboard
api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(affiliates.router, prefix="/affiliates", tags=["affiliates"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(deals.router, prefix="/deals", tags=["deals"])

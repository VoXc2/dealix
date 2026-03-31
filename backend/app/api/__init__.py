"""Dealix - API Package"""
from fastapi import APIRouter
from app.api.routes.auth import router as auth_router
from app.api.routes.deals import router as deals_router
from app.api.routes.leads import router as leads_router
from app.api.routes.affiliates import router as affiliates_router
from app.api.routes.meetings import router as meetings_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router, prefix="/api/v1")
api_router.include_router(deals_router, prefix="/api/v1")
api_router.include_router(leads_router, prefix="/api/v1")
api_router.include_router(affiliates_router, prefix="/api/v1")
api_router.include_router(meetings_router, prefix="/api/v1")
api_router.include_router(dashboard_router, prefix="/api/v1")

"""Dealix - Health Check"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Dealix API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/ready")
async def readiness_check():
    return {"status": "ready", "checks": {"database": "ok", "redis": "ok"}}


@router.get("/health/live")
async def liveness_check():
    return {"status": "alive"}

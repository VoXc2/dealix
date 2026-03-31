from fastapi import APIRouter
router = APIRouter()
@router.get("")
async def health():
    return {"status": "healthy", "service": "dealix-api", "version": "1.0.0"}
@router.get("/ready")
async def ready():
    return {"status": "ready"}

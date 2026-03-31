"""Dealix - Main Application"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_redis
from app.api import api_router

logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Dealix...")
    await init_db()
    from app.extensions import init_redis
    await init_redis()
    logger.info("Dealix started successfully")
    yield
    await close_redis()
    logger.info("Dealix shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    description="منصة Dealix لإدارة الصفقات والتسويق بالعمولة في السوق السعودي",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if not settings.is_production else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"service": "Dealix API", "version": "1.0.0", "docs": "/docs"}

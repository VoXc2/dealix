"""Async database session management."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config.settings import get_settings


@lru_cache(maxsize=1)
def _engine():
    """Lazy-create async engine with production-grade pool settings."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=settings.is_development,
        pool_pre_ping=True,
        # Pool sizing: 20 workers × ~1 connection + 30 burst capacity.
        # For PgBouncer deployments these can be lowered to 2/5.
        pool_size=20,
        max_overflow=30,
        pool_timeout=30,  # seconds to wait for a connection from pool
        pool_recycle=1800,  # recycle connections every 30 min to avoid stale TCP
    )


@lru_cache(maxsize=1)
def async_session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(_engine(), expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — async DB session."""
    async with async_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Async context manager for DB sessions (`async with get_session() as session:`)."""
    async with async_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create all tables (dev only — production uses Alembic)."""
    # Side-effect imports — register out-of-line models on Base.metadata
    # (kept in their own files to avoid bloating models.py).
    import db.models_revenue_events
    import db.models_workflow_runs
    from db.models import Base

    async with _engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

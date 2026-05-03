"""Async database session management."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config.settings import get_settings


@lru_cache(maxsize=1)
def _engine():
    """Lazy-create async engine."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=settings.is_development,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


@lru_cache(maxsize=1)
def _sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(_engine(), expire_on_commit=False, class_=AsyncSession)


def async_session_factory() -> AsyncSession:
    """Return a fresh AsyncSession.

    Routers use this as `async with async_session_factory() as session:` —
    AsyncSession is itself an async context manager.
    """
    return _sessionmaker()()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — async DB session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Async context manager for DB sessions (`async with get_session() as session:`)."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create all tables (dev only — production uses Alembic)."""
    from db.models import Base

    async with _engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

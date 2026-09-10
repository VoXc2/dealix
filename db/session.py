"""Async database session management."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config.settings import get_settings


def _engine_options(database_url: str, *, echo: bool) -> dict[str, object]:
    """Return backend-compatible SQLAlchemy engine options.

    QueuePool sizing is production tuning for PostgreSQL. SQLite memory/test
    engines use StaticPool and reject QueuePool-only arguments such as
    pool_size, max_overflow, and pool_timeout.
    """
    options: dict[str, object] = {
        "echo": echo,
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }
    if make_url(database_url).get_backend_name() != "sqlite":
        options.update(
            pool_size=20,
            max_overflow=30,
            pool_timeout=30,
        )
    return options


@lru_cache(maxsize=1)
def _engine():
    """Lazy-create an async engine with backend-compatible pool settings."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        **_engine_options(settings.database_url, echo=settings.is_development),
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
    """Create all registered tables (development only)."""
    from db.model_registry import load_all_models
    from db.models import Base

    load_all_models()
    async with _engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

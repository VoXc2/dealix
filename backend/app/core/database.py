"""
Dealix - إدارة قاعدة البيانات
"""
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as sync_sessionmaker
from typing import AsyncGenerator

from app.core.config import settings


class Base(DeclarativeBase):
    """النموذج الأساسي لجميع النماذج"""
    pass


# محرك غير متزامن
async_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# محرك متزامن (للتهجيرات و Celery)
sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# جلسات غير متزامنة
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# جلسات متزامنة
SyncSessionLocal = sync_sessionmaker(
    bind=sync_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """مُعتمد FastAPI للحصول على جلسة قاعدة بيانات"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    """للاستخدام مع Celery والعمال"""
    db = SyncSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


async def init_db() -> None:
    """إنشاء جميع الجداول"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """حذف جميع الجداول - للبيئة التطويرية فقط"""
    if not settings.is_production:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

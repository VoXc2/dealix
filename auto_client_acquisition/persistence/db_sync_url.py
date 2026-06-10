"""Convert async application DATABASE_URL to a sync SQLAlchemy URL when possible."""

from __future__ import annotations


def sync_sqlalchemy_url(async_or_sync_url: str) -> str:
    """Map ``postgresql+asyncpg://`` to ``postgresql+psycopg://`` for sync engines."""
    u = (async_or_sync_url or "").strip()
    if "+asyncpg" in u:
        return u.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    return u


__all__ = ["sync_sqlalchemy_url"]

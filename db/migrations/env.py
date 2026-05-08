"""
Alembic async migration environment.
بيئة ترحيل Alembic غير المتزامن.

Reads DATABASE_URL from the same settings as the app so there is a single
source of truth. Uses SQLAlchemy 2.0 async engine (asyncpg driver).
"""

from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ── Load app metadata ──────────────────────────────────────────────
# Import Base so all models are registered
from db.models import Base  # noqa: F401 — registers all mapped classes

# ── Alembic Config ─────────────────────────────────────────────────
config = context.config

# Inject DATABASE_URL from app settings (respects .env)
try:
    from core.config.settings import get_settings
    _db_url = get_settings().database_url
except Exception:
    _db_url = os.getenv("DATABASE_URL", "")

# Convert async URL to sync for offline mode (alembic needs a sync URL)
_sync_url = _db_url.replace("postgresql+asyncpg://", "postgresql://")
config.set_main_option("sqlalchemy.url", _sync_url)

# Setup Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ── Offline mode (generate SQL without connecting) ─────────────────
def run_migrations_offline() -> None:
    """Write SQL to stdout — useful for review before applying."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online async mode ──────────────────────────────────────────────
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Use the async engine to run migrations."""
    # Use asyncpg URL for the live run
    config.set_main_option("sqlalchemy.url", _db_url)
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

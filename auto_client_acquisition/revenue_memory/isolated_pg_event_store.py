"""
Isolated-thread Postgres revenue event store with a synchronous API.

``AsyncEngine`` from SQLAlchemy/asyncpg must not be used across different
asyncio event loops. The main FastAPI app uses ``db.session.async_session_factory``
on the request loop; sync callers (``Orchestrator``, ``append_event``, routers
that call ``store.append()``) therefore cannot safely share that factory.

This module runs a daemon thread with its **own** asyncio loop and async engine
(same ``DATABASE_URL``), wraps ``PostgresEventStore``, and exposes the sync
``EventStore`` operations via ``asyncio.run_coroutine_threadsafe``.

**Connection pools:** this worker uses a **second** async connection pool to the
same database URL as ``db.session``. Budget max connections accordingly; a
future refactor may route all revenue-event IO through one async surface to
collapse pools.
"""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Iterator
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from auto_client_acquisition.revenue_memory.events import RevenueEvent
from auto_client_acquisition.revenue_memory.pg_event_store import PostgresEventStore
from core.config.settings import get_settings

_state_lock = threading.RLock()
_worker_loop: asyncio.AbstractEventLoop | None = None
_worker_engine: Any = None
_worker_inner: PostgresEventStore | None = None
_worker_thread: threading.Thread | None = None
_worker_ready = threading.Event()
_store_singleton: IsolatedSyncPostgresEventStore | None = None


class IsolatedSyncPostgresEventStore:
    """Sync ``EventStore``-shaped facade over ``PostgresEventStore`` on a worker loop."""

    __slots__ = ("_inner", "_loop")

    def __init__(self, loop: asyncio.AbstractEventLoop, inner: PostgresEventStore) -> None:
        self._loop = loop
        self._inner = inner

    def _run(self, coro: Any, *, timeout: float = 120.0) -> Any:
        if not self._loop.is_running():
            raise RuntimeError("isolated postgres event loop is not running")
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return fut.result(timeout=timeout)

    def append(self, event: RevenueEvent) -> None:
        self._run(self._inner.append(event))

    def append_many(self, events: list[RevenueEvent]) -> None:
        self._run(self._inner.append_many(events))

    def read_for_customer(
        self,
        customer_id: str,
        *,
        since: datetime | None = None,
        until: datetime | None = None,
        event_types: tuple[str, ...] | None = None,
    ) -> Iterator[RevenueEvent]:
        async def _collect() -> list[RevenueEvent]:
            out: list[RevenueEvent] = []
            async for e in self._inner.read_for_customer(
                customer_id,
                since=since,
                until=until,
                event_types=event_types,
            ):
                out.append(e)
            return out

        return iter(self._run(_collect()))

    def read_for_subject(
        self,
        subject_type: str,
        subject_id: str,
        *,
        customer_id: str | None = None,
    ) -> Iterator[RevenueEvent]:
        async def _collect() -> list[RevenueEvent]:
            out: list[RevenueEvent] = []
            async for e in self._inner.read_for_subject(
                subject_type, subject_id, customer_id=customer_id
            ):
                out.append(e)
            return out

        return iter(self._run(_collect()))

    def count(self, customer_id: str | None = None) -> int:
        return int(self._run(self._inner.count(customer_id)))


def _worker_main() -> None:
    global _worker_loop, _worker_engine, _worker_inner

    settings = get_settings()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _worker_loop = loop
    _worker_engine = create_async_engine(
        settings.database_url,
        echo=settings.is_development,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )
    factory = async_sessionmaker(
        _worker_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    _worker_inner = PostgresEventStore(factory)
    _worker_ready.set()
    loop.run_forever()


def get_isolated_sync_postgres_store() -> IsolatedSyncPostgresEventStore:
    """Singleton sync facade; safe for ``Orchestrator`` and sync HTTP handlers."""
    global _worker_thread, _store_singleton

    with _state_lock:
        if (
            _store_singleton is not None
            and _worker_loop is not None
            and _worker_loop.is_running()
        ):
            return _store_singleton

        if _worker_thread is not None and _worker_thread.is_alive():
            _worker_thread.join(timeout=5.0)

        _worker_ready.clear()
        _worker_loop = None
        _worker_engine = None
        _worker_inner = None
        _store_singleton = None

        t = threading.Thread(target=_worker_main, name="dealix-revenue-pg-isolated", daemon=True)
        t.start()
        _worker_thread = t
        if not _worker_ready.wait(timeout=60.0):
            raise RuntimeError("timed out starting isolated postgres revenue worker")

        if _worker_loop is None or _worker_inner is None:
            raise RuntimeError("isolated postgres revenue worker failed to initialize store")

        _store_singleton = IsolatedSyncPostgresEventStore(_worker_loop, _worker_inner)
        return _store_singleton


def shutdown_isolated_postgres_revenue_worker() -> None:
    """Stop the worker loop and dispose the engine (tests / explicit teardown)."""
    global _worker_loop, _worker_inner, _worker_thread, _store_singleton, _worker_engine

    with _state_lock:
        loop = _worker_loop
        engine = _worker_engine
        if loop is None or not loop.is_running():
            _store_singleton = None
            _worker_loop = None
            _worker_inner = None
            _worker_engine = None
            th = _worker_thread
            _worker_thread = None
            if th is not None and th.is_alive():
                th.join(timeout=1.0)
            return

        async def _shutdown() -> None:
            if engine is not None:
                await engine.dispose()
            loop.stop()

        try:
            fut = asyncio.run_coroutine_threadsafe(_shutdown(), loop)
            fut.result(timeout=120.0)
        except Exception:
            try:
                loop.call_soon_threadsafe(loop.stop)
            except Exception:
                pass

        th = _worker_thread
        _worker_loop = None
        _worker_inner = None
        _worker_engine = None
        _worker_thread = None
        _store_singleton = None
        if th is not None and th.is_alive():
            th.join(timeout=5.0)

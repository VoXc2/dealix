"""Tests for async append facade (memory + optional postgres)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auto_client_acquisition.revenue_memory.event_store import reset_default_store
from auto_client_acquisition.revenue_memory.events import make_event


@pytest.mark.asyncio
async def test_append_memory_only_appends_once():
    reset_default_store()
    from auto_client_acquisition.revenue_memory import async_facade

    mock_settings = MagicMock()
    mock_settings.revenue_memory_backend = "memory"

    e = make_event(
        event_type="lead.created",
        customer_id="cust_mem_only",
        subject_type="account",
        subject_id="a1",
    )
    with patch.object(async_facade, "get_settings", return_value=mock_settings):
        await async_facade.append_revenue_event(e)

    from auto_client_acquisition.revenue_memory.event_store import get_default_store

    assert get_default_store("memory").count(customer_id="cust_mem_only") >= 1


@pytest.mark.asyncio
async def test_append_postgres_dual_write():
    reset_default_store()
    from auto_client_acquisition.revenue_memory import async_facade

    mock_settings = MagicMock()
    mock_settings.revenue_memory_backend = "postgres"

    e = make_event(
        event_type="lead.created",
        customer_id="cust_pg_dual",
        subject_type="account",
        subject_id="a1",
        tenant_id="ten_x",
    )

    mock_pg = MagicMock()
    mock_pg.append = AsyncMock()

    with (
        patch.object(async_facade, "get_settings", return_value=mock_settings),
        patch.object(async_facade, "get_postgres_store", return_value=mock_pg),
    ):
        await async_facade.append_revenue_event(e)

    mock_pg.append.assert_awaited_once()
    from auto_client_acquisition.revenue_memory.event_store import get_default_store

    assert get_default_store("memory").count(customer_id="cust_pg_dual") >= 1

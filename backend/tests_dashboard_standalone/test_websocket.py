"""
Tests: WebSocket endpoint and event bus
"""
from __future__ import annotations

import asyncio
import pytest

from conftest import auth, TENANT_A_ID, app, DEFAULT_TENANT_ID


@pytest.mark.asyncio
async def test_websocket_publish():
    """Publishing an event via event bus does not raise."""
    from dashboard_api_module import publish_event

    async def run():
        await publish_event("test.event", {"data": "hello"}, DEFAULT_TENANT_ID)
        await asyncio.sleep(0.05)
        return True

    result = await asyncio.wait_for(run(), timeout=3.0)
    assert result is True


@pytest.mark.asyncio
async def test_ws_manager_connect_disconnect():
    """WS manager connect/disconnect lifecycle."""
    from dashboard_api_module import ws_manager

    class FakeWS:
        accepted = False
        sent = []

        async def accept(self):
            self.accepted = True

        async def send_json(self, data):
            self.sent.append(data)

    ws = FakeWS()
    tenant_id = "test-tenant-ws"

    await ws_manager.connect(ws, tenant_id)
    assert ws.accepted
    assert ws_manager.count(tenant_id) == 1

    await ws_manager.broadcast(tenant_id, {"type": "test", "payload": {}})
    assert len(ws.sent) == 1

    ws_manager.disconnect(ws, tenant_id)
    assert ws_manager.count(tenant_id) == 0


@pytest.mark.asyncio
async def test_event_bus_queue():
    """Event bus accepts events without overflow on small queues."""
    from dashboard_api_module import publish_event, event_bus

    # Drain current queue
    while not event_bus.empty():
        event_bus.get_nowait()

    # Publish several events
    for i in range(5):
        await publish_event("test.batch", {"i": i}, DEFAULT_TENANT_ID)

    # Queue should have items
    assert not event_bus.empty()

    # Drain
    events = []
    while not event_bus.empty():
        events.append(event_bus.get_nowait())

    assert any(e["type"] == "test.batch" for e in events)

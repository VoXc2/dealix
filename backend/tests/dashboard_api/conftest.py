"""
Shared fixtures for dashboard_api tests.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path

import aiosqlite
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from passlib.context import CryptContext

# Ensure the backend directory is on sys.path so 'dashboard_api' resolves correctly
_BACKEND_DIR = str(Path(__file__).parent.parent.parent)
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

# Use a temp DB for all tests
_tmp_dir = tempfile.mkdtemp(prefix="dealix_test_")
TEST_DB = str(Path(_tmp_dir) / "test_leads.db")
os.environ["DEALIX_DB"] = TEST_DB

# Import after setting env var and fixing path
import importlib
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "dashboard_api_module",
    Path(_BACKEND_DIR) / "dashboard_api.py"
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["dashboard_api_module"] = _mod
_spec.loader.exec_module(_mod)

app = _mod.app
migrate_db = _mod.migrate_db
DEFAULT_TENANT_ID = _mod.DEFAULT_TENANT_ID
hash_password = _mod.hash_password

TENANT_A_ID = DEFAULT_TENANT_ID  # 00000000-0000-0000-0000-000000000001
TENANT_B_ID = "00000000-0000-0000-0000-000000000002"
USER_A_ID = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
USER_B_ID = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"


@pytest_asyncio.fixture(scope="session")
async def setup_db():
    """Run migrations and seed minimal test data once per session."""
    await migrate_db()

    async with aiosqlite.connect(TEST_DB) as db:
        pw_hash = hash_password("testpass123")

        # Tenants
        await db.execute(
            "INSERT OR IGNORE INTO tenants (id, name) VALUES (?,?)",
            (TENANT_A_ID, "Tenant Alpha")
        )
        await db.execute(
            "INSERT OR IGNORE INTO tenants (id, name) VALUES (?,?)",
            (TENANT_B_ID, "Tenant Beta")
        )

        # Users
        await db.execute("""
            INSERT OR IGNORE INTO users (id, tenant_id, email, password_hash, role, api_keys)
            VALUES (?,?,?,?,?,?)
        """, (USER_A_ID, TENANT_A_ID, "user_a@test.com", pw_hash, "admin", "{}"))

        await db.execute("""
            INSERT OR IGNORE INTO users (id, tenant_id, email, password_hash, role, api_keys)
            VALUES (?,?,?,?,?,?)
        """, (USER_B_ID, TENANT_B_ID, "user_b@test.com", pw_hash, "admin", "{}"))

        # Leads for tenant A
        lead_a_id = "lead-a-" + str(uuid.uuid4())[:8]
        await db.execute("""
            INSERT OR IGNORE INTO leads
                (id, phone, company_name, sector, stage, tenant_id, score_total,
                 priority_tier, value_sar, last_channel, first_seen, last_seen,
                 employees, score_breakdown, tech_stack, contributing_signals,
                 penalizing_factors, contacts)
            VALUES (?,?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'),?,?,?,?,?,?)
        """, (
            lead_a_id, "+966501111111", "Alpha Corp", "ecommerce", "new",
            TENANT_A_ID, 75.0, "warm", 50000, "whatsapp", 100,
            json.dumps({"icp": 80, "intent": 70, "timing": 60, "budget": 75, "authority": 65, "engagement": 10}),
            json.dumps(["Shopify"]), json.dumps(["ICP match"]), json.dumps([]), json.dumps([])
        ))

        # Lead for tenant B (should be invisible to tenant A)
        lead_b_id = "lead-b-" + str(uuid.uuid4())[:8]
        await db.execute("""
            INSERT OR IGNORE INTO leads
                (id, phone, company_name, sector, stage, tenant_id, score_total,
                 priority_tier, value_sar, last_channel, first_seen, last_seen,
                 employees, score_breakdown, tech_stack, contributing_signals,
                 penalizing_factors, contacts)
            VALUES (?,?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'),?,?,?,?,?,?)
        """, (
            lead_b_id, "+966502222222", "Beta Corp", "retail", "qualified",
            TENANT_B_ID, 55.0, "cool", 30000, "email", 50,
            json.dumps({"icp": 60, "intent": 50, "timing": 40, "budget": 55, "authority": 45, "engagement": 0}),
            json.dumps([]), json.dumps([]), json.dumps([]), json.dumps([])
        ))

        # Agent for tenant A
        await db.execute("""
            INSERT OR IGNORE INTO agents (id, name, channel, status, msgs_today,
                success_rate, cost_today, tenant_id)
            VALUES (?,?,?,?,?,?,?,?)
        """, ("agent-test-001", "Test Agent", "whatsapp", "active", 10, 0.75, 5.0, TENANT_A_ID))

        # Conversation + messages for tenant A
        await db.execute("""
            INSERT OR IGNORE INTO conversations
                (phone, channel, lead_name, last_message_preview, unread_count,
                 sentiment, stage, tenant_id, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))
        """, ("+966501111111", "whatsapp", "Alpha User", "مرحبا", 1, "positive", "new", TENANT_A_ID))

        await db.execute("""
            INSERT INTO messages (phone, direction, body, channel, tenant_id, created_at)
            VALUES (?,?,?,?,?,datetime('now'))
        """, ("+966501111111", "in", "مرحبا، أريد معرفة المزيد", "whatsapp", TENANT_A_ID))

        # Sources health for tenant A
        await db.execute("""
            INSERT OR IGNORE INTO sources_health
                (source_name, status, records_imported, tenant_id)
            VALUES (?,?,?,?)
        """, ("saudi_registry", "ok", 100, TENANT_A_ID))

        # Playbook for tenant A
        await db.execute("""
            INSERT OR IGNORE INTO playbooks (id, name, sector, steps, active_count, tenant_id)
            VALUES (?,?,?,?,?,?)
        """, ("pb-test", "Test Playbook", "ecommerce", json.dumps([{"step": 1}]), 5, TENANT_A_ID))

        await db.commit()

    yield {
        "tenant_a": TENANT_A_ID,
        "tenant_b": TENANT_B_ID,
        "lead_a_id": lead_a_id,
        "lead_b_id": lead_b_id,
    }


@pytest_asyncio.fixture(scope="session")
async def client(setup_db):
    """Async HTTP client for the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c


@pytest_asyncio.fixture(scope="session")
async def token_a(client):
    """JWT token for user A (tenant A)."""
    r = await client.post("/api/v1/auth/login", json={
        "email": "user_a@test.com",
        "password": "testpass123"
    })
    assert r.status_code == 200, f"Login A failed: {r.text}"
    return r.json()["access_token"]


@pytest_asyncio.fixture(scope="session")
async def token_b(client):
    """JWT token for user B (tenant B)."""
    r = await client.post("/api/v1/auth/login", json={
        "email": "user_b@test.com",
        "password": "testpass123"
    })
    assert r.status_code == 200, f"Login B failed: {r.text}"
    return r.json()["access_token"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

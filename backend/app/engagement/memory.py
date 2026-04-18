"""
Dealix — ConversationMemory
============================
Async SQLite-backed conversation store using aiosqlite.

Tables:
  leads         — one row per (channel, address) with enrichment fields
  conversations — session grouping (one per lead + channel)
  messages      — individual messages (inbound + outbound)

Schema extends whatsapp_webhook.py style with richer fields:
  channel, sentiment, intent, stage

Usage:
    mem = ConversationMemory(db_path="dealix.db")
    await mem.init()
    await mem.upsert_lead(channel="whatsapp", address="+966512345678", name="Ahmed")
    await mem.save_message(channel="whatsapp", address="+966512345678",
                           direction="in", body="مرحبا")
    history = await mem.get_history(channel="whatsapp", address="+966512345678")
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiosqlite

logger = logging.getLogger("dealix.engagement.memory")

_SCHEMA_SQL = """
-- ── Leads ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS leads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    channel         TEXT    NOT NULL,                    -- 'whatsapp' | 'email' | 'linkedin' | 'sms' ...
    address         TEXT    NOT NULL,                    -- phone | email | linkedin_urn | etc.
    name            TEXT,
    company         TEXT,
    sector          TEXT,
    city            TEXT,
    stage           TEXT    DEFAULT 'new',              -- LeadStage enum value
    opt_in          INTEGER DEFAULT 1,                  -- 0 = opted out (PDPL)
    first_seen      TEXT    NOT NULL,
    last_seen       TEXT    NOT NULL,
    message_count   INTEGER DEFAULT 0,
    UNIQUE(channel, address)
);
CREATE INDEX IF NOT EXISTS idx_leads_channel_address ON leads(channel, address);
CREATE INDEX IF NOT EXISTS idx_leads_stage           ON leads(stage);

-- ── Conversations ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    channel         TEXT    NOT NULL,
    address         TEXT    NOT NULL,
    started_at      TEXT    NOT NULL,
    last_activity   TEXT    NOT NULL,
    session_active  INTEGER DEFAULT 1,                  -- WhatsApp 24h window flag
    session_expires TEXT,                               -- ISO timestamp
    intent          TEXT,                               -- last detected intent
    sentiment       TEXT,                               -- 'positive' | 'neutral' | 'negative'
    FOREIGN KEY(channel, address) REFERENCES leads(channel, address)
);
CREATE INDEX IF NOT EXISTS idx_conv_channel_address ON conversations(channel, address);

-- ── Messages ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    channel             TEXT    NOT NULL,
    address             TEXT    NOT NULL,
    direction           TEXT    NOT NULL,               -- 'in' | 'out'
    body                TEXT    NOT NULL,
    provider_message_id TEXT,
    intent              TEXT,
    sentiment           TEXT,
    stage_at_send       TEXT,
    created_at          TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_channel_address ON messages(channel, address);
CREATE INDEX IF NOT EXISTS idx_messages_created_at      ON messages(created_at);
"""


class ConversationMemory:
    """
    Async conversation store backed by SQLite.

    All methods are async and safe to call from any asyncio context.
    The db_path is configurable via env var DEALIX_DB (via EngagementSettings).
    """

    def __init__(self, db_path: str = "dealix_engagement.db") -> None:
        self._db_path = str(Path(db_path).expanduser().resolve())
        self._initialized = False

    async def init(self) -> None:
        """Create tables if they do not exist. Call once at startup."""
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self._db_path) as db:
            await db.executescript(_SCHEMA_SQL)
            await db.commit()
        self._initialized = True
        logger.info("ConversationMemory ready at %s", self._db_path)

    async def _ensure_init(self) -> None:
        if not self._initialized:
            await self.init()

    # ── Lead operations ─────────────────────────────────────

    async def upsert_lead(
        self,
        channel: str,
        address: str,
        name: str | None = None,
        company: str | None = None,
        sector: str | None = None,
        city: str | None = None,
        stage: str | None = None,
    ) -> None:
        """Insert or update a lead record."""
        await self._ensure_init()
        now = _now()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                """
                INSERT INTO leads
                    (channel, address, name, company, sector, city, stage,
                     first_seen, last_seen, message_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                ON CONFLICT(channel, address) DO UPDATE SET
                    last_seen     = excluded.last_seen,
                    message_count = leads.message_count + 1,
                    name          = COALESCE(excluded.name,    leads.name),
                    company       = COALESCE(excluded.company, leads.company),
                    sector        = COALESCE(excluded.sector,  leads.sector),
                    city          = COALESCE(excluded.city,    leads.city),
                    stage         = COALESCE(excluded.stage,   leads.stage)
                """,
                (channel, address, name, company, sector, city, stage, now, now),
            )
            await db.commit()

    async def get_lead(
        self, channel: str, address: str
    ) -> dict[str, Any] | None:
        """Fetch a lead record by channel + address."""
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM leads WHERE channel = ? AND address = ?",
                (channel, address),
            )
            row = await cursor.fetchone()
        return dict(row) if row else None

    async def set_opt_out(self, channel: str, address: str) -> None:
        """Mark lead as opted out — PDPL compliance."""
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "UPDATE leads SET opt_in = 0, stage = 'unsubscribed' "
                "WHERE channel = ? AND address = ?",
                (channel, address),
            )
            await db.commit()

    async def update_stage(
        self, channel: str, address: str, stage: str
    ) -> None:
        """Update a lead's pipeline stage."""
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "UPDATE leads SET stage = ?, last_seen = ? "
                "WHERE channel = ? AND address = ?",
                (stage, _now(), channel, address),
            )
            await db.commit()

    async def list_leads(
        self,
        channel: str | None = None,
        stage: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """List leads with optional filters."""
        await self._ensure_init()
        clauses: list[str] = []
        params: list[Any] = []
        if channel:
            clauses.append("channel = ?")
            params.append(channel)
        if stage:
            clauses.append("stage = ?")
            params.append(stage)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        params.append(limit)
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                f"SELECT * FROM leads {where} ORDER BY last_seen DESC LIMIT ?",
                params,
            )
            rows = await cursor.fetchall()
        return [dict(r) for r in rows]

    # ── Message operations ───────────────────────────────────

    async def save_message(
        self,
        channel: str,
        address: str,
        direction: str,                  # 'in' | 'out'
        body: str,
        provider_message_id: str | None = None,
        intent: str | None = None,
        sentiment: str | None = None,
        stage_at_send: str | None = None,
    ) -> int:
        """Persist a single message; return its row ID."""
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO messages
                    (channel, address, direction, body, provider_message_id,
                     intent, sentiment, stage_at_send, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    channel, address, direction, body, provider_message_id,
                    intent, sentiment, stage_at_send, _now(),
                ),
            )
            await db.commit()
            return cursor.lastrowid  # type: ignore[return-value]

    async def get_history(
        self,
        channel: str,
        address: str,
        limit: int = 10,
    ) -> list[dict[str, str]]:
        """
        Return last `limit` messages as OpenAI-style chat history:
          [{"role": "user"|"assistant", "content": "..."}]
        """
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                """
                SELECT direction, body
                FROM messages
                WHERE channel = ? AND address = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (channel, address, limit),
            )
            rows = await cursor.fetchall()

        rows = list(reversed(rows))  # chronological
        return [
            {
                "role": "user" if row[0] == "in" else "assistant",
                "content": row[1],
            }
            for row in rows
        ]

    async def get_raw_messages(
        self,
        channel: str,
        address: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Return full message rows (for analytics / debugging)."""
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT * FROM messages
                WHERE channel = ? AND address = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (channel, address, limit),
            )
            rows = await cursor.fetchall()
        return [dict(r) for r in rows]

    # ── Conversation / session operations ───────────────────

    async def upsert_conversation(
        self,
        channel: str,
        address: str,
        session_active: bool = True,
        session_expires: str | None = None,
        intent: str | None = None,
        sentiment: str | None = None,
    ) -> None:
        """Create or refresh a conversation session record."""
        await self._ensure_init()
        now = _now()
        async with aiosqlite.connect(self._db_path) as db:
            # Try update first
            cursor = await db.execute(
                """
                UPDATE conversations
                SET last_activity   = ?,
                    session_active  = ?,
                    session_expires = COALESCE(?, session_expires),
                    intent          = COALESCE(?, intent),
                    sentiment       = COALESCE(?, sentiment)
                WHERE channel = ? AND address = ?
                """,
                (now, int(session_active), session_expires, intent, sentiment,
                 channel, address),
            )
            if cursor.rowcount == 0:
                await db.execute(
                    """
                    INSERT INTO conversations
                        (channel, address, started_at, last_activity,
                         session_active, session_expires, intent, sentiment)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (channel, address, now, now,
                     int(session_active), session_expires, intent, sentiment),
                )
            await db.commit()

    async def get_conversation(
        self, channel: str, address: str
    ) -> dict[str, Any] | None:
        """Fetch the latest conversation record for a lead."""
        await self._ensure_init()
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT * FROM conversations
                WHERE channel = ? AND address = ?
                ORDER BY id DESC LIMIT 1
                """,
                (channel, address),
            )
            row = await cursor.fetchone()
        return dict(row) if row else None


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

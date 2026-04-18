"""
Dealix — Dashboard Real Backend API
=====================================
FastAPI production service replacing mock.json.

Run:
    uvicorn dashboard_api:app --host 0.0.0.0 --port 8002 --reload

Or via unified main.py (preferred).
"""

from __future__ import annotations

import asyncio
import builtins
import json
import logging
import os
import uuid

builtins_range = builtins.range
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, AsyncGenerator

import aiosqlite
import bcrypt as _bcrypt
import httpx
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger("dealix.dashboard_api")

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
DB_PATH = Path(os.getenv("DEALIX_DB", "/home/user/workspace/dealix-clean/dealix_leads.db"))
JWT_SECRET = os.getenv("JWT_SECRET", "dealix-dev-secret-change-in-prod")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24  # 24 hours
DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

DASHBOARD_CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:8080,http://127.0.0.1:5500"
).split(",")

# ─────────────────────────────────────────────────────────────────────────────
# In-process Event Bus (asyncio.Queue)
# ─────────────────────────────────────────────────────────────────────────────
# Shared event bus — whatsapp_webhook.py publishes here via publish_event()
event_bus: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=1000)


async def publish_event(event_type: str, payload: dict[str, Any], tenant_id: str = DEFAULT_TENANT_ID) -> None:
    """Publish an event to the in-process event bus."""
    event = {
        "type": event_type,
        "payload": payload,
        "tenant_id": tenant_id,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    try:
        event_bus.put_nowait(event)
    except asyncio.QueueFull:
        logger.warning("[event_bus] Queue full, dropping event: %s", event_type)


# ─────────────────────────────────────────────────────────────────────────────
# WebSocket Connection Manager
# ─────────────────────────────────────────────────────────────────────────────
class ConnectionManager:
    def __init__(self) -> None:
        # {tenant_id: [WebSocket, ...]}
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, ws: WebSocket, tenant_id: str) -> None:
        await ws.accept()
        self._connections.setdefault(tenant_id, []).append(ws)
        logger.info("[ws] client connected tenant=%s total=%d", tenant_id, self.count(tenant_id))

    def disconnect(self, ws: WebSocket, tenant_id: str) -> None:
        conns = self._connections.get(tenant_id, [])
        if ws in conns:
            conns.remove(ws)
        logger.info("[ws] client disconnected tenant=%s remaining=%d", tenant_id, len(conns))

    async def broadcast(self, tenant_id: str, message: dict[str, Any]) -> None:
        conns = self._connections.get(tenant_id, [])[:]
        dead: list[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws, tenant_id)

    async def broadcast_all(self, message: dict[str, Any]) -> None:
        for tenant_id in list(self._connections.keys()):
            await self.broadcast(tenant_id, message)

    def count(self, tenant_id: str) -> int:
        return len(self._connections.get(tenant_id, []))


ws_manager = ConnectionManager()


# ─────────────────────────────────────────────────────────────────────────────
# DB Helpers
# ─────────────────────────────────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _trace_id() -> str:
    return str(uuid.uuid4())


async def migrate_db() -> None:
    """Run all DDL migrations. Safe to re-run (IF NOT EXISTS + ALTER TABLE IF NOT EXISTS)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        # ── Drop and recreate leads with full schema (only if it's the old tiny schema) ──
        existing_cols = []
        try:
            cursor = await db.execute("PRAGMA table_info(leads)")
            rows = await cursor.fetchall()
            existing_cols = [r[1] for r in rows]
        except Exception:
            pass

        # If leads table exists but is the old minimal schema, rename and recreate
        if existing_cols and "tenant_id" not in existing_cols:
            logger.info("[db] upgrading legacy leads table schema...")
            await db.execute("ALTER TABLE leads RENAME TO leads_legacy_v1")
            await db.commit()

        # If messages table exists but missing channel/tenant_id, rename it
        msg_cols = []
        try:
            cur = await db.execute("PRAGMA table_info(messages)")
            msg_cols = [r[1] for r in await cur.fetchall()]
        except Exception:
            pass
        if msg_cols and "tenant_id" not in msg_cols:
            logger.info("[db] upgrading legacy messages table schema...")
            await db.execute("ALTER TABLE messages RENAME TO messages_legacy_v1")
            await db.commit()

        # Now create all tables fresh
        await db.executescript("""
        -- Core leads table (full production schema)
        CREATE TABLE IF NOT EXISTS leads (
            id               TEXT    PRIMARY KEY,
            phone            TEXT    UNIQUE,
            name             TEXT,
            company_name     TEXT,
            company_name_ar  TEXT,
            sector           TEXT    NOT NULL DEFAULT 'other',
            city             TEXT,
            employees        INTEGER NOT NULL DEFAULT 0,
            score_total      REAL    NOT NULL DEFAULT 0,
            score_breakdown  TEXT    NOT NULL DEFAULT '{}',
            stage            TEXT    NOT NULL DEFAULT 'new',
            assigned_agent   TEXT,
            value_sar        REAL    NOT NULL DEFAULT 0,
            tenant_id        TEXT    NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
            last_channel     TEXT    NOT NULL DEFAULT 'whatsapp',
            priority_tier    TEXT    NOT NULL DEFAULT 'cold',
            first_seen       TEXT    NOT NULL,
            last_seen        TEXT    NOT NULL,
            message_count    INTEGER NOT NULL DEFAULT 0,
            status           TEXT    NOT NULL DEFAULT 'new',
            website          TEXT,
            revenue_sar      REAL,
            tech_stack       TEXT    NOT NULL DEFAULT '[]',
            contributing_signals TEXT NOT NULL DEFAULT '[]',
            penalizing_factors   TEXT NOT NULL DEFAULT '[]',
            contacts         TEXT    NOT NULL DEFAULT '[]',
            playbook         TEXT,
            days_in_stage    INTEGER NOT NULL DEFAULT 0,
            owner            TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_leads_tenant    ON leads(tenant_id);
        CREATE INDEX IF NOT EXISTS idx_leads_stage     ON leads(stage);
        CREATE INDEX IF NOT EXISTS idx_leads_sector    ON leads(sector);

        -- Messages
        CREATE TABLE IF NOT EXISTS messages (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            phone            TEXT    NOT NULL,
            direction        TEXT    NOT NULL,
            body             TEXT    NOT NULL,
            provider_sid     TEXT,
            channel          TEXT    NOT NULL DEFAULT 'whatsapp',
            tenant_id        TEXT    NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
            created_at       TEXT    NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_messages_phone  ON messages(phone);

        -- Conversations (inbox)
        CREATE TABLE IF NOT EXISTS conversations (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            phone                TEXT    NOT NULL UNIQUE,
            channel              TEXT    NOT NULL DEFAULT 'whatsapp',
            lead_name            TEXT,
            company_name         TEXT,
            last_message_preview TEXT,
            unread_count         INTEGER NOT NULL DEFAULT 0,
            sentiment            TEXT    NOT NULL DEFAULT 'neutral',
            stage                TEXT    NOT NULL DEFAULT 'new',
            tenant_id            TEXT    NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
            created_at           TEXT    NOT NULL,
            updated_at           TEXT    NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_conv_tenant    ON conversations(tenant_id);

        -- Agents
        CREATE TABLE IF NOT EXISTS agents (
            id             TEXT PRIMARY KEY,
            name           TEXT NOT NULL,
            channel        TEXT NOT NULL DEFAULT 'whatsapp',
            status         TEXT NOT NULL DEFAULT 'active',
            msgs_today     INTEGER NOT NULL DEFAULT 0,
            success_rate   REAL NOT NULL DEFAULT 0,
            cost_today     REAL NOT NULL DEFAULT 0,
            last_activity  TEXT,
            tenant_id      TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'
        );
        CREATE INDEX IF NOT EXISTS idx_agents_tenant  ON agents(tenant_id);

        -- Playbooks
        CREATE TABLE IF NOT EXISTS playbooks (
            id           TEXT PRIMARY KEY,
            name         TEXT NOT NULL,
            sector       TEXT,
            steps        TEXT NOT NULL DEFAULT '[]',
            active_count INTEGER NOT NULL DEFAULT 0,
            tenant_id    TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'
        );

        -- Signals
        CREATE TABLE IF NOT EXISTS signals (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id      TEXT,
            category     TEXT,
            text         TEXT NOT NULL,
            score_impact REAL NOT NULL DEFAULT 0,
            source       TEXT,
            tenant_id    TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
            created_at   TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_signals_lead   ON signals(lead_id);

        -- Activities timeline
        CREATE TABLE IF NOT EXISTS activities (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id    TEXT,
            actor      TEXT,
            channel    TEXT,
            action     TEXT NOT NULL,
            meta       TEXT NOT NULL DEFAULT '{}',
            trace_id   TEXT,
            tenant_id  TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_activities_lead   ON activities(lead_id);
        CREATE INDEX IF NOT EXISTS idx_activities_tenant ON activities(tenant_id);

        -- Sources health
        CREATE TABLE IF NOT EXISTS sources_health (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name      TEXT NOT NULL UNIQUE,
            status           TEXT NOT NULL DEFAULT 'unknown',
            records_imported INTEGER NOT NULL DEFAULT 0,
            last_sync        TEXT,
            error            TEXT,
            tenant_id        TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'
        );

        -- Tenants
        CREATE TABLE IF NOT EXISTS tenants (
            id         TEXT PRIMARY KEY,
            name       TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        -- Users
        CREATE TABLE IF NOT EXISTS users (
            id            TEXT PRIMARY KEY,
            tenant_id     TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role          TEXT NOT NULL DEFAULT 'admin',
            api_keys      TEXT NOT NULL DEFAULT '{}'
        );
        CREATE INDEX IF NOT EXISTS idx_users_tenant ON users(tenant_id);
        """)
        await db.commit()
    logger.info("[db] migrations complete at %s", DB_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────────────────────
security = HTTPBearer(auto_error=False)


def hash_password(pw: str) -> str:
    return _bcrypt.hashpw(pw.encode(), _bcrypt.gensalt()).decode()


def verify_password(pw: str, hashed: str) -> bool:
    try:
        return _bcrypt.checkpw(pw.encode(), hashed.encode())
    except Exception:
        return False


def create_token(user_id: str, tenant_id: str, email: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": user_id, "tenant_id": tenant_id, "email": email, "role": role, "exp": expire},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    try:
        payload = decode_token(credentials.credentials)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    return payload


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Response Models
# ─────────────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error: str
    code: str
    trace_id: str


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str
    db: str
    timestamp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    tenant_id: str
    user_id: str
    email: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LeadListItem(BaseModel):
    id: str
    company_name: str
    company_name_ar: str | None = None
    sector: str
    city: str | None = None
    employees: int
    score_total: float
    priority_tier: str
    stage: str
    assigned_agent: str | None = None
    value_sar: float
    last_channel: str
    last_seen: str
    days_in_stage: int
    tenant_id: str


class LeadDetail(BaseModel):
    id: str
    company_name: str
    company_name_ar: str | None = None
    sector: str
    city: str | None = None
    employees: int
    score_total: float
    score_breakdown: dict[str, Any]
    priority_tier: str
    stage: str
    assigned_agent: str | None = None
    value_sar: float
    last_channel: str
    last_seen: str
    days_in_stage: int
    website: str | None = None
    revenue_sar: float | None = None
    tech_stack: list[str]
    contributing_signals: list[str]
    penalizing_factors: list[str]
    contacts: list[dict[str, Any]]
    signals: list[dict[str, Any]]
    timeline: list[dict[str, Any]]
    playbook: str | None = None
    owner: str | None = None
    tenant_id: str


class LeadPatch(BaseModel):
    stage: str | None = None
    assigned_agent: str | None = None
    value_sar: float | None = None
    owner: str | None = None


class ConversationItem(BaseModel):
    id: int
    phone: str
    channel: str
    lead_name: str | None = None
    company_name: str | None = None
    last_message_preview: str | None = None
    unread_count: int
    sentiment: str
    stage: str
    updated_at: str


class MessageItem(BaseModel):
    id: int
    phone: str
    direction: str
    body: str
    channel: str
    created_at: str


class ReplyRequest(BaseModel):
    channel: str = "whatsapp"
    body: str


class AISuggestResponse(BaseModel):
    suggestions: list[str]


class PipelineColumn(BaseModel):
    stage: str
    label: str
    count: int
    value_sar: float
    leads: list[LeadListItem]


class AgentItem(BaseModel):
    id: str
    name: str
    channel: str
    status: str
    msgs_today: int
    success_rate: float
    cost_today: float
    last_activity: str | None = None


class PlaybookItem(BaseModel):
    id: str
    name: str
    sector: str | None = None
    steps: list[dict[str, Any]]
    active_count: int


class SourceItem(BaseModel):
    source_name: str
    status: str
    records_imported: int
    last_sync: str | None = None
    error: str | None = None


class MRRDataPoint(BaseModel):
    date: str
    value: float


class ConversionData(BaseModel):
    channel: str
    sent: int
    replied: int
    qualified: int
    rate: float


class AgentROIItem(BaseModel):
    id: str
    name: str
    channel: str
    leads_touched: int
    deals_closed: int
    revenue_sar: float
    cost_sar: float
    roi: float


class OverviewResponse(BaseModel):
    kpis: dict[str, Any]
    funnel: list[dict[str, Any]]
    recent_activity: list[dict[str, Any]]
    channel_performance: list[dict[str, Any]]


class SettingsMe(BaseModel):
    user_id: str
    email: str
    role: str
    tenant_id: str
    tenant_name: str
    api_keys: dict[str, str]


class ApiKeysRequest(BaseModel):
    groq_key: str | None = None
    twilio_sid: str | None = None
    twilio_token: str | None = None
    sendgrid_key: str | None = None


class StageMove(BaseModel):
    stage: str


class AgentToggleResponse(BaseModel):
    id: str
    status: str


# ─────────────────────────────────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Dealix Dashboard API",
    version="1.0.0",
    description="Production backend for the Dealix sales intelligence dashboard.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=DASHBOARD_CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_trace_id(request, call_next):
    trace_id = request.headers.get("X-Trace-ID", _trace_id())
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Service"] = "dealix-dashboard-api"
    return response


@app.on_event("startup")
async def startup():
    await migrate_db()
    # Start event bus broadcaster
    asyncio.create_task(_event_broadcaster())
    logger.info("[startup] Dashboard API ready")


async def _event_broadcaster():
    """Drain the event bus and broadcast to all connected WS clients."""
    while True:
        try:
            event = await asyncio.wait_for(event_bus.get(), timeout=1.0)
            tenant_id = event.get("tenant_id", DEFAULT_TENANT_ID)
            await ws_manager.broadcast(tenant_id, event)
        except asyncio.TimeoutError:
            continue
        except Exception as e:
            logger.warning("[event_broadcaster] error: %s", e)


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

# ── Health ───────────────────────────────────────────────────────────────────
@app.get("/api/v1/health", response_model=HealthResponse, tags=["meta"])
async def health():
    db_ok = "ok"
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("SELECT 1")
    except Exception as e:
        db_ok = f"error: {e}"
    return HealthResponse(
        service="dealix-dashboard-api",
        status="ok" if db_ok == "ok" else "degraded",
        version="1.0.0",
        db=db_ok,
        timestamp=_now(),
    )


# ── Auth ─────────────────────────────────────────────────────────────────────
@app.post("/api/v1/auth/login", response_model=TokenResponse, tags=["auth"])
async def login(body: LoginRequest):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute(
            "SELECT * FROM users WHERE email = ?", (body.email,)
        )).fetchone()

    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(row["id"], row["tenant_id"], row["email"], row["role"])
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        tenant_id=row["tenant_id"],
        user_id=row["id"],
        email=row["email"],
        role=row["role"],
    )


# ── Overview ─────────────────────────────────────────────────────────────────
@app.get("/api/v1/overview", response_model=OverviewResponse, tags=["overview"])
async def overview(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        # KPIs
        total_leads = (await (await db.execute(
            "SELECT COUNT(*) FROM leads WHERE tenant_id=?", (tid,)
        )).fetchone())[0]

        hot_leads = (await (await db.execute(
            "SELECT COUNT(*) FROM leads WHERE tenant_id=? AND priority_tier='hot'", (tid,)
        )).fetchone())[0]

        pipeline_value = (await (await db.execute(
            "SELECT COALESCE(SUM(value_sar),0) FROM leads WHERE tenant_id=? AND stage NOT IN ('closed_lost','disqualified')", (tid,)
        )).fetchone())[0]

        won_value = (await (await db.execute(
            "SELECT COALESCE(SUM(value_sar),0) FROM leads WHERE tenant_id=? AND stage='closed_won'", (tid,)
        )).fetchone())[0]

        total_msgs = (await (await db.execute(
            "SELECT COUNT(*) FROM messages WHERE tenant_id=?", (tid,)
        )).fetchone())[0]

        active_agents = (await (await db.execute(
            "SELECT COUNT(*) FROM agents WHERE tenant_id=? AND status='active'", (tid,)
        )).fetchone())[0]

        # Funnel
        stages = ["new", "enriching", "qualified", "contacted", "meeting", "proposal", "negotiation", "closed_won"]
        funnel = []
        for s in stages:
            cnt = (await (await db.execute(
                "SELECT COUNT(*) FROM leads WHERE tenant_id=? AND stage=?", (tid, s)
            )).fetchone())[0]
            funnel.append({"stage": s, "count": cnt})

        # Recent activity (last 10)
        act_rows = await (await db.execute(
            "SELECT * FROM activities WHERE tenant_id=? ORDER BY created_at DESC LIMIT 10", (tid,)
        )).fetchall()
        recent_activity = [dict(r) for r in act_rows]

        # Channel performance from messages
        ch_rows = await (await db.execute(
            "SELECT channel, COUNT(*) as total, SUM(CASE WHEN direction='in' THEN 1 ELSE 0 END) as replies "
            "FROM messages WHERE tenant_id=? GROUP BY channel", (tid,)
        )).fetchall()
        channel_perf = []
        for r in ch_rows:
            total = r["total"] or 1
            replies = r["replies"] or 0
            channel_perf.append({
                "channel": r["channel"],
                "messages": total,
                "replies": replies,
                "reply_rate": round(replies / total * 100, 1),
            })

    return OverviewResponse(
        kpis={
            "total_leads": total_leads,
            "hot_leads": hot_leads,
            "pipeline_value_sar": round(pipeline_value, 2),
            "won_value_sar": round(won_value, 2),
            "total_messages": total_msgs,
            "active_agents": active_agents,
        },
        funnel=funnel,
        recent_activity=recent_activity,
        channel_performance=channel_perf,
    )


# ── Leads ────────────────────────────────────────────────────────────────────
@app.get("/api/v1/leads", tags=["leads"])
async def list_leads(
    search: str | None = Query(None),
    sector: str | None = Query(None),
    stage: str | None = Query(None),
    tier: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user=Depends(get_current_user),
):
    tid = user["tenant_id"]
    clauses = ["tenant_id = ?"]
    params: list[Any] = [tid]

    if search:
        clauses.append("(company_name LIKE ? OR company_name_ar LIKE ? OR name LIKE ?)")
        like = f"%{search}%"
        params += [like, like, like]
    if sector:
        clauses.append("sector = ?")
        params.append(sector)
    if stage:
        clauses.append("stage = ?")
        params.append(stage)
    if tier:
        clauses.append("priority_tier = ?")
        params.append(tier)

    where = "WHERE " + " AND ".join(clauses)
    count_q = f"SELECT COUNT(*) FROM leads {where}"
    data_q = f"SELECT * FROM leads {where} ORDER BY score_total DESC LIMIT ? OFFSET ?"

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        total = (await (await db.execute(count_q, params)).fetchone())[0]
        rows = await (await db.execute(data_q, params + [limit, offset])).fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "company_name": r["company_name"] or "",
            "company_name_ar": r["company_name_ar"],
            "sector": r["sector"],
            "city": r["city"],
            "employees": r["employees"] or 0,
            "score_total": r["score_total"] or 0,
            "priority_tier": r["priority_tier"] or "cold",
            "stage": r["stage"],
            "assigned_agent": r["assigned_agent"],
            "value_sar": r["value_sar"] or 0,
            "last_channel": r["last_channel"] or "whatsapp",
            "last_seen": r["last_seen"],
            "days_in_stage": r["days_in_stage"] or 0,
            "tenant_id": r["tenant_id"],
        })

    return {"total": total, "limit": limit, "offset": offset, "items": items}


@app.get("/api/v1/leads/{lead_id}", tags=["leads"])
async def get_lead(lead_id: str, user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute(
            "SELECT * FROM leads WHERE id=? AND tenant_id=?", (lead_id, tid)
        )).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Signals
        sig_rows = await (await db.execute(
            "SELECT * FROM signals WHERE lead_id=? ORDER BY created_at DESC LIMIT 20", (lead_id,)
        )).fetchall()

        # Activities / timeline
        act_rows = await (await db.execute(
            "SELECT * FROM activities WHERE lead_id=? ORDER BY created_at DESC LIMIT 30", (lead_id,)
        )).fetchall()

    r = dict(row)
    return {
        "id": r["id"],
        "company_name": r["company_name"] or "",
        "company_name_ar": r["company_name_ar"],
        "sector": r["sector"],
        "city": r["city"],
        "employees": r["employees"] or 0,
        "score_total": r["score_total"] or 0,
        "score_breakdown": json.loads(r["score_breakdown"] or "{}"),
        "priority_tier": r["priority_tier"] or "cold",
        "stage": r["stage"],
        "assigned_agent": r["assigned_agent"],
        "value_sar": r["value_sar"] or 0,
        "last_channel": r["last_channel"] or "whatsapp",
        "last_seen": r["last_seen"],
        "days_in_stage": r["days_in_stage"] or 0,
        "website": r["website"],
        "revenue_sar": r["revenue_sar"],
        "tech_stack": json.loads(r["tech_stack"] or "[]"),
        "contributing_signals": json.loads(r["contributing_signals"] or "[]"),
        "penalizing_factors": json.loads(r["penalizing_factors"] or "[]"),
        "contacts": json.loads(r["contacts"] or "[]"),
        "signals": [dict(s) for s in sig_rows],
        "timeline": [dict(a) for a in act_rows],
        "playbook": r["playbook"],
        "owner": r["owner"],
        "tenant_id": r["tenant_id"],
    }


@app.patch("/api/v1/leads/{lead_id}", tags=["leads"])
async def update_lead(lead_id: str, body: LeadPatch, user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute(
            "SELECT * FROM leads WHERE id=? AND tenant_id=?", (lead_id, tid)
        )).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lead not found")

        updates: dict[str, Any] = {}
        if body.stage is not None:
            updates["stage"] = body.stage
            updates["days_in_stage"] = 0
        if body.assigned_agent is not None:
            updates["assigned_agent"] = body.assigned_agent
        if body.value_sar is not None:
            updates["value_sar"] = body.value_sar
        if body.owner is not None:
            updates["owner"] = body.owner

        if updates:
            set_clause = ", ".join(f"{k}=?" for k in updates)
            vals = list(updates.values()) + [lead_id, tid]
            await db.execute(f"UPDATE leads SET {set_clause} WHERE id=? AND tenant_id=?", vals)

            # Log activity
            trace = _trace_id()
            for field, val in updates.items():
                await db.execute(
                    "INSERT INTO activities (lead_id, actor, channel, action, meta, trace_id, tenant_id, created_at) "
                    "VALUES (?,?,?,?,?,?,?,?)",
                    (lead_id, user["email"], "dashboard", f"updated_{field}",
                     json.dumps({"field": field, "value": str(val)}), trace, tid, _now())
                )
            await db.commit()

        updated = dict(await (await db.execute(
            "SELECT * FROM leads WHERE id=?", (lead_id,)
        )).fetchone())

    # Broadcast event
    await publish_event("lead.updated", {"lead_id": lead_id, "updates": updates}, tid)
    return updated


# ── Pipeline ─────────────────────────────────────────────────────────────────
STAGE_LABELS = {
    "new": "جديد",
    "enriching": "إثراء",
    "qualified": "مؤهّل",
    "contacted": "تواصل",
    "meeting": "اجتماع",
    "proposal": "عرض",
    "negotiation": "تفاوض",
    "closed_won": "فاز",
    "closed_lost": "خسر",
}


@app.get("/api/v1/pipeline", tags=["pipeline"])
async def pipeline(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    stages = list(STAGE_LABELS.keys())
    columns = []
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        for s in stages:
            rows = await (await db.execute(
                "SELECT * FROM leads WHERE tenant_id=? AND stage=? ORDER BY score_total DESC LIMIT 50",
                (tid, s)
            )).fetchall()
            leads_list = []
            total_val = 0.0
            for r in rows:
                total_val += r["value_sar"] or 0
                leads_list.append({
                    "id": r["id"],
                    "company_name": r["company_name"] or "",
                    "company_name_ar": r["company_name_ar"],
                    "sector": r["sector"],
                    "city": r["city"],
                    "employees": r["employees"] or 0,
                    "score_total": r["score_total"] or 0,
                    "priority_tier": r["priority_tier"] or "cold",
                    "stage": r["stage"],
                    "assigned_agent": r["assigned_agent"],
                    "value_sar": r["value_sar"] or 0,
                    "last_channel": r["last_channel"] or "whatsapp",
                    "last_seen": r["last_seen"],
                    "days_in_stage": r["days_in_stage"] or 0,
                    "tenant_id": r["tenant_id"],
                })
            columns.append({
                "stage": s,
                "label": STAGE_LABELS[s],
                "count": len(leads_list),
                "value_sar": round(total_val, 2),
                "leads": leads_list,
            })
    return {"columns": columns}


@app.post("/api/v1/leads/{lead_id}/stage", tags=["pipeline"])
async def move_stage(lead_id: str, body: StageMove, user=Depends(get_current_user)):
    return await update_lead(lead_id, LeadPatch(stage=body.stage), user)


# ── Conversations ─────────────────────────────────────────────────────────────
@app.get("/api/v1/conversations", tags=["conversations"])
async def list_conversations(
    channel: str | None = Query(None),
    user=Depends(get_current_user),
):
    tid = user["tenant_id"]
    clauses = ["c.tenant_id = ?"]
    params: list[Any] = [tid]
    if channel:
        clauses.append("c.channel = ?")
        params.append(channel)

    where = " AND ".join(clauses)
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            f"SELECT * FROM conversations c WHERE {where} ORDER BY updated_at DESC LIMIT 100",
            params
        )).fetchall()

    return {"items": [dict(r) for r in rows]}


@app.get("/api/v1/conversations/{phone}/messages", tags=["conversations"])
async def get_messages(phone: str, user=Depends(get_current_user)):
    tid = user["tenant_id"]
    # Mark as read
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE conversations SET unread_count=0, updated_at=? WHERE phone=? AND tenant_id=?",
            (_now(), phone, tid)
        )
        await db.commit()

        rows = await (await db.execute(
            "SELECT * FROM messages WHERE phone=? AND tenant_id=? ORDER BY created_at ASC",
            (phone, tid)
        )).fetchall()

    return {"phone": phone, "messages": [dict(r) for r in rows]}


@app.post("/api/v1/conversations/{phone}/reply", tags=["conversations"])
async def reply_message(phone: str, body: ReplyRequest, user=Depends(get_current_user)):
    """Send a real message via Twilio (WhatsApp) or log it; save to DB."""
    tid = user["tenant_id"]
    trace = _trace_id()
    provider_sid = None
    error_msg = None

    if body.channel == "whatsapp" and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        to_wa = f"whatsapp:{phone}" if not phone.startswith("whatsapp:") else phone
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
                    auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                    data={
                        "From": TWILIO_WHATSAPP_FROM,
                        "To": to_wa,
                        "Body": body.body,
                    },
                )
                if r.status_code in (200, 201):
                    provider_sid = r.json().get("sid")
                else:
                    error_msg = f"Twilio error {r.status_code}: {r.text[:200]}"
        except Exception as e:
            error_msg = str(e)
    elif not TWILIO_ACCOUNT_SID:
        # dry-run mode
        provider_sid = f"dry-run-{trace}"

    # Save outbound message
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "INSERT INTO messages (phone, direction, body, provider_sid, channel, tenant_id, created_at) "
            "VALUES (?,?,?,?,?,?,?)",
            (phone, "out", body.body, provider_sid, body.channel, tid, _now())
        )
        msg_id = cursor.lastrowid
        await db.execute(
            "UPDATE conversations SET last_message_preview=?, updated_at=? WHERE phone=? AND tenant_id=?",
            (body.body[:100], _now(), phone, tid)
        )
        await db.commit()

        msg_row = dict(await (await db.execute(
            "SELECT * FROM messages WHERE id=?", (msg_id,)
        )).fetchone())

    await publish_event("message.new", {"message": msg_row, "phone": phone}, tid)

    if error_msg:
        return JSONResponse(
            status_code=207,
            content={"message": msg_row, "warning": error_msg, "trace_id": trace}
        )
    return {"message": msg_row, "provider_sid": provider_sid, "trace_id": trace}


@app.post("/api/v1/conversations/{phone}/ai-suggest", tags=["conversations"])
async def ai_suggest(phone: str, user=Depends(get_current_user)):
    """Generate 3 AI-suggested replies in Arabic (Gulf dialect) using Groq."""
    tid = user["tenant_id"]

    # Get last 10 messages for context
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT direction, body FROM messages WHERE phone=? AND tenant_id=? ORDER BY id DESC LIMIT 10",
            (phone, tid)
        )).fetchall()

    history = []
    for r in reversed(rows):
        role = "user" if r["direction"] == "in" else "assistant"
        history.append({"role": role, "content": r["body"]})

    if not GROQ_API_KEY:
        return AISuggestResponse(suggestions=[
            "شكراً لتواصلك، سنرد عليك قريباً.",
            "يسعدنا خدمتك، هل يمكنك مشاركة متطلباتك؟",
            "نشكر اهتمامك، دعنا نحدد موعداً مناسباً."
        ])

    system = """أنت مساعد مبيعات لمنصة Dealix. مهمتك اقتراح 3 ردود مختصرة ومناسبة باللهجة الخليجية.
الردود يجب أن:
1. تكون مناسبة للسياق
2. باللغة العربية، لهجة خليجية مهذبة
3. قصيرة (2-3 أسطر)
4. تهدف إلى تأهيل العميل أو تحديد موعد

أعد فقط قائمة JSON بصيغة: {"suggestions": ["رد 1", "رد 2", "رد 3"]}
لا تضف أي نص آخر."""

    messages = [{"role": "system", "content": system}]
    messages.extend(history)
    messages.append({"role": "user", "content": "اقترح 3 ردود مناسبة بصيغة JSON."})

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                GROQ_URL,
                json={"model": GROQ_MODEL, "messages": messages, "temperature": 0.7, "max_tokens": 400},
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            )
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"].strip()
            # Parse JSON from response
            data = json.loads(content)
            suggestions = data.get("suggestions", [])[:3]
            while len(suggestions) < 3:
                suggestions.append("كيف يمكنني مساعدتك؟")
    except Exception as e:
        logger.warning("[ai-suggest] error: %s", e)
        suggestions = [
            "شكراً لتواصلك، سنرد عليك قريباً.",
            "يسعدنا خدمتك، هل يمكنك مشاركة متطلباتك؟",
            "نشكر اهتمامك، دعنا نحدد موعداً مناسباً.",
        ]

    return AISuggestResponse(suggestions=suggestions)


# ── Agents ────────────────────────────────────────────────────────────────────
@app.get("/api/v1/agents", tags=["agents"])
async def list_agents(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM agents WHERE tenant_id=? ORDER BY name", (tid,)
        )).fetchall()
    return {"items": [dict(r) for r in rows]}


@app.post("/api/v1/agents/{agent_id}/toggle", response_model=AgentToggleResponse, tags=["agents"])
async def toggle_agent(agent_id: str, user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute(
            "SELECT * FROM agents WHERE id=? AND tenant_id=?", (agent_id, tid)
        )).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Agent not found")
        new_status = "paused" if row["status"] == "active" else "active"
        await db.execute(
            "UPDATE agents SET status=?, last_activity=? WHERE id=? AND tenant_id=?",
            (new_status, _now(), agent_id, tid)
        )
        await db.commit()

    await publish_event("agent.status", {"agent_id": agent_id, "status": new_status}, tid)
    return AgentToggleResponse(id=agent_id, status=new_status)


# ── Playbooks ─────────────────────────────────────────────────────────────────
@app.get("/api/v1/playbooks", tags=["playbooks"])
async def list_playbooks(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM playbooks WHERE tenant_id=?", (tid,)
        )).fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "name": r["name"],
            "sector": r["sector"],
            "steps": json.loads(r["steps"] or "[]"),
            "active_count": r["active_count"] or 0,
        })
    return {"items": items}


# ── Sources ───────────────────────────────────────────────────────────────────
@app.get("/api/v1/sources", tags=["sources"])
async def list_sources(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM sources_health WHERE tenant_id=?", (tid,)
        )).fetchall()
    return {"items": [dict(r) for r in rows]}


@app.post("/api/v1/sources/{source_name}/discover", tags=["sources"])
async def discover_source(
    source_name: str,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
):
    tid = user["tenant_id"]
    background_tasks.add_task(_run_discovery, source_name, tid)
    return {"status": "discovery_started", "source": source_name, "trace_id": _trace_id()}


async def _run_discovery(source_name: str, tenant_id: str) -> None:
    """Background discovery stub — logs and updates sources_health."""
    logger.info("[discovery] starting source=%s tenant=%s", source_name, tenant_id)
    try:
        # Update to running
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE sources_health SET status='running', last_sync=? WHERE source_name=? AND tenant_id=?",
                (_now(), source_name, tenant_id)
            )
            await db.commit()

        # Simulate discovery (stub — real impl would call intelligence orchestrator)
        await asyncio.sleep(2)

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE sources_health SET status='ok', last_sync=? WHERE source_name=? AND tenant_id=?",
                (_now(), source_name, tenant_id)
            )
            await db.commit()

        await publish_event("source.discovered", {"source": source_name}, tenant_id)
    except Exception as e:
        logger.error("[discovery] error source=%s: %s", source_name, e)
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE sources_health SET status='error', error=? WHERE source_name=? AND tenant_id=?",
                (str(e), source_name, tenant_id)
            )
            await db.commit()


# ── Analytics ─────────────────────────────────────────────────────────────────
@app.get("/api/v1/analytics/mrr", tags=["analytics"])
async def analytics_mrr(
    range: str = Query("30d", alias="range"),
    user=Depends(get_current_user),
):
    tid = user["tenant_id"]
    _range = range  # avoid shadowing builtin
    days = 30
    if _range == "7d":
        days = 7
    elif _range == "90d":
        days = 90

    # Build daily MRR series from closed_won leads
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            """
            SELECT DATE(last_seen) as day, SUM(value_sar) as daily_value
            FROM leads
            WHERE tenant_id=? AND stage='closed_won'
              AND last_seen >= datetime('now', ?)
            GROUP BY DATE(last_seen)
            ORDER BY day ASC
            """,
            (tid, f"-{days} days")
        )).fetchall()

    # Fill missing days with 0
    series: dict[str, float] = {}
    for r in rows:
        series[r["day"]] = r["daily_value"] or 0

    result = []
    for i in builtins_range(days):
        d = (datetime.now(timezone.utc) - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
        result.append({"date": d, "value": series.get(d, 0)})

    return {"range": _range, "series": result}


@app.get("/api/v1/analytics/conversion", tags=["analytics"])
async def analytics_conversion(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            """
            SELECT last_channel as channel,
                   COUNT(*) as total,
                   SUM(CASE WHEN stage IN ('contacted','meeting','proposal','negotiation','closed_won') THEN 1 ELSE 0 END) as replied,
                   SUM(CASE WHEN stage IN ('qualified','meeting','proposal','negotiation','closed_won') THEN 1 ELSE 0 END) as qualified
            FROM leads
            WHERE tenant_id=?
            GROUP BY last_channel
            """,
            (tid,)
        )).fetchall()

    result = []
    for r in rows:
        total = r["total"] or 1
        result.append({
            "channel": r["channel"] or "whatsapp",
            "sent": total,
            "replied": r["replied"] or 0,
            "qualified": r["qualified"] or 0,
            "rate": round((r["qualified"] or 0) / total * 100, 1),
        })
    return {"items": result}


@app.get("/api/v1/analytics/agent-roi", tags=["analytics"])
async def analytics_agent_roi(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        agents = await (await db.execute(
            "SELECT * FROM agents WHERE tenant_id=?", (tid,)
        )).fetchall()

        result = []
        for a in agents:
            # Count leads touched by this agent
            touched = (await (await db.execute(
                "SELECT COUNT(*) FROM leads WHERE tenant_id=? AND assigned_agent=?",
                (tid, a["name"])
            )).fetchone())[0]

            won = (await (await db.execute(
                "SELECT COUNT(*), COALESCE(SUM(value_sar),0) FROM leads "
                "WHERE tenant_id=? AND assigned_agent=? AND stage='closed_won'",
                (tid, a["name"])
            )).fetchone())
            deals_closed = won[0] or 0
            revenue = won[1] or 0
            cost = (a["cost_today"] or 0) * 30  # estimated monthly cost
            roi = round((revenue - cost) / max(cost, 1) * 100, 1) if cost > 0 else 0

            result.append({
                "id": a["id"],
                "name": a["name"],
                "channel": a["channel"],
                "leads_touched": touched,
                "deals_closed": deals_closed,
                "revenue_sar": round(revenue, 2),
                "cost_sar": round(cost, 2),
                "roi": roi,
            })

    return {"items": result}


# ── Settings ──────────────────────────────────────────────────────────────────
@app.get("/api/v1/settings/me", response_model=SettingsMe, tags=["settings"])
async def settings_me(user=Depends(get_current_user)):
    tid = user["tenant_id"]
    uid = user["sub"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        u_row = await (await db.execute(
            "SELECT * FROM users WHERE id=?", (uid,)
        )).fetchone()
        t_row = await (await db.execute(
            "SELECT * FROM tenants WHERE id=?", (tid,)
        )).fetchone()

    if not u_row:
        raise HTTPException(status_code=404, detail="User not found")

    api_keys_raw = json.loads(u_row["api_keys"] or "{}")
    # Mask all keys
    masked = {k: f"***{v[-4:]}" if len(v) > 4 else "***" for k, v in api_keys_raw.items()}

    return SettingsMe(
        user_id=u_row["id"],
        email=u_row["email"],
        role=u_row["role"],
        tenant_id=tid,
        tenant_name=t_row["name"] if t_row else "Unknown",
        api_keys=masked,
    )


@app.post("/api/v1/settings/api-keys", tags=["settings"])
async def update_api_keys(body: ApiKeysRequest, user=Depends(get_current_user)):
    uid = user["sub"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        u_row = await (await db.execute(
            "SELECT api_keys FROM users WHERE id=?", (uid,)
        )).fetchone()
        if not u_row:
            raise HTTPException(status_code=404, detail="User not found")

        keys = json.loads(u_row["api_keys"] or "{}")
        if body.groq_key:
            keys["groq"] = body.groq_key
        if body.twilio_sid:
            keys["twilio_sid"] = body.twilio_sid
        if body.twilio_token:
            keys["twilio_token"] = body.twilio_token
        if body.sendgrid_key:
            keys["sendgrid"] = body.sendgrid_key

        await db.execute(
            "UPDATE users SET api_keys=? WHERE id=?",
            (json.dumps(keys), uid)
        )
        await db.commit()

    return {"status": "updated", "keys_stored": list(keys.keys())}


# ── WebSocket ─────────────────────────────────────────────────────────────────
@app.websocket("/api/v1/ws")
async def websocket_endpoint(ws: WebSocket, tenant_id: str = DEFAULT_TENANT_ID, token: str = ""):
    # Optional token validation
    if token:
        try:
            payload = decode_token(token)
            tenant_id = payload.get("tenant_id", tenant_id)
        except JWTError:
            await ws.close(code=4001, reason="Invalid token")
            return

    await ws_manager.connect(ws, tenant_id)
    try:
        # Send connected acknowledgment
        await ws.send_json({
            "type": "connected",
            "payload": {"tenant_id": tenant_id},
            "ts": _now(),
        })
        # Keep alive — receive ping/pong or disconnect
        while True:
            try:
                data = await asyncio.wait_for(ws.receive_json(), timeout=30.0)
                if data.get("type") == "ping":
                    await ws.send_json({"type": "pong", "ts": _now()})
            except asyncio.TimeoutError:
                await ws.send_json({"type": "heartbeat", "ts": _now()})
    except WebSocketDisconnect:
        pass
    finally:
        ws_manager.disconnect(ws, tenant_id)

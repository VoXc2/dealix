"""
Dealix — WhatsApp Webhook (Standalone, Arabic-first)
====================================================
Minimal FastAPI app to:
  1. Receive incoming WhatsApp messages from Twilio Sandbox
  2. Generate an Arabic reply via Groq (llama-3.3-70b-versatile)
  3. Save the lead + conversation to SQLite
  4. Return TwiML response so Twilio sends the reply

Run locally:
    cd dealix-clean/backend
    uvicorn whatsapp_webhook:app --host 0.0.0.0 --port 8001

Then expose via Cloudflare Tunnel:
    cloudflared tunnel --url http://localhost:8001

Then paste the public URL + /webhook/whatsapp into Twilio Sandbox.
"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, JSONResponse

# ────────────────────────────────────────────────────────────────
# Configuration (from env)
# ────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

DB_PATH = Path(os.getenv("DEALIX_DB", "/home/user/workspace/dealix-clean/dealix_leads.db"))

SYSTEM_PROMPT = """أنت مساعد مبيعات ذكي لمنصة Dealix (ديلكس) — منصة سعودية تستخدم AI Agents لتحويل المحادثات إلى صفقات مكتملة عبر WhatsApp.

قواعد صارمة:
- رد بالعربي الفصيح المبسّط بلهجة خليجية مهذبة.
- لا تزعم أي ادعاءات غير مؤكدة (مثل "معتمد ISO" أو "نسبة نجاح 100%") — ديلكس في مرحلة التدشين.
- كن مختصراً: 2-4 أسطر كحد أقصى في كل رد.
- اسأل سؤالاً واحداً كل مرة لتأهيل العميل: اسمه، مجال شركته، حجمها، أو مشكلته.
- إذا طلب العميل تسعير: اشرح أن ديلكس يقدم تجربة تجريبية مجانية، واطلب تواصله.
- نهاية المحادثة: لخّص واطلب موعد مكالمة.

أسلوبك: ودود، واثق، غير مندفع. لا emojis أكثر من 1 كل رد."""

# ────────────────────────────────────────────────────────────────
# SQLite — leads store
# ────────────────────────────────────────────────────────────────
def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE NOT NULL,
        name TEXT,
        first_seen TEXT NOT NULL,
        last_seen TEXT NOT NULL,
        message_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'new'
    );
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT NOT NULL,
        direction TEXT NOT NULL,  -- 'in' | 'out'
        body TEXT NOT NULL,
        provider_sid TEXT,
        created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_messages_phone ON messages(phone);
    """)
    con.commit()
    con.close()


def upsert_lead(phone: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        INSERT INTO leads (phone, first_seen, last_seen, message_count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(phone) DO UPDATE SET
            last_seen = excluded.last_seen,
            message_count = leads.message_count + 1
    """, (phone, now, now))
    con.commit()
    con.close()


def save_message(phone: str, direction: str, body: str, sid: str | None = None) -> None:
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO messages (phone, direction, body, provider_sid, created_at) VALUES (?, ?, ?, ?, ?)",
        (phone, direction, body, sid, datetime.now(timezone.utc).isoformat()),
    )
    con.commit()
    con.close()


def get_history(phone: str, limit: int = 10) -> list[dict[str, str]]:
    """Return last N messages as chat format for LLM context."""
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT direction, body FROM messages WHERE phone = ? ORDER BY id DESC LIMIT ?",
        (phone, limit),
    ).fetchall()
    con.close()
    # reverse to chronological
    rows.reverse()
    history = []
    for direction, body in rows:
        role = "user" if direction == "in" else "assistant"
        history.append({"role": role, "content": body})
    return history


# ────────────────────────────────────────────────────────────────
# Groq LLM call
# ────────────────────────────────────────────────────────────────
async def groq_reply(user_message: str, history: list[dict[str, str]]) -> str:
    if not GROQ_API_KEY:
        return "مرحباً — نظامنا في وضع الصيانة مؤقتاً. سنتواصل معك قريباً."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    # ensure latest user message is present
    if not history or history[-1].get("content") != user_message:
        messages.append({"role": "user", "content": user_message})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 300,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(GROQ_URL, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:  # noqa: BLE001
        print(f"[groq] error: {e}")
        return "مرحباً، شكراً لتواصلك مع Dealix. سيرد عليك مختص بأقرب وقت."


# ────────────────────────────────────────────────────────────────
# FastAPI app
# ────────────────────────────────────────────────────────────────
app = FastAPI(title="Dealix WhatsApp Webhook", version="0.1.0")


@app.on_event("startup")
def _startup() -> None:
    init_db()
    print(f"[dealix] DB ready at {DB_PATH}")
    print(f"[dealix] Groq key present: {bool(GROQ_API_KEY)}")


@app.get("/")
def health() -> dict[str, Any]:
    return {"service": "dealix-whatsapp-webhook", "status": "ok"}


@app.get("/leads")
def leads() -> JSONResponse:
    """List all collected leads (for debugging — protect in prod)."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT * FROM leads ORDER BY last_seen DESC LIMIT 100"
    ).fetchall()
    con.close()
    return JSONResponse([dict(r) for r in rows])


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str | None = Form(None),
    ProfileName: str | None = Form(None),
):
    """
    Twilio Sandbox calls this when a user sends a WhatsApp message.
    We reply synchronously via TwiML so the user sees the response immediately.
    """
    # Normalize phone — ensure single leading '+' and no whitespace
    raw = From.replace("whatsapp:", "").strip()
    digits = "".join(c for c in raw if c.isdigit())
    phone = f"+{digits}" if digits else raw
    user_msg = Body.strip()
    print(f"[inbound] {phone} ({ProfileName}): {user_msg!r}")

    # persist
    upsert_lead(phone)
    save_message(phone, "in", user_msg, MessageSid)

    # build reply
    history = get_history(phone, limit=10)
    reply = await groq_reply(user_msg, history)
    save_message(phone, "out", reply, None)

    # return TwiML — Twilio will send this as the WhatsApp reply
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{_escape_xml(reply)}</Message>
</Response>"""
    return PlainTextResponse(content=twiml, media_type="application/xml")


def _escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

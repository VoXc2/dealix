"""
Dealix — WhatsApp Webhook (v2, integrated with dashboard_api event bus)
=======================================================================
Extends whatsapp_webhook.py to:
  1. Publish WS events after inbound messages
  2. Publish WS events after Groq replies
  3. Share event bus and DB with dashboard_api
  4. Keep the existing /webhook/whatsapp route working

This module is imported by main.py (unified entry point).
"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from fastapi import APIRouter, Form, Request
from fastapi.responses import PlainTextResponse, JSONResponse

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

DB_PATH = Path(os.getenv("DEALIX_DB", "/home/user/workspace/dealix-clean/dealix_leads.db"))
DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"

SYSTEM_PROMPT = """أنت مساعد مبيعات ذكي لمنصة Dealix (ديلكس) — منصة سعودية تستخدم AI Agents لتحويل المحادثات إلى صفقات مكتملة عبر WhatsApp.

قواعد صارمة:
- رد بالعربي الفصيح المبسّط بلهجة خليجية مهذبة.
- لا تزعم أي ادعاءات غير مؤكدة (مثل "معتمد ISO" أو "نسبة نجاح 100%") — ديلكس في مرحلة التدشين.
- كن مختصراً: 2-4 أسطر كحد أقصى في كل رد.
- اسأل سؤالاً واحداً كل مرة لتأهيل العميل: اسمه، مجال شركته، حجمها، أو مشكلته.
- إذا طلب العميل تسعير: اشرح أن ديلكس يقدم تجربة تجريبية مجانية، واطلب تواصله.
- نهاية المحادثة: لخّص واطلب موعد مكالمة.

أسلوبك: ودود، واثق، غير مندفع. لا emojis أكثر من 1 كل رد."""

# Router (will be mounted by main.py)
router = APIRouter(tags=["webhook"])


# ── DB helpers (sync — called from webhook handler) ───────────────────────────

def upsert_lead_sync(phone: str, tenant_id: str = DEFAULT_TENANT_ID) -> str:
    """Upsert a lead and return its id."""
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    # Check if lead exists
    row = con.execute("SELECT id FROM leads WHERE phone=? AND tenant_id=?", (phone, tenant_id)).fetchone()
    if row:
        lead_id = row["id"]
        con.execute("""
            UPDATE leads SET last_seen=?, message_count=message_count+1 WHERE id=?
        """, (now, lead_id))
    else:
        import uuid
        lead_id = str(uuid.uuid4())
        con.execute("""
            INSERT INTO leads (id, phone, first_seen, last_seen, message_count, stage, tenant_id,
                               company_name, sector, last_channel, priority_tier, score_total)
            VALUES (?,?,?,?,1,'new',?,'','other','whatsapp','cold',0)
        """, (lead_id, phone, now, now, tenant_id))
    con.commit()
    con.close()
    return lead_id


def save_message_sync(phone: str, direction: str, body: str, sid: str | None = None,
                      channel: str = "whatsapp", tenant_id: str = DEFAULT_TENANT_ID) -> int:
    """Save message synchronously; return row id."""
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB_PATH)
    cur = con.execute(
        "INSERT INTO messages (phone, direction, body, provider_sid, channel, tenant_id, created_at) "
        "VALUES (?,?,?,?,?,?,?)",
        (phone, direction, body, sid, channel, tenant_id, now),
    )
    msg_id = cur.lastrowid
    # Update/create conversation
    con.execute("""
        INSERT INTO conversations (phone, channel, last_message_preview, unread_count, tenant_id, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(phone) DO UPDATE SET
            last_message_preview=excluded.last_message_preview,
            unread_count=conversations.unread_count + (CASE WHEN ? = 'in' THEN 1 ELSE 0 END),
            updated_at=excluded.updated_at
    """, (phone, channel, body[:100], 1 if direction == "in" else 0, tenant_id, now, now, direction))
    con.commit()
    con.close()
    return msg_id


def get_history_sync(phone: str, limit: int = 10) -> list[dict[str, str]]:
    """Return last N messages as chat format for LLM context."""
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT direction, body FROM messages WHERE phone=? ORDER BY id DESC LIMIT ?",
        (phone, limit),
    ).fetchall()
    con.close()
    rows.reverse()
    return [
        {"role": "user" if d == "in" else "assistant", "content": b}
        for d, b in rows
    ]


# ── Groq LLM call ─────────────────────────────────────────────────────────────

async def groq_reply(user_message: str, history: list[dict[str, str]]) -> str:
    if not GROQ_API_KEY:
        return "مرحباً — نظامنا في وضع الصيانة مؤقتاً. سنتواصل معك قريباً."

    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    if not history or history[-1].get("content") != user_message:
        messages.append({"role": "user", "content": user_message})

    payload = {"model": GROQ_MODEL, "messages": messages, "temperature": 0.6, "max_tokens": 300}
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(GROQ_URL, json=payload, headers=headers)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[groq] error: {e}")
        return "مرحباً، شكراً لتواصلك مع Dealix. سيرد عليك مختص بأقرب وقت."


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/")
def health() -> dict[str, Any]:
    return {"service": "dealix-whatsapp-webhook", "status": "ok", "version": "2.0"}


@router.get("/leads")
def leads_debug() -> JSONResponse:
    """Debug endpoint — list leads."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT * FROM leads ORDER BY last_seen DESC LIMIT 100").fetchall()
    con.close()
    return JSONResponse([dict(r) for r in rows])


@router.post("/webhook/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str | None = Form(None),
    ProfileName: str | None = Form(None),
):
    """
    Twilio Sandbox → receive WhatsApp message → Groq reply → TwiML.
    Also publishes events to the dashboard WS event bus.
    """
    # Normalize phone
    raw = From.replace("whatsapp:", "").strip()
    digits = "".join(c for c in raw if c.isdigit())
    phone = f"+{digits}" if digits else raw
    user_msg = Body.strip()
    print(f"[inbound] {phone} ({ProfileName}): {user_msg!r}")

    # Persist
    lead_id = upsert_lead_sync(phone)
    msg_id = save_message_sync(phone, "in", user_msg, MessageSid)

    # Build reply
    history = get_history_sync(phone, limit=10)
    reply = await groq_reply(user_msg, history)
    out_id = save_message_sync(phone, "out", reply, None)

    # Publish events to dashboard WS bus
    try:
        from dashboard_api import publish_event
        inbound_msg = {
            "id": msg_id, "phone": phone, "direction": "in",
            "body": user_msg, "channel": "whatsapp",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await publish_event("message.new", {"message": inbound_msg, "phone": phone, "lead_id": lead_id})
        outbound_msg = {
            "id": out_id, "phone": phone, "direction": "out",
            "body": reply, "channel": "whatsapp",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await publish_event("message.new", {"message": outbound_msg, "phone": phone, "lead_id": lead_id})
    except ImportError:
        pass  # Running standalone

    # TwiML response
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{_escape_xml(reply)}</Message>
</Response>"""
    return PlainTextResponse(content=twiml, media_type="application/xml")


def _escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

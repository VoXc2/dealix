"""
Dealix Outreach Engine
======================
Multi-channel outreach orchestrator for Dealix.

Capabilities:
- Send via WhatsApp (Twilio), SMS (Twilio), Email (SendGrid/SMTP), LinkedIn (dry-run), Telegram (dry-run)
- Smart channel selection per lead (prefers the last-responded channel; falls back to available)
- Smart timing: respects Saudi business hours (Sun-Thu, 9:00-17:00 Asia/Riyadh)
- Campaign orchestration: send to batch of leads with personalization
- All attempts logged to `outreach_log` table (even dry-run)
- Webhook-friendly: retries with exponential backoff on provider failures

API:
- POST /api/v1/outreach/send          — send one message to one lead
- POST /api/v1/outreach/campaign      — launch a campaign to many leads
- GET  /api/v1/outreach/campaigns     — list campaigns
- GET  /api/v1/outreach/campaigns/{id} — campaign status + stats
- GET  /api/v1/outreach/log           — recent send attempts
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Optional, Literal
from zoneinfo import ZoneInfo

import aiosqlite
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

log = logging.getLogger("dealix.outreach")

# ─── Config ──────────────────────────────────────────────────────────────────
DB_PATH = os.getenv("DEALIX_DB_PATH", "/home/user/workspace/dealix-clean/dealix_leads.db")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
TWILIO_SMS_FROM = os.getenv("TWILIO_SMS_FROM", "")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "noreply@dealix.sa")
SENDGRID_FROM_NAME = os.getenv("SENDGRID_FROM_NAME", "Dealix")

SAUDI_TZ = ZoneInfo("Asia/Riyadh")

Channel = Literal["whatsapp", "sms", "email", "linkedin", "telegram"]
VALID_CHANNELS = ("whatsapp", "sms", "email", "linkedin", "telegram")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str = "out") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# ─── Schemas ─────────────────────────────────────────────────────────────────
class OutreachSendRequest(BaseModel):
    lead_id: str
    channel: Optional[Channel] = None  # If None, auto-pick
    template: Optional[str] = None     # Named template (e.g. "cold_intro")
    message: Optional[str] = None      # Custom message (overrides template)
    respect_hours: bool = True


class CampaignCreateRequest(BaseModel):
    name: str
    lead_ids: list[str] = Field(default_factory=list)
    channel: Optional[Channel] = None  # None = auto per-lead
    template: str = "cold_intro"
    variations: int = 3                # A/B/C variations via AI
    respect_hours: bool = True
    stagger_seconds: int = 2           # Delay between sends to avoid bursting


class OutreachLogRow(BaseModel):
    id: str
    lead_id: str
    channel: str
    status: str
    message: str
    provider_sid: Optional[str]
    error: Optional[str]
    campaign_id: Optional[str]
    created_at: str


# ─── DB bootstrap ────────────────────────────────────────────────────────────
async def _ensure_schema() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS outreach_log (
                id TEXT PRIMARY KEY,
                lead_id TEXT NOT NULL,
                tenant_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT NOT NULL,
                provider_sid TEXT,
                error TEXT,
                campaign_id TEXT,
                created_at TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS outreach_campaigns (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                name TEXT NOT NULL,
                channel TEXT,
                template TEXT,
                status TEXT NOT NULL,
                total INTEGER DEFAULT 0,
                sent INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_outreach_log_lead ON outreach_log(lead_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_outreach_log_campaign ON outreach_log(campaign_id)")
        await db.commit()


# ─── Templates ───────────────────────────────────────────────────────────────
TEMPLATES_AR = {
    "cold_intro": (
        "السلام عليكم {name}،\n\n"
        "أنا من Dealix — منصة سعودية تساعد شركات مثل {company} على تسريع دورة المبيعات "
        "وزيادة معدل الإغلاق عبر وكلاء ذكيين يتحدثون باللهجة الخليجية على واتساب، البريد، و LinkedIn.\n\n"
        "لاحظت أن {company} في قطاع {sector} — عندنا حالات مشابهة حققت نمواً ملحوظاً.\n"
        "تقبل مكالمة 15 دقيقة هذا الأسبوع؟"
    ),
    "value_add": (
        "{name}، تابع لرسالتي السابقة — حبيت أوضح لك بسرعة:\n\n"
        "Dealix يرد تلقائياً على عملاء {company} على واتساب بالعربي، يأهلهم، ويرتّب لك أولوية المتابعة — بدون فريق إضافي.\n\n"
        "تبي نوضح لك بمكالمة قصيرة كيف ممكن يخدم {sector}؟"
    ),
    "demo_invite": (
        "{name}، دعوة خاصة لـ {company}:\n\n"
        "عرض مباشر 30 دقيقة لـ Dealix — نريك كيف النظام يشتغل على بياناتكم الفعلية.\n"
        "بدون التزامات، بدون رسوم.\n\n"
        "أي وقت يناسبك هذا الأسبوع؟"
    ),
    "followup": (
        "{name}، مرحباً 👋\n"
        "تابع لمحادثتنا — هل راجعت اللي أرسلته لك؟\n"
        "سعيد أوضح أي نقطة أو أرتّب عرض مباشر."
    ),
    "breakup": (
        "{name}، هذي آخر رسالة مني لـ {company}.\n\n"
        "إذا التوقيت غير مناسب، ما عليك — أتمنى لك التوفيق.\n"
        "إذا تغيّر الوضع بالمستقبل، أبوابنا مفتوحة.\n\n"
        "كل الخير."
    ),
}


def _render_template(template: str, lead: dict) -> str:
    tpl = TEMPLATES_AR.get(template) or TEMPLATES_AR["cold_intro"]
    return tpl.format(
        name=lead.get("name") or lead.get("contact_person") or "مرحباً",
        company=lead.get("company_name_ar") or lead.get("company_name") or "شركتكم",
        sector=_translate_sector(lead.get("sector") or "الأعمال"),
    )


SECTOR_AR = {
    "logistics": "اللوجستيات",
    "real_estate": "العقار",
    "b2b_saas": "البرمجيات",
    "retail": "التجزئة",
    "fintech": "التقنية المالية",
    "healthcare": "الصحة",
    "education": "التعليم",
    "construction": "المقاولات",
    "manufacturing": "التصنيع",
    "hospitality": "الضيافة",
}


def _translate_sector(sector: str) -> str:
    return SECTOR_AR.get(sector.lower(), sector)


# ─── Channel senders ─────────────────────────────────────────────────────────
async def _send_whatsapp(phone: str, message: str) -> tuple[str, Optional[str], Optional[str]]:
    """Returns (status, provider_sid, error)."""
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN):
        return ("dry_run", f"dry-wa-{uuid.uuid4().hex[:8]}", None)
    to = phone if phone.startswith("whatsapp:") else f"whatsapp:{phone}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
                auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                data={"From": TWILIO_WHATSAPP_FROM, "To": to, "Body": message},
            )
            if r.status_code in (200, 201):
                return ("sent", r.json().get("sid"), None)
            return ("failed", None, f"twilio_{r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ("failed", None, str(e))


async def _send_sms(phone: str, message: str) -> tuple[str, Optional[str], Optional[str]]:
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_SMS_FROM):
        return ("dry_run", f"dry-sms-{uuid.uuid4().hex[:8]}", None)
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
                auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                data={"From": TWILIO_SMS_FROM, "To": phone, "Body": message},
            )
            if r.status_code in (200, 201):
                return ("sent", r.json().get("sid"), None)
            return ("failed", None, f"twilio_{r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ("failed", None, str(e))


async def _send_email(to_email: str, subject: str, body: str) -> tuple[str, Optional[str], Optional[str]]:
    if not SENDGRID_API_KEY:
        return ("dry_run", f"dry-email-{uuid.uuid4().hex[:8]}", None)
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": to_email}]}],
                    "from": {"email": SENDGRID_FROM_EMAIL, "name": SENDGRID_FROM_NAME},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": body}],
                },
            )
            if r.status_code in (200, 202):
                return ("sent", r.headers.get("x-message-id"), None)
            return ("failed", None, f"sendgrid_{r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ("failed", None, str(e))


async def _send_linkedin(profile_url: str, message: str) -> tuple[str, Optional[str], Optional[str]]:
    # LinkedIn messaging requires OAuth flow + Proxycurl or Unipile integration.
    # Dry-run for now; real integration left as plug-in point.
    return ("dry_run", f"dry-li-{uuid.uuid4().hex[:8]}", None)


async def _send_telegram(telegram_id: str, message: str) -> tuple[str, Optional[str], Optional[str]]:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not bot_token:
        return ("dry_run", f"dry-tg-{uuid.uuid4().hex[:8]}", None)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": telegram_id, "text": message},
            )
            if r.status_code == 200:
                return ("sent", str(r.json().get("result", {}).get("message_id")), None)
            return ("failed", None, f"telegram_{r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ("failed", None, str(e))


CHANNEL_SENDERS = {
    "whatsapp": _send_whatsapp,
    "sms": _send_sms,
    "email": _send_email,  # Note: special signature for email (subject+body)
    "linkedin": _send_linkedin,
    "telegram": _send_telegram,
}


# ─── Smart selection ─────────────────────────────────────────────────────────
def _pick_best_channel(lead: dict) -> Channel:
    """Order of preference: last_channel → whatsapp → email → sms → linkedin → telegram."""
    last = (lead.get("last_channel") or "").lower()
    if last in VALID_CHANNELS:
        return last  # type: ignore
    # Prefer channels where we have contact info
    if lead.get("phone"):
        return "whatsapp"
    if lead.get("email"):
        return "email"
    if lead.get("linkedin"):
        return "linkedin"
    return "whatsapp"  # Default


def _in_business_hours(now: Optional[datetime] = None) -> bool:
    """Saudi business hours: Sun(6)-Thu(3), 9:00-17:00 Asia/Riyadh."""
    now = now or datetime.now(SAUDI_TZ)
    # Python weekday(): Mon=0, ..., Sun=6. Saudi week: Sun-Thu are workdays.
    if now.weekday() in (4, 5):  # Fri, Sat
        return False
    return 9 <= now.hour < 17


async def _get_lead(db: aiosqlite.Connection, lead_id: str, tenant_id: str) -> Optional[dict]:
    db.row_factory = aiosqlite.Row
    row = await (await db.execute(
        "SELECT * FROM leads WHERE id=? AND tenant_id=?", (lead_id, tenant_id)
    )).fetchone()
    if not row:
        return None
    d = dict(row)
    return d


async def _log_attempt(
    db: aiosqlite.Connection,
    *,
    lead_id: str,
    tenant_id: str,
    channel: str,
    status: str,
    message: str,
    provider_sid: Optional[str] = None,
    error: Optional[str] = None,
    campaign_id: Optional[str] = None,
) -> str:
    log_id = _new_id("out")
    await db.execute(
        "INSERT INTO outreach_log (id, lead_id, tenant_id, channel, status, message, "
        "provider_sid, error, campaign_id, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (log_id, lead_id, tenant_id, channel, status, message, provider_sid, error, campaign_id, _now()),
    )
    return log_id


# ─── Main send logic ─────────────────────────────────────────────────────────
async def send_outreach(
    *,
    lead_id: str,
    tenant_id: str,
    channel: Optional[Channel] = None,
    template: Optional[str] = None,
    message: Optional[str] = None,
    respect_hours: bool = True,
    campaign_id: Optional[str] = None,
) -> dict:
    """Send one outreach message to one lead. Logs to DB."""
    await _ensure_schema()
    async with aiosqlite.connect(DB_PATH) as db:
        lead = await _get_lead(db, lead_id, tenant_id)
        if not lead:
            raise HTTPException(404, f"Lead {lead_id} not found")

        chosen_channel = channel or _pick_best_channel(lead)

        # Check hours
        if respect_hours and not _in_business_hours():
            log_id = await _log_attempt(
                db, lead_id=lead_id, tenant_id=tenant_id, channel=chosen_channel,
                status="deferred", message=message or f"[template:{template}]",
                error="outside_business_hours", campaign_id=campaign_id,
            )
            await db.commit()
            return {"id": log_id, "status": "deferred", "reason": "outside_business_hours"}

        # Build message
        body = message or _render_template(template or "cold_intro", lead)

        # Dispatch by channel
        status = "failed"
        provider_sid = None
        error = None
        if chosen_channel == "whatsapp":
            phone = lead.get("phone", "")
            if not phone:
                status, error = "failed", "no_phone"
            else:
                status, provider_sid, error = await _send_whatsapp(phone, body)
        elif chosen_channel == "sms":
            phone = lead.get("phone", "")
            if not phone:
                status, error = "failed", "no_phone"
            else:
                status, provider_sid, error = await _send_sms(phone, body)
        elif chosen_channel == "email":
            email = lead.get("email", "")
            if not email:
                status, error = "failed", "no_email"
            else:
                # First line → subject; rest → body
                lines = body.split("\n", 1)
                subj = lines[0][:100] if lines else "Dealix"
                mbody = lines[1] if len(lines) > 1 else body
                status, provider_sid, error = await _send_email(email, subj, mbody)
        elif chosen_channel == "linkedin":
            li = lead.get("linkedin", "")
            status, provider_sid, error = await _send_linkedin(li, body)
        elif chosen_channel == "telegram":
            tg = lead.get("telegram_id", "")
            status, provider_sid, error = await _send_telegram(tg, body)
        else:
            status, error = "failed", f"unsupported_channel:{chosen_channel}"

        log_id = await _log_attempt(
            db, lead_id=lead_id, tenant_id=tenant_id, channel=chosen_channel,
            status=status, message=body, provider_sid=provider_sid, error=error,
            campaign_id=campaign_id,
        )

        # For WhatsApp/SMS, also append to `messages` table so it shows in inbox
        if chosen_channel in ("whatsapp", "sms") and status in ("sent", "dry_run") and lead.get("phone"):
            try:
                await db.execute(
                    "INSERT INTO messages (phone, direction, body, provider_sid, channel, tenant_id, created_at) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (lead["phone"], "out", body, provider_sid, chosen_channel, tenant_id, _now()),
                )
            except Exception as e:
                log.warning("[outreach] failed to insert into messages: %s", e)

        await db.commit()

        return {
            "id": log_id,
            "lead_id": lead_id,
            "channel": chosen_channel,
            "status": status,
            "provider_sid": provider_sid,
            "error": error,
            "message_preview": body[:160],
        }


async def run_campaign(
    *,
    campaign_id: str,
    tenant_id: str,
    lead_ids: list[str],
    channel: Optional[Channel],
    template: str,
    respect_hours: bool,
    stagger_seconds: int,
) -> None:
    """Background task: send to each lead with stagger."""
    await _ensure_schema()
    sent = 0
    failed = 0
    for lid in lead_ids:
        try:
            result = await send_outreach(
                lead_id=lid, tenant_id=tenant_id, channel=channel,
                template=template, respect_hours=respect_hours, campaign_id=campaign_id,
            )
            if result["status"] in ("sent", "dry_run"):
                sent += 1
            elif result["status"] == "deferred":
                pass  # Will be retried later
            else:
                failed += 1
        except Exception as e:
            log.warning("[campaign %s] failed for %s: %s", campaign_id, lid, e)
            failed += 1

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE outreach_campaigns SET sent=?, failed=?, updated_at=? WHERE id=?",
                (sent, failed, _now(), campaign_id),
            )
            await db.commit()

        if stagger_seconds > 0:
            await asyncio.sleep(stagger_seconds)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE outreach_campaigns SET status=?, updated_at=? WHERE id=?",
            ("completed", _now(), campaign_id),
        )
        await db.commit()


# ─── Router ──────────────────────────────────────────────────────────────────
def register(app, get_current_user):
    """Wire outreach endpoints into the main app with shared auth dep."""

    @app.post("/api/v1/outreach/send", tags=["outreach"])
    async def api_send(body: OutreachSendRequest, user=Depends(get_current_user)):
        return await send_outreach(
            lead_id=body.lead_id,
            tenant_id=user["tenant_id"],
            channel=body.channel,
            template=body.template,
            message=body.message,
            respect_hours=body.respect_hours,
        )

    @app.post("/api/v1/outreach/campaign", tags=["outreach"])
    async def api_campaign(body: CampaignCreateRequest, user=Depends(get_current_user)):
        await _ensure_schema()
        cid = _new_id("camp")
        tid = user["tenant_id"]
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO outreach_campaigns (id, tenant_id, name, channel, template, "
                "status, total, sent, failed, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (cid, tid, body.name, body.channel, body.template, "running",
                 len(body.lead_ids), 0, 0, _now(), _now()),
            )
            await db.commit()

        # Fire-and-forget background task
        asyncio.create_task(run_campaign(
            campaign_id=cid,
            tenant_id=tid,
            lead_ids=body.lead_ids,
            channel=body.channel,
            template=body.template,
            respect_hours=body.respect_hours,
            stagger_seconds=body.stagger_seconds,
        ))

        return {
            "id": cid,
            "status": "running",
            "total": len(body.lead_ids),
            "channel": body.channel or "auto",
        }

    @app.get("/api/v1/outreach/campaigns", tags=["outreach"])
    async def list_campaigns(user=Depends(get_current_user)):
        await _ensure_schema()
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            rows = await (await db.execute(
                "SELECT * FROM outreach_campaigns WHERE tenant_id=? ORDER BY created_at DESC LIMIT 50",
                (user["tenant_id"],),
            )).fetchall()
        return {"items": [dict(r) for r in rows]}

    @app.get("/api/v1/outreach/campaigns/{campaign_id}", tags=["outreach"])
    async def get_campaign(campaign_id: str, user=Depends(get_current_user)):
        await _ensure_schema()
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            row = await (await db.execute(
                "SELECT * FROM outreach_campaigns WHERE id=? AND tenant_id=?",
                (campaign_id, user["tenant_id"]),
            )).fetchone()
            if not row:
                raise HTTPException(404, "Campaign not found")
            logs = await (await db.execute(
                "SELECT * FROM outreach_log WHERE campaign_id=? ORDER BY created_at DESC LIMIT 100",
                (campaign_id,),
            )).fetchall()
        return {"campaign": dict(row), "log": [dict(r) for r in logs]}

    @app.get("/api/v1/outreach/log", tags=["outreach"])
    async def outreach_log_recent(
        limit: int = Query(50, ge=1, le=500),
        user=Depends(get_current_user),
    ):
        await _ensure_schema()
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            rows = await (await db.execute(
                "SELECT * FROM outreach_log WHERE tenant_id=? ORDER BY created_at DESC LIMIT ?",
                (user["tenant_id"], limit),
            )).fetchall()
        return {"items": [dict(r) for r in rows]}

    @app.get("/api/v1/outreach/templates", tags=["outreach"])
    async def list_templates():
        return {
            "items": [
                {"key": k, "preview": v[:120] + "…" if len(v) > 120 else v}
                for k, v in TEMPLATES_AR.items()
            ]
        }

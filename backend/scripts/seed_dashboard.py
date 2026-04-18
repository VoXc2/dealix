"""
Dealix — Dashboard Seed Script
=================================
Populates the SQLite database with:
  - Default tenant "Dealix Demo"
  - 1 test user: sami@dealix.sa / dealix2026
  - 30 Saudi companies as leads (scored via LeadScorer)
  - 10 realistic conversations with 3-8 messages each
  - 7 agents
  - 3 playbooks (ecommerce / agency / real_estate)
  - 6 sources_health records
  - 50 activity events

Run:
    cd /home/user/workspace/dealix-clean/backend
    python scripts/seed_dashboard.py
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- Path setup so we can import app modules ---
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import aiosqlite
import bcrypt as _bcrypt

# Import intelligence modules
from app.intelligence.sources.saudi_registry import SAUDI_COMPANY_SEED
from app.intelligence.models import (
    Company,
    Contact,
    SocialHandles,
    Signal,
    SignalType,
)
from app.intelligence.scoring import LeadScorer

DB_PATH = Path(os.getenv("DEALIX_DB", "/home/user/workspace/dealix-clean/dealix_leads.db"))
DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"
TEST_USER_ID = "00000000-0000-0000-0000-000000000002"

scorer = LeadScorer()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ts(days_ago: float = 0) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def _random_ts(max_days: int = 30) -> str:
    return _ts(random.uniform(0, max_days))


STAGES = ["new", "enriching", "qualified", "contacted", "meeting", "proposal", "negotiation", "closed_won"]
STAGE_WEIGHTS = [0.15, 0.10, 0.20, 0.20, 0.15, 0.10, 0.05, 0.05]

AGENT_NAMES = [
    ("agent-wa-001", "وكيل واتساب", "whatsapp"),
    ("agent-em-001", "وكيل البريد", "email"),
    ("agent-li-001", "وكيل لينكدإن", "linkedin"),
    ("agent-sms-001", "وكيل SMS", "sms"),
    ("agent-ql-001", "وكيل التأهيل", "whatsapp"),
    ("agent-pr-001", "وكيل المقترحات", "email"),
    ("agent-cs-001", "وكيل خدمة العملاء", "whatsapp"),
]

PLAYBOOKS = [
    {
        "id": "pb-ecommerce",
        "name": "Ecommerce Growth Playbook",
        "sector": "ecommerce",
        "steps": [
            {"step": 1, "action": "WhatsApp intro", "template": "ecom_intro_ar", "delay_hours": 0},
            {"step": 2, "action": "Send case study PDF", "template": "ecom_case_study", "delay_hours": 24},
            {"step": 3, "action": "Schedule demo call", "template": "ecom_demo_invite", "delay_hours": 48},
            {"step": 4, "action": "Send proposal", "template": "ecom_proposal", "delay_hours": 72},
        ],
    },
    {
        "id": "pb-agency",
        "name": "Digital Agency Playbook",
        "sector": "digital_agency",
        "steps": [
            {"step": 1, "action": "LinkedIn connection request", "template": "agency_li_connect", "delay_hours": 0},
            {"step": 2, "action": "Email value prop", "template": "agency_email_intro", "delay_hours": 48},
            {"step": 3, "action": "WhatsApp follow-up", "template": "agency_wa_followup", "delay_hours": 72},
            {"step": 4, "action": "Partnership proposal", "template": "agency_partnership", "delay_hours": 96},
        ],
    },
    {
        "id": "pb-realestate",
        "name": "Real Estate Playbook",
        "sector": "real_estate",
        "steps": [
            {"step": 1, "action": "WhatsApp cold intro", "template": "re_intro_ar", "delay_hours": 0},
            {"step": 2, "action": "ROI calculator PDF", "template": "re_roi_calc", "delay_hours": 24},
            {"step": 3, "action": "CEO direct message", "template": "re_ceo_dm", "delay_hours": 72},
            {"step": 4, "action": "Executive demo", "template": "re_exec_demo", "delay_hours": 96},
            {"step": 5, "action": "Contract draft", "template": "re_contract", "delay_hours": 168},
        ],
    },
]

SOURCES = [
    ("saudi_registry", "ok", 1200, 0),
    ("linkedin_jobs", "ok", 840, 1),
    ("etimad_tenders", "ok", 322, 2),
    ("tech_stack_detector", "ok", 512, 0.5),
    ("news_monitor", "ok", 98, 3),
    ("gosi_employees", "partial", 0, 7),
]

CONVERSATION_TEMPLATES = [
    # (inbound_msgs, outbound_msgs)
    [
        ("in", "مرحبا، أريد معرفة المزيد عن خدماتكم"),
        ("out", "أهلاً وسهلاً! نحن في Dealix نساعد شركتك على تحويل المحادثات إلى صفقات مكتملة. ما مجال شركتكم؟"),
        ("in", "شركتنا في قطاع التجارة الإلكترونية"),
        ("out", "ممتاز! لدينا نتائج قوية مع شركات التجارة الإلكترونية. كم عدد موظفيكم؟"),
        ("in", "حوالي 50 موظف"),
    ],
    [
        ("in", "سمعت عن Dealix من زميل، كيف يعمل النظام؟"),
        ("out", "أهلاً! Dealix هو نظام ذكاء اصطناعي يدير محادثات المبيعات عبر واتساب وغيره. هل يمكنني معرفة اسمك؟"),
        ("in", "أنا أحمد، مدير المبيعات"),
        ("out", "أهلاً أحمد! هل يمكنني تحديد موعد مكالمة قصيرة لشرح النظام؟"),
        ("in", "نعم، أنا متاح غداً"),
        ("out", "سأرسل لك دعوة للمكالمة الساعة 10 صباحاً. شكراً لاهتمامك!"),
        ("in", "ممتاز، أتطلع للتحدث"),
    ],
    [
        ("in", "كم تكلفة الاشتراك في Dealix؟"),
        ("out", "لدينا تجربة مجانية 14 يوم. بعدها الباقات تبدأ من 990 ريال شهرياً. ما حجم فريق المبيعات لديكم؟"),
        ("in", "فريق صغير، 5 أشخاص"),
        ("out", "الباقة الأساسية مناسبة تماماً لكم. هل تريد أن أرتب لك عرضاً تجريبياً؟"),
    ],
    [
        ("in", "هل تدعمون اللغة العربية؟"),
        ("out", "نعم بالكامل! النظام عربي أولاً، مع دعم اللهجة الخليجية. جميع المحادثات باللغة العربية."),
        ("in", "ممتاز، هذا مهم جداً لنا"),
        ("out", "بالتأكيد! هل شركتكم في السعودية؟"),
        ("in", "نعم، في الرياض"),
        ("out", "عالي! نحن متخصصون في السوق السعودي. دعني أرسل لك دراسة حالة لشركة مشابهة."),
    ],
    [
        ("in", "ما الفرق بين Dealix والحلول الأخرى؟"),
        ("out", "Dealix متخصص بالسوق السعودي والعربي، مع AI agents تعمل 24/7 وتفهم السياق المحلي."),
        ("in", "هل لديكم عملاء في قطاع العقارات؟"),
        ("out", "نعم! لدينا playbook خاص للعقارات يعطي نتائج ممتازة. هل شركتكم في هذا القطاع؟"),
        ("in", "نعم، شركة عقارية متوسطة"),
        ("out", "رائع! سأرسل لك دراسة حالة عقارية مع أرقام حقيقية."),
        ("in", "شكراً، أنا مهتم"),
        ("out", "ممتاز! هل يمكنني الحصول على رقم الواتساب الرسمي لترتيب عرض؟"),
    ],
    [
        ("in", "مرحبا، شركتنا تبحث عن حل لأتمتة المبيعات"),
        ("out", "أهلاً! Dealix هو الحل المثالي لأتمتة المبيعات مع الذكاء الاصطناعي."),
        ("in", "هل يتكامل مع CRM؟"),
        ("out", "نعم، نتكامل مع HubSpot وSalesforce والأنظمة الرئيسية."),
    ],
    [
        ("in", "اريد تفاصيل عن خدمة الواتساب"),
        ("out", "خدمة الواتساب من Dealix تعمل 24/7 وترد على العملاء فوراً بالعربي."),
        ("in", "كم رسالة يمكن إرسالها يومياً؟"),
        ("out", "لا حد للرسائل. الباقات تختلف حسب عدد الوكلاء الذكيين."),
        ("in", "ممتاز"),
    ],
    [
        ("in", "هل توجد نسخة تجريبية مجانية؟"),
        ("out", "نعم! 14 يوم مجاناً بدون بطاقة ائتمانية. هل تريد أن أفعّل لك الحساب؟"),
        ("in", "نعم أريد"),
        ("out", "ممتاز! سأحتاج اسمك واسم الشركة ورقمك."),
        ("in", "أنا خالد الغامدي، شركة ريادة للتقنية"),
        ("out", "شكراً خالد! سأرسل لك رابط التفعيل خلال دقائق."),
    ],
    [
        ("in", "كيف يختلف Dealix عن ChatGPT؟"),
        ("out", "ChatGPT عام، Dealix متخصص بالمبيعات السعودية مع تكاملات Twilio وCRM ومتابعة Pipeline."),
        ("in", "مثير للاهتمام"),
        ("out", "هل تريد رؤية عرض توضيحي سريع؟"),
    ],
    [
        ("in", "سعركم مرتفع جداً"),
        ("out", "نفهم. يمكننا مناقشة باقة مخصصة حسب احتياجاتكم. ما ميزانيتكم الشهرية؟"),
        ("in", "حول 500 ريال شهرياً"),
        ("out", "لدينا خيارات لذلك. هل يمكنني إرسال مقترح مفصّل؟"),
        ("in", "نعم من فضلك"),
    ],
]

ACTIVITY_TEMPLATES = [
    ("وكيل واتساب", "whatsapp", "أرسل رسالة ترحيب"),
    ("وكيل البريد", "email", "أرسل بريد تعريفي"),
    ("نورة السلمان", "dashboard", "حدّث مرحلة العميل"),
    ("وكيل التأهيل", "whatsapp", "أجرى محادثة تأهيلية"),
    ("سامي العسيري", "dashboard", "راجع ملف العميل"),
    ("وكيل لينكدإن", "linkedin", "طلب تواصل على LinkedIn"),
    ("وكيل المقترحات", "email", "أرسل عرض سعر"),
    ("أحمد الزهراني", "dashboard", "أضاف ملاحظات"),
    ("وكيل واتساب", "whatsapp", "متابعة بعد الاجتماع"),
    ("نورة السلمان", "dashboard", "نقل العميل لمرحلة المفاوضات"),
]


def _make_company(data: dict) -> Company:
    """Build a Company object from seed dict."""
    social = data.get("social_handles")
    if not isinstance(social, SocialHandles):
        social = SocialHandles()

    hiring = data.get("hiring_signals", [])
    funding = data.get("funding_events", [])
    tenders = data.get("tender_wins", [])
    signals = data.get("signals", [])

    dms = []
    for dm_data in data.get("decision_makers", []):
        if isinstance(dm_data, Contact):
            dms.append(dm_data)
        elif isinstance(dm_data, dict):
            dms.append(Contact(**dm_data))

    return Company(
        id=str(uuid.uuid4()),
        name=data.get("name", ""),
        name_ar=data.get("name_ar"),
        domain=data.get("domain"),
        website=data.get("website"),
        sector=data.get("sector", "other"),
        city=data.get("city"),
        city_ar=data.get("city_ar"),
        employee_count=data.get("employee_count"),
        revenue_estimate_sar=data.get("revenue_estimate_sar"),
        ceo_name=data.get("ceo_name"),
        ceo_name_ar=data.get("ceo_name_ar"),
        tech_stack=data.get("tech_stack", []),
        ecommerce_platform=data.get("ecommerce_platform"),
        social_handles=social,
        hiring_signals=hiring,
        funding_events=funding,
        tender_wins=tenders,
        signals=signals,
        decision_makers=dms,
    )


async def seed(db_path: Path) -> None:
    print(f"[seed] Connecting to DB: {db_path}")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Run migrations first
    from dashboard_api import migrate_db
    await migrate_db()

    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

        # ── Tenant ────────────────────────────────────────────────────────────
        print("[seed] Creating default tenant...")
        await db.execute("""
            INSERT OR IGNORE INTO tenants (id, name, created_at)
            VALUES (?, ?, ?)
        """, (DEFAULT_TENANT_ID, "Dealix Demo", _now()))

        # ── Test User ─────────────────────────────────────────────────────────
        print("[seed] Creating test user sami@dealix.sa...")
        pw_hash = _bcrypt.hashpw(b"dealix2026", _bcrypt.gensalt()).decode()
        await db.execute("""
            INSERT OR IGNORE INTO users (id, tenant_id, email, password_hash, role, api_keys)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (TEST_USER_ID, DEFAULT_TENANT_ID, "sami@dealix.sa", pw_hash, "admin", "{}"))

        # ── Agents ────────────────────────────────────────────────────────────
        print("[seed] Creating 7 agents...")
        for agent_id, name, channel in AGENT_NAMES:
            msgs = random.randint(20, 120)
            await db.execute("""
                INSERT OR REPLACE INTO agents
                    (id, name, channel, status, msgs_today, success_rate, cost_today, last_activity, tenant_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                agent_id, name, channel,
                random.choice(["active", "active", "active", "paused"]),
                msgs,
                round(random.uniform(0.55, 0.92), 2),
                round(random.uniform(2.5, 15.0), 2),
                _random_ts(1),
                DEFAULT_TENANT_ID,
            ))

        # ── Playbooks ─────────────────────────────────────────────────────────
        print("[seed] Creating 3 playbooks...")
        for pb in PLAYBOOKS:
            active = random.randint(3, 18)
            await db.execute("""
                INSERT OR REPLACE INTO playbooks (id, name, sector, steps, active_count, tenant_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (pb["id"], pb["name"], pb["sector"], json.dumps(pb["steps"]), active, DEFAULT_TENANT_ID))

        # ── Sources health ─────────────────────────────────────────────────────
        print("[seed] Creating 6 sources_health records...")
        for src_name, status_, records, days_ago in SOURCES:
            await db.execute("""
                INSERT OR REPLACE INTO sources_health
                    (source_name, status, records_imported, last_sync, error, tenant_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                src_name, status_, records,
                _ts(days_ago) if days_ago is not None else None,
                None if status_ == "ok" else "API credentials not configured",
                DEFAULT_TENANT_ID,
            ))

        # ── Leads (30 Saudi companies) ─────────────────────────────────────────
        print("[seed] Scoring and inserting 30 Saudi leads...")
        lead_ids: list[str] = []

        for idx, company_data in enumerate(SAUDI_COMPANY_SEED):
            lead_id = str(uuid.uuid4())
            lead_ids.append(lead_id)

            try:
                company = _make_company(company_data)
                breakdown = scorer.score(company)
            except Exception as e:
                print(f"  [warn] scoring failed for {company_data.get('name')}: {e}")
                breakdown = type("B", (), {
                    "total_score": random.uniform(20, 80),
                    "icp_score": 50.0, "intent_score": 40.0,
                    "timing_score": 30.0, "budget_score": 50.0,
                    "authority_score": 40.0, "engagement_score": 0.0,
                    "contributing_signals": [], "penalizing_factors": [],
                })()

            score_total = round(breakdown.total_score, 1)
            if score_total >= 80:
                tier = "hot"
            elif score_total >= 60:
                tier = "warm"
            elif score_total >= 40:
                tier = "cool"
            else:
                tier = "cold"

            score_bd = {
                "icp": round(breakdown.icp_score, 1),
                "intent": round(breakdown.intent_score, 1),
                "timing": round(breakdown.timing_score, 1),
                "budget": round(breakdown.budget_score, 1),
                "authority": round(breakdown.authority_score, 1),
                "engagement": round(breakdown.engagement_score, 1),
            }

            stage = random.choices(STAGES, weights=STAGE_WEIGHTS)[0]
            agent = random.choice([a[1] for a in AGENT_NAMES])
            value_sar = round(
                (company_data.get("employee_count", 50) or 50) * random.uniform(800, 3000),
                -3
            )

            # Contacts
            contacts = []
            if company_data.get("ceo_name"):
                contacts.append({
                    "name": company_data["ceo_name"],
                    "name_ar": company_data.get("ceo_name_ar"),
                    "role": "CEO",
                    "email": None,
                    "phone": None,
                })
            for dm in company_data.get("decision_makers", []):
                if isinstance(dm, dict):
                    contacts.append({
                        "name": dm.get("full_name", ""),
                        "role": dm.get("title", ""),
                        "email": dm.get("email"),
                        "phone": dm.get("phone"),
                    })

            # Phone for conversations (synthetic)
            phone = f"+9665{random.randint(10000000, 99999999)}"

            await db.execute("""
                INSERT OR REPLACE INTO leads
                    (id, phone, name, company_name, company_name_ar, sector, city, employees,
                     score_total, score_breakdown, stage, assigned_agent, value_sar,
                     tenant_id, last_channel, priority_tier, first_seen, last_seen,
                     message_count, status, website, revenue_sar, tech_stack,
                     contributing_signals, penalizing_factors, contacts, playbook,
                     days_in_stage, owner)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                lead_id,
                phone,
                company_data.get("ceo_name", ""),
                company_data["name"],
                company_data.get("name_ar"),
                company_data.get("sector", "other") if isinstance(company_data.get("sector"), str)
                    else company_data["sector"].value,
                company_data.get("city"),
                company_data.get("employee_count", 0),
                score_total,
                json.dumps(score_bd),
                stage,
                agent,
                value_sar,
                DEFAULT_TENANT_ID,
                random.choice(["whatsapp", "email", "whatsapp", "linkedin"]),
                tier,
                _random_ts(random.randint(30, 90)),  # first_seen
                _random_ts(random.randint(0, 14)),   # last_seen
                random.randint(0, 15),
                stage,
                company_data.get("website"),
                company_data.get("revenue_estimate_sar"),
                json.dumps(company_data.get("tech_stack", [])),
                json.dumps(getattr(breakdown, "contributing_signals", [])[:5]),
                json.dumps(getattr(breakdown, "penalizing_factors", [])[:3]),
                json.dumps(contacts[:3]),
                random.choice([pb["id"] for pb in PLAYBOOKS]),
                random.randint(0, 21),
                random.choice(["نورة السلمان", "سامي العسيري", "أحمد الزهراني"]),
            ))

            # Insert signals
            signals_data = []
            if score_bd["intent"] > 50:
                signals_data.append(("intent", "إشارة توظيف نشط", score_bd["intent"] * 0.3, "linkedin_jobs"))
            if score_bd["icp"] > 70:
                signals_data.append(("icp", "تطابق قوي مع ICP", score_bd["icp"] * 0.2, "saudi_registry"))
            if company_data.get("revenue_estimate_sar", 0) > 100_000_000:
                signals_data.append(("budget", "ميزانية كبيرة مقدّرة", 15.0, "saudi_registry"))

            for cat, text, impact, src in signals_data:
                await db.execute("""
                    INSERT INTO signals (lead_id, category, text, score_impact, source, tenant_id, created_at)
                    VALUES (?,?,?,?,?,?,?)
                """, (lead_id, cat, text, impact, src, DEFAULT_TENANT_ID, _random_ts(random.randint(0, 20))))

            print(f"  [{idx+1}/30] {company_data['name']} | score={score_total} tier={tier} stage={stage}")

        # ── Conversations (10 with messages) ──────────────────────────────────
        print("[seed] Creating 10 conversations with messages...")

        # Use first 10 leads for conversations
        for i, lead_id in enumerate(lead_ids[:10]):
            lead_row = dict(await (await db.execute(
                "SELECT * FROM leads WHERE id=?", (lead_id,)
            )).fetchone())

            phone = lead_row["phone"]
            template = CONVERSATION_TEMPLATES[i % len(CONVERSATION_TEMPLATES)]
            sentiment = random.choice(["positive", "neutral", "positive", "negative"])

            # Insert conversation
            await db.execute("""
                INSERT OR REPLACE INTO conversations
                    (phone, channel, lead_name, company_name, last_message_preview,
                     unread_count, sentiment, stage, tenant_id, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                phone, "whatsapp",
                lead_row["name"] or lead_row["company_name"],
                lead_row["company_name"],
                template[-1][1][:100] if template else "",
                random.randint(0, 5),
                sentiment,
                lead_row["stage"],
                DEFAULT_TENANT_ID,
                _random_ts(random.randint(5, 30)),
                _random_ts(random.randint(0, 5)),
            ))

            # Insert messages
            msg_ts = datetime.now(timezone.utc) - timedelta(hours=random.randint(2, 72))
            for direction, body in template:
                msg_ts += timedelta(minutes=random.randint(2, 30))
                await db.execute("""
                    INSERT INTO messages (phone, direction, body, channel, tenant_id, created_at)
                    VALUES (?,?,?,?,?,?)
                """, (phone, direction, body, "whatsapp", DEFAULT_TENANT_ID, msg_ts.isoformat()))

        # ── Activities (50 events) ─────────────────────────────────────────────
        print("[seed] Creating 50 activity events...")
        for i in range(50):
            lead_id = random.choice(lead_ids)
            actor, channel, action = random.choice(ACTIVITY_TEMPLATES)
            await db.execute("""
                INSERT INTO activities
                    (lead_id, actor, channel, action, meta, trace_id, tenant_id, created_at)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                lead_id, actor, channel, action,
                json.dumps({"event_index": i}),
                str(uuid.uuid4()),
                DEFAULT_TENANT_ID,
                _random_ts(random.uniform(0, 30)),
            ))

        await db.commit()

    print("[seed] Done! Database seeded successfully.")
    print(f"       Leads: 30 | Conversations: 10 | Agents: 7 | Playbooks: 3")
    print(f"       Login: sami@dealix.sa / dealix2026")
    print(f"       DB: {db_path}")


if __name__ == "__main__":
    asyncio.run(seed(DB_PATH))

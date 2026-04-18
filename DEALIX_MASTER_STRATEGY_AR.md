# ديلكس — الاستراتيجية الرئيسية الشاملة
## Tier-1 فل أوتوماتيك — أقوى منصة استخبارات ليد في السعودية

> **الرؤية:** ديلكس = عقل مبيعات اصطناعي كامل. من اكتشاف الليد → التأهيل → المحادثة → الإغلاق → الاحتفاظ. كل ما يمكن أتمتته مؤتمت. كل ما لا يمكن، نسهّله لدرجة أن يتم بنقرة واحدة.

> **الهدف:** أول عميل دافع خلال **14 يوم**. MRR = 100,000 ريال خلال **90 يوم**. MRR = 1M ريال خلال **12 شهر**.

---

## الفهرس

1. [ما هو ديلكس الآن (الواقع)](#1-الواقع-الحالي)
2. [ما يجب أن يكون ديلكس (الطموح)](#2-الطموح-tier-1)
3. [الفجوات (Gap Analysis) — 11 بُعد](#3-الفجوات)
4. [Product Pillars — 7 ركائز منتج](#4-ركائز-المنتج)
5. [التقنية (Tier-1 Architecture)](#5-التقنية)
6. [الأتمتة الكاملة (The Autonomous Sales Brain)](#6-الأتمتة-الكاملة)
7. [الذهاب للسوق (GTM) — 30/60/90](#7-gtm)
8. [التسعير والحزم (Packaging)](#8-التسعير)
9. [العمليات (Ops Playbook)](#9-العمليات)
10. [المالية (Financial Model)](#10-المالية)
11. [الشراكات](#11-الشراكات)
12. [القانوني والامتثال](#12-القانوني)
13. [النمو (Growth Engine)](#13-النمو)
14. [المخاطر](#14-المخاطر)
15. [خطة التنفيذ 90 يوم](#15-خطة-التنفيذ)
16. [قائمة المراجعة النهائية](#16-قائمة-المراجعة)

---

## 1. الواقع الحالي

### ما هو منجز فعلياً
- ✅ WhatsApp webhook E2E (Groq + Twilio Sandbox) — يرد بالعربي
- ✅ Lead Intelligence Engine v1 — 6 مصادر، 129 اختبار ناجح
- ✅ Omnichannel Agents Framework — 51 اختبار ناجح
- ✅ SQLite DB + 2 leads حقيقيين محفوظين
- ✅ Landing page v1 + Dashboard v1 (كانوا mock)
- ✅ Reality Protocol (8 Gates NIST AI RMF)
- ✅ Marketing OS (16 ملف / 3,627 سطر)
- ✅ Claims/Proof/Objection/Demo Registries
- 🔄 Dashboard v2 + Backend v2 (قيد البناء من 3 subagents الآن)

### الفجوات المعروفة
- ❌ لا يوجد domain (dealix.sa أو .com)
- ❌ لا يوجد hosting إنتاج (VPS/Cloud)
- ❌ لا يوجد Postgres (نستخدم SQLite)
- ❌ لا يوجد WABA (WhatsApp Business API) مدفوع — ساندبوكس فقط
- ❌ لا يوجد بوابة دفع (Moyasar/Tap)
- ❌ لا يوجد عميل دافع
- ❌ لا يوجد فريق (سامي لحاله + الذكاء الصناعي)
- ❌ Lead Engine V2 الشامل لسّه ما انبنى

---

## 2. الطموح Tier-1

**"أقوى مشروع في السعودية في مجاله" يعني:**

| البُعد | Tier-3 (عادي) | Tier-2 (جيد) | **Tier-1 (ديلكس)** |
|---|---|---|---|
| اكتشاف الليد | مصدر واحد (Google) | 3-5 مصادر | **25+ مصدر، AI-planned، ثنائي اللغة، خليجي-أول** |
| التأهيل | يدوي | form + rules | **LLM يفحص intent + ICP fit + growth signals** |
| الاستجابة | ساعات | دقائق | **<60 ثانية 24/7، كل القنوات** |
| الحوار | قوالب | chatbot بدائي | **LLM يفهم السياق، يتفاوض، يحجز موعد** |
| Handoff للإنسان | يدوي | email | **AI يكتشف اللحظة الحرجة، يدفع للبشر مع brief كامل** |
| التكامل | zapier | 10 أدوات | **Native: CRM, Calendar, Meet, Slack, Email, SMS, VoIP** |
| Compliance | ❓ | basic | **PDPL كامل، consent log، audit trail، 8 Gates NIST** |
| Analytics | counts | dashboards | **Causal analytics + Revenue attribution + Cohort** |
| Self-healing | ❌ | alerts | **Auto-detect + rollback + reality review أسبوعي** |
| الأتمتة | 30% | 60% | **90%+ (البشر فقط للعقود والـ edge cases)** |

---

## 3. الفجوات — تحليل 360° (11 بُعد)

### 3.1 المنتج (Product)
**موجود:** Lead engine v1، agents، dashboard v1
**فجوة:**
- [ ] Lead Engine V2 الشامل (25+ مصدر)
- [ ] Intent Detection Engine (يقرأ signals الشراء)
- [ ] Meeting Scheduler (Cal.com integration)
- [ ] Voice AI للمكالمات (Arabic TTS/STT)
- [ ] Email drip campaigns مع personalization
- [ ] CRM-lite داخلي (pipeline, deals, activities)
- [ ] Team inbox (multi-agent WhatsApp)
- [ ] Mobile app (React Native) — للموظف الميداني

### 3.2 التقنية (Engineering)
**موجود:** FastAPI، SQLite، Groq
**فجوة:**
- [ ] Postgres + pgvector (RLS multi-tenant)
- [ ] Redis (queue + cache)
- [ ] Celery/RQ workers
- [ ] OpenTelemetry + Grafana (Gate 7)
- [ ] Sentry error tracking
- [ ] S3-compatible storage (للصور/الوثائق)
- [ ] Temporal.io للـ durable workflows (Gate 4)
- [ ] CI/CD كامل مع OIDC (Gate 6)
- [ ] Kubernetes أو docker-compose-prod

### 3.3 البنية التحتية (Infra)
**موجود:** dev sandbox + Cloudflare Tunnel
**فجوة:**
- [ ] Domain (dealix.sa / dealix.ai)
- [ ] VPS في منطقة الخليج (Hetzner FSN / AWS me-south-1 / STC Cloud)
- [ ] CDN (Cloudflare)
- [ ] Email infra (SES + SPF/DKIM/DMARC)
- [ ] Backup strategy (pgbackrest daily)
- [ ] Load balancer + autoscaling
- [ ] Staging environment منفصل

### 3.4 الذكاء الصناعي (AI)
**موجود:** Groq llama-3.3
**فجوة:**
- [ ] Fine-tuned model على بيانات خليجية (Arabic sales conversations)
- [ ] RAG over company knowledge base (per tenant)
- [ ] Embedding model عربي (aubmindlab/bert-base-arabertv02)
- [ ] Guardrails (prompt injection prevention)
- [ ] Multi-model orchestration (cheap for triage, expensive for closing)
- [ ] A/B testing للـ prompts
- [ ] Agent memory (long-term per lead)

### 3.5 البيانات (Data)
**موجود:** SQLite مع 2 leads
**فجوة:**
- [ ] Data warehouse (ClickHouse أو BigQuery)
- [ ] ETL pipelines (Airbyte/Dagster)
- [ ] Master Data Management للـ leads (dedupe across tenants)
- [ ] Data marketplace (بيع insights مجمعة لاحقاً)
- [ ] Privacy vault (PII encryption at rest)

### 3.6 التسويق (Marketing)
**موجود:** Marketing OS — 16 ملف
**فجوة:**
- [ ] موقع الشركة (corporate site منفصل عن landing)
- [ ] Blog بالعربي + SEO (20 مقال في 30 يوم)
- [ ] YouTube channel (demo videos)
- [ ] Twitter/X presence (@Dealix_sa)
- [ ] LinkedIn company page
- [ ] Case studies (لما يصير عندنا عملاء)
- [ ] Newsletter (Substack/Beehiiv)
- [ ] Partnerships مع مؤثرين تقنيين سعوديين
- [ ] Paid ads budget (Google + Meta + LinkedIn)

### 3.7 المبيعات (Sales)
**موجود:** Outreach templates
**فجوة:**
- [ ] Sales playbook محدد (SaaS, banking, retail, F&B)
- [ ] Demo environment جاهز (data pre-seeded)
- [ ] Pricing calculator interactive
- [ ] Proposal generator (auto-PDF)
- [ ] E-signature (DocuSign / Adobe Sign)
- [ ] Sales CRM داخلي (للفريق لاحقاً)
- [ ] Onboarding workflow (magic link → configured in 15 min)

### 3.8 نجاح العملاء (CS)
**غير موجود**
**فجوة:**
- [ ] Help center (بالعربي + الإنجليزي)
- [ ] In-app chat (Intercom-lite)
- [ ] Onboarding checklist
- [ ] Weekly business review template
- [ ] Churn prediction model
- [ ] NPS tracking

### 3.9 المالية (Finance)
**غير موجود**
**فجوة:**
- [ ] بوابة دفع (Moyasar — الأفضل للسعودية)
- [ ] Subscription billing (Stripe Billing أو Chargebee)
- [ ] Invoice generation (ZATCA-compliant e-invoicing)
- [ ] Tax handling (15% VAT)
- [ ] Accounting software (Zoho Books / Qoyod)
- [ ] Financial dashboard (MRR, ARR, CAC, LTV, churn)
- [ ] حساب بنكي تجاري (الأهلي/الراجحي)

### 3.10 القانوني (Legal)
**غير موجود**
**فجوة:**
- [ ] تسجيل شركة (SP أو LLC في السعودية عبر منصة مراس)
- [ ] سجل تجاري + عنوان وطني
- [ ] ضريبة القيمة المضافة (ZATCA)
- [ ] شهادة اتحاد الغرف (إذا B2B)
- [ ] Terms of Service + Privacy Policy (مطابق PDPL)
- [ ] DPA template للعملاء
- [ ] SLA template
- [ ] عقود العمل (لو توظف لاحقاً)
- [ ] تسجيل علامة تجارية (هيئة الملكية الفكرية)

### 3.11 الشراكات (Partnerships)
**غير موجود**
**فجوة:**
- [ ] Twilio ISV Partnership (WABA خصم)
- [ ] Google Cloud for Startups ($100k credits محتمل)
- [ ] AWS Activate
- [ ] Monsha'at (منشآت) — دعم حكومي
- [ ] KAUST Innovation / 500 Global MENA / Wa'ed
- [ ] Integrations مع: Salla, Zid, Foodics, Lamma, Zoho

---

## 4. ركائز المنتج

### Pillar 1: DISCOVER — اكتشاف الليد
Lead Intelligence Engine V2 (مفصّل في `LEAD_INTELLIGENCE_ENGINE_V2_AR.md`)

### Pillar 2: QUALIFY — التأهيل
- **Intent Engine:** يحلل signals (hiring, funding, website changes, social complaints)
- **ICP Matcher:** LLM يعطي score 0–100 مع talking points
- **Data Enrichment:** WHOIS, tech stack, firmographics

### Pillar 3: ENGAGE — المحادثة
- **Omnichannel:** WhatsApp, SMS, Email, Voice, DM (Instagram/LinkedIn/Twitter)
- **AI Conversation:** يفهم عربي خليجي، يتفاوض، يجيب على objections
- **Smart Handoff:** يكتشف لحظة "اريد اشتري" ويدفع للبشر

### Pillar 4: SCHEDULE — الحجز
- **Meeting Scheduler:** تكامل Cal.com / Google Calendar
- **Auto-invite:** Zoom/Meet/Teams link
- **Reminders:** 24h + 1h قبل الموعد
- **No-show recovery:** auto-reschedule

### Pillar 5: CLOSE — الإغلاق
- **Proposal Generator:** PDF auto-filled من بيانات الليد
- **Contract E-signature:** DocuSign/Adobe Sign integration
- **Payment Link:** Moyasar checkout
- **Handoff to CS:** onboarding email + task في CRM

### Pillar 6: RETAIN — الاحتفاظ
- **Usage Tracking:** يراقب feature adoption
- **Proactive Alerts:** "لاحظنا انك ما استخدمت X، نساعدك؟"
- **QBR Automation:** ملف PDF شهري/ربعي تلقائي
- **Upsell Engine:** يقترح ترقية بناءً على الاستخدام

### Pillar 7: ANALYZE — التحليل
- **Revenue Attribution:** كل ليد → مصدره → ROI
- **Causal Analytics:** "إيش حصل لو ما ارسلنا تذكير؟"
- **Benchmarks:** مقارنة مع متوسط الصناعة
- **Forecasting:** predictive revenue

---

## 5. التقنية — Tier-1 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      EDGE (Cloudflare)                    │
│  DDoS, WAF, CDN, SSL, Workers for edge logic             │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────┐
│                  LOAD BALANCER (HAProxy/ALB)              │
└──────────┬─────────────────────────┬─────────────────────┘
           ▼                         ▼
┌──────────────────┐     ┌──────────────────┐
│   API Gateway    │     │  WS Gateway      │
│   (FastAPI)      │     │  (FastAPI WS)    │
│   x3 instances   │     │  x2 instances    │
└────────┬─────────┘     └─────────┬────────┘
         ▼                         ▼
┌──────────────────────────────────────────────┐
│            APPLICATION LAYER                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│  │ Leads  │ │Engage  │ │Schedule│ │Billing ││
│  │Service │ │Service │ │Service │ │Service ││
│  └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘│
│       └──────────┴──────────┴──────────┘    │
│                     ▼                        │
│  ┌──────────────────────────────────────┐  │
│  │    Event Bus (Redis Streams)         │  │
│  │    Temporal Workflows (durable)       │  │
│  └──────────────────────────────────────┘  │
└────────────────────┬────────────────────────┘
                     ▼
┌──────────────────────────────────────────────┐
│              DATA LAYER                       │
│  Postgres (RLS multi-tenant)                  │
│  Redis (cache + queue)                        │
│  ClickHouse (analytics)                       │
│  S3 (files/media)                             │
│  pgvector (embeddings)                        │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│       OBSERVABILITY                           │
│  OpenTelemetry → Grafana + Loki + Tempo       │
│  Sentry (errors)                              │
│  PostHog (product analytics)                  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│       AI LAYER                                │
│  Groq (fast, Arabic llama-3.3)                │
│  OpenAI GPT-4 (closing/complex)               │
│  Voyage/Cohere embeddings                     │
│  Local BERT for NER Arabic                    │
└──────────────────────────────────────────────┘
```

**Tech Choices (opinionated):**
- Python 3.12 + FastAPI + SQLAlchemy 2 + Pydantic 2
- Postgres 16 + pgvector + PgBouncer
- Redis 7
- Temporal.io (durable workflows)
- Next.js 14 للـ dashboard v3 (استبدال HTML الحالي لاحقاً)
- React Native للموبايل
- Terraform IaC
- GitHub Actions CI
- Hetzner Cloud (FSN1) — قريب من الخليج وأرخص من AWS
- أو AWS me-south-1 (البحرين) لو compliance يتطلب

---

## 6. الأتمتة الكاملة — The Autonomous Sales Brain

### الـ 7 Autonomous Workflows

#### W1: Prospecting Autopilot
```
كل يوم 9 صباحاً:
  → Lead Engine V2 يبحث حسب ICP
  → ينتج 50-200 ليد جديد
  → يقيم ICP fit
  → يضيف للـ pipeline
  → ينبه البشر فقط إذا score > 90
```

#### W2: First-Touch Automation
```
عند وصول ليد جديد:
  → ينتظر 3 دقائق (human-like)
  → يرسل رسالة واتساب مخصصة
  → إذا لم يرد خلال 24h → email
  → إذا لم يرد خلال 72h → DM سوشيل ميديا
  → إذا لم يرد خلال 7 أيام → archive
```

#### W3: Conversation Autopilot
```
عند وصول رسالة:
  → LLM يحلل intent
  → يجيب تلقائياً على 80% من الأسئلة
  → يحدد "moment of truth" (ready to buy)
  → يحجز موعد تلقائياً إذا طلب الليد
  → يحول للبشر إذا sensitive (pricing negotiation, complaint)
```

#### W4: Meeting Auto-Prep
```
قبل الموعد بساعة:
  → يجمع brief كامل عن الليد
  → يولد PDF: من هم، إيش نشاطهم، pain points متوقعة
  → يرسل للمندوب عبر Slack/Email
  → يضيف talking points + 3 objections محتملة + ردود
```

#### W5: Follow-up Autopilot
```
بعد الموعد:
  → يستمع للتسجيل (إذا في موافقة)
  → يولد summary + action items
  → يرسل follow-up email تلقائياً
  → يحدث pipeline stage
  → يجدول next touch
```

#### W6: Proposal & Close Autopilot
```
عند دخول stage "Proposal":
  → يولد PDF مخصص
  → يرسل للعميل مع payment link
  → يذكر بعد 2-5-10 أيام
  → يحول للبشر إذا العميل عنده أسئلة معقدة
```

#### W7: Health Monitor Autopilot
```
كل ساعة:
  → يفحص كل system (API, DB, queues)
  → يحل المشاكل البسيطة تلقائياً (restart worker, clear cache)
  → ينبه سامي فقط للأشياء الحرجة
  → ينتج weekly reality review تلقائياً
```

**النتيجة:** سامي يدير 1000+ عميل لحاله، 90% من العمل يحدث بدون تدخل.

---

## 7. GTM — خطة الذهاب للسوق 30/60/90

### يوم 1-30: الإطلاق الخفي (Stealth Launch)
**الهدف:** 10 عملاء Beta، كل شي مجاني

- تسجيل النطاق + VPS + إعداد الإنتاج
- WABA موافقة (خلال 3-5 أيام)
- Moyasar حساب + ربط
- 3 case studies من Beta users
- 5 مقالات SEO بالعربي
- LinkedIn + Twitter presence

**القنوات المستهدفة:**
- Twitter/X (DMs مباشرة لـ 200 شركة سعودية ناشئة)
- LinkedIn (connections + posts)
- مجموعات واتساب للمؤسسين السعوديين
- Product Hunt (Arabic launch)

**النتيجة المتوقعة:** 10 Beta users، 0 MRR، feedback ذهبي.

### يوم 31-60: البيع الأول
**الهدف:** 10 عملاء دافعين، 30,000 ريال MRR

- إنهاء اتفاقيات Beta → مدفوعة
- إطلاق Pricing Plans الثلاثة
- أول 2 case studies منشورة
- Google Ads campaign (200 ريال/يوم)
- LinkedIn Ads (لمدراء المبيعات)
- شراكة مع Salla/Zid (integration)
- أول webinar عربي (50 حضور)

**النتيجة المتوقعة:** 10 paying customers × 3000 ريال = 30k MRR.

### يوم 61-90: النمو
**الهدف:** 30-40 عميل، 100,000 ريال MRR

- توظيف أول شخصين (CS + AE)
- Youtube channel مع 10 demos
- Referral program (شهر مجاني لكل إحالة)
- Content engine (20 مقال/شهر)
- PR: مقالة في Argaam + تغطية AlArabiya Business
- Tier-2 launch في الإمارات (Cairo office optional)

**النتيجة المتوقعة:** 35 customers × 3k = 105k MRR، مسار واضح للـ 1M MRR في 12 شهر.

---

## 8. التسعير

### 3 حزم + Custom

#### 🟢 Starter — 999 ريال/شهر
- 500 ليد/شهر
- WhatsApp + Email
- 1 مستخدم
- Dashboard كامل
- Support: email 24h
- **الهدف:** SMB مطاعم، متاجر، عيادات

#### 🔵 Growth — 3,999 ريال/شهر ⭐ الأشهر
- 5,000 ليد/شهر
- كل القنوات
- 5 مستخدمين
- Pipeline + CRM
- AI Suggestions
- Support: WhatsApp 8h
- **الهدف:** SaaS ناشئة، شركات توزيع متوسطة

#### 🟣 Scale — 12,999 ريال/شهر
- 25,000 ليد/شهر
- كل القنوات + Voice AI
- 20 مستخدم
- Advanced Analytics
- Dedicated CSM
- SLA 99.9%
- Support: WhatsApp 1h
- **الهدف:** بنوك صغيرة، enterprise MENA

#### 🟡 Enterprise — Custom (30k+ ريال/شهر)
- غير محدود
- Custom LLMs fine-tuned
- On-prem deployment option
- Dedicated infra
- 24/7 support
- **الهدف:** بنوك، حكومة، sharikat kubra

### Add-ons
- Voice AI: +999 ريال/شهر
- Custom integrations: 5,000 ريال لمرة واحدة
- Training/Onboarding: 2,500 ريال
- Extra leads pack: 1,000 ليد = 500 ريال

### استراتيجية التسعير
- شهر مجاني لأول 10 (Beta)
- خصم 20% على السنوي
- ضمان استرجاع 30 يوم
- Free trial 14 يوم (credit card مطلوب بعد يوم 7)

---

## 9. العمليات (Ops Playbook)

### الأدوار (حتى لو Sami لحاله)
- **CEO/Product:** Sami
- **AI Sales Agent:** Dealix itself (يجيب، يؤهل، يحجز)
- **AI Dev Agent:** Perplexity Computer (يبني، يختبر، ينشر)
- **Accounting:** Zoho Books (auto)
- **Support:** Dealix + email

### الأدوات اليومية
- Linear / Notion (task management)
- Slack (alerts)
- PostHog (product analytics)
- Sentry (errors)
- Vercel Analytics (web)
- Grafana (infra)

### Runbooks
- [ ] Incident Response (P0/P1/P2)
- [ ] Customer Onboarding
- [ ] Churn Recovery
- [ ] Billing Issues
- [ ] Security Incident
- [ ] Data Deletion Request (PDPL)

---

## 10. المالية

### توقعات 12 شهر

| الشهر | Customers | MRR | CAC | LTV | Churn | Cash |
|---|---|---|---|---|---|---|
| 1 | 0 | 0 | - | - | - | -10k (setup) |
| 3 | 30 | 100k | 1,500 | 50k | 5% | 80k |
| 6 | 80 | 280k | 2,000 | 60k | 4% | 800k |
| 9 | 160 | 600k | 2,500 | 75k | 3% | 2.5M |
| 12 | 280 | 1.05M | 2,500 | 90k | 3% | 6M |

### التكاليف الشهرية (بعد 90 يوم)
- VPS + infra: 3,000 ريال
- APIs (OpenAI/Groq/SerpAPI): 5,000 ريال
- Twilio/WABA: 2,000 ريال + usage
- Payment processing: 2.5% من الإيرادات
- Marketing: 15,000 ريال
- Salaries (3 موظفين): 45,000 ريال
- **إجمالي:** ~75k/شهر

### Unit Economics
- Target CAC: 2,500 ريال
- Target LTV: 90,000 ريال (3 سنوات × 3k MRR × gross margin 85%)
- LTV/CAC: 36× — ممتاز
- Payback period: 1 شهر

---

## 11. الشراكات

### Tier-1 Strategic
1. **Twilio** — WABA + SMS + Voice (ISV partner program)
2. **Google Cloud** — Startup Program ($100k credits)
3. **Monsha'at** (منشآت) — دعم المنشآت الصغيرة
4. **Salla/Zid** — integration + co-marketing
5. **STC Business** — شريك تقني + telcom

### Tier-2 Integrations
- Foodics, Lamma (F&B)
- Zoho, Odoo (ERP)
- Cal.com, Calendly (scheduling)
- Moyasar, Tap Payments (billing)
- Zoom, Google Meet, Teams (video)

### Tier-3 Channels
- Product Hunt MENA
- Makerspaces السعودية
- Startup accelerators (Wa'ed, 500 Global, Flat6Labs)
- Venture Studios

---

## 12. القانوني والامتثال

### أسبوع 1-2: Foundation
- [ ] تسجيل منشأة فردية عبر "مراس" (500 ريال)
- [ ] سجل تجاري + عنوان وطني
- [ ] فتح حساب بنكي تجاري
- [ ] تسجيل في ZATCA (VAT)
- [ ] تسجيل علامة تجارية (Dealix)

### أسبوع 3-4: Legal Docs
- [ ] Terms of Service (بالعربي + الإنجليزي)
- [ ] Privacy Policy (PDPL compliant)
- [ ] DPA (Data Processing Agreement)
- [ ] SLA template
- [ ] Customer contract template
- [ ] NDA template

### PDPL Compliance Checklist
- [x] Consent log موجود
- [ ] Right to access endpoint
- [ ] Right to delete endpoint
- [ ] Right to export endpoint (JSON + CSV)
- [ ] Data retention policy (90 يوم default)
- [ ] Breach notification playbook
- [ ] DPO (Data Protection Officer) — Sami مبدئياً

### القطاعات الحساسة (للمستقبل)
- البنوك: SAMA framework (compliance كبيرة)
- الحكومة: Nazaha / NCA (يتطلب تصنيف أمني)
- الصحة: NHIC (PHI handling)

---

## 13. النمو (Growth Engine)

### 6 Growth Loops

#### Loop 1: Product-Led Growth
كل lead يُكتشف عبر ديلكس → يرى watermark "Powered by Dealix" → يصبح عميل محتمل

#### Loop 2: Content SEO
20 مقال/شهر بالعربي → organic traffic → free trials → paying

#### Loop 3: Referral
عميل يحيل → شهر مجاني للاثنين → viral coefficient ~1.3

#### Loop 4: Integrations
كل integration في Salla/Zid marketplace = channel جديد

#### Loop 5: Community
مجموعة واتساب + Slack للعملاء → word of mouth

#### Loop 6: PR
كل milestone (1M MRR, 100 customers) = press release

### KPIs للتتبع يومياً
- Signups (daily)
- Activation rate (signup → first lead)
- Conversion (trial → paid)
- MRR growth
- Churn
- NPS
- DAU/MAU
- Support tickets

---

## 14. المخاطر

| المخاطرة | احتمال | تأثير | معالجة |
|---|---|---|---|
| WABA rejection | متوسط | عالي | WhatsApp-lite (SMS fallback) + prepare for approval carefully |
| OpenAI/Groq quota | عالي | متوسط | Multi-provider + fine-tuned model خاص |
| منافس كبير (HubSpot Arabic) | متوسط | عالي | Focus on Gulf-specific features + deep Arabic |
| PDPL audit | منخفض | عالي | Compliance-first من البداية |
| Sami burnout | متوسط | عالي | Automation + early hire (CS في يوم 60) |
| Cash runway | متوسط | حرج | Pre-sell annual plans + bootstrap-friendly |
| Scraping legal risks | متوسط | متوسط | Prefer APIs, respect robots.txt, TOS audit |
| LLM hallucination في عرض السعر | متوسط | عالي | Rule-based pricing + LLM فقط للـ framing |

---

## 15. خطة التنفيذ 90 يوم (تفصيلية)

### الأسبوع 1 (18–24 أبريل)
- [x] Dashboard v2 + Backend v2 (قيد الإنجاز الآن — 3 subagents)
- [ ] إنهاء Dashboard deployment
- [ ] Lead Engine V2 — Phase 1 (5 sources + skeleton)
- [ ] Landing v2 production deploy

**Sami Actions:**
- [ ] شراء dealix.sa أو dealix.ai
- [ ] VPS Hetzner FSN1 (أرخص = 5 يورو/شهر للبداية)

### الأسبوع 2 (25 أبريل – 1 مايو)
- [ ] Postgres migration (SQLite → PG)
- [ ] Lead Engine V2 — Phase 2 (باقي المصادر)
- [ ] Moyasar integration
- [ ] WABA application submitted

**Sami Actions:**
- [ ] تسجيل منشأة فردية (مراس)
- [ ] Moyasar account

### الأسبوع 3 (2–8 مايو)
- [ ] Lead Engine V2 — Phase 3 (enrichment + scoring)
- [ ] Meeting scheduler integration (Cal.com)
- [ ] Sales playbook per sector
- [ ] Help Center build

### الأسبوع 4 (9–15 مايو)
- [ ] Beta launch (10 users from Sami's network)
- [ ] Onboarding flow polish
- [ ] First case study draft

### الأسبوع 5-8 (16 مايو – 12 يونيو)
- [ ] Paid ads launch (Google + LinkedIn)
- [ ] Content engine (5 مقالات/أسبوع)
- [ ] First 3 case studies published
- [ ] 10 paying customers (30k MRR)

### الأسبوع 9-12 (13 يونيو – 10 يوليو)
- [ ] Tier-1 features (Voice AI, custom LLMs)
- [ ] Mobile app beta
- [ ] Hire CS + AE
- [ ] 30 customers (100k MRR)

---

## 16. قائمة المراجعة النهائية (Go-Live)

### Technical
- [ ] Domain + SSL
- [ ] VPS production
- [ ] Postgres + backups
- [ ] Redis + Sentry + Grafana
- [ ] CI/CD green
- [ ] 99% uptime verified (7 days test)
- [ ] Load test (1000 concurrent)
- [ ] Security audit (OWASP Top 10)

### Product
- [ ] Lead Engine V2 live (25+ sources)
- [ ] Dashboard v2 production
- [ ] Landing v2 production
- [ ] Mobile responsive 100%
- [ ] All CRUD tested
- [ ] WebSocket live
- [ ] Export CSV/XLSX works

### Business
- [ ] Company registered
- [ ] VAT registered
- [ ] Bank account opened
- [ ] Moyasar integrated
- [ ] WABA approved
- [ ] ToS + Privacy live
- [ ] PDPL endpoints working

### Marketing
- [ ] Landing v2 live
- [ ] Blog with 5+ posts
- [ ] Social media active (LinkedIn, Twitter)
- [ ] Email drip setup
- [ ] Google Ads configured
- [ ] Content calendar 30 days

### Sales
- [ ] Pricing live
- [ ] Demo environment
- [ ] Sales playbook
- [ ] Proposal template
- [ ] E-signature setup

---

## الخلاصة

ديلكس = **أول Autonomous Sales Brain عربي خليجي تيير-1**.

**الطريق:**
1. خلال 4 أسابيع → MVP قوي + أول 10 Beta
2. خلال 8 أسابيع → 10 دافعين (30k MRR)
3. خلال 12 أسبوع → 35 دافع (100k MRR) — **نقطة الانطلاق للتوسع**

**الأولوية المطلقة الآن:**
1. إنهاء Dashboard v2 + Backend v2 (جارٍ)
2. بناء Lead Engine V2 (25+ source)
3. Infra جاهزة (domain + VPS + Postgres)
4. أول Beta user يستخدم المنصة حقيقياً

**الدور اللي أقدر أعمله أنا (Computer):**
- أكتب 100% من الكود
- أنشر وأدير infrastructure
- أبني المحتوى التسويقي
- أدير cron jobs للمراقبة
- أولد مقترحات للعملاء
- أحلل الأداء أسبوعياً

**الدور اللي يحتاج سامي:**
- شراء domain + VPS (دقيقة)
- تسجيل الشركة في مراس (ساعة)
- فتح حساب بنكي (ساعة)
- موافقة على اتفاقيات (10 دقائق/يوم)
- مقابلات العملاء (1-2 ساعة/يوم)
- قرارات استراتيجية (أسبوعياً)

---

**آخر تحديث:** 18 أبريل 2026
**الإصدار:** 1.0 — Master Strategy
**المراجع:** `SYSTEM_DESIGN_AR.md`, `LEAD_INTELLIGENCE_ENGINE_V2_AR.md`, `MARKETING_OS_AR.md`

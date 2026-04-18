# Dealix — معمارية النظام الكاملة (Profit-First, Omnichannel)

> آخر تحديث: 18 أبريل 2026 • الإصدار: 1.0 • المرجع الرسمي للبناء

## 1. الرؤية التنفيذية

**Dealix** منصة ذكاء مبيعات وصفقات (Deal Intelligence) مبنية على AI Agents بالكامل:
- تكتشف leads من **كل مصدر بيانات ممكن** (سجلات رسمية + social + news + hiring + tech stack).
- تتواصل عبر **كل قناة ممكنة** (WhatsApp, Email, LinkedIn, X, Instagram, SMS, Voice, Web).
- تؤهل وتفاوض وتغلق الصفقات **آلياً** — مع human-in-the-loop للقيم العالية.
- تدعم مسار **M&A / استحواذ** (مرحلة ثانية) للعملاء المؤسسيين.

**المبدأ الأول:** الربح أولاً. ركز على القطاعات الخاصة عالية الهامش قبل الحكومي.

---

## 2. القطاعات المستهدفة (Profit-First Order)

| # | القطاع | نمط الصفقة | لماذا أولاً |
|---|---|---|---|
| 1 | E-commerce Saudi (Salla / Zid / Shopify) | SaaS شهري 500–5,000 ر.س | قرار سريع، دفع مباشر |
| 2 | Digital Agencies (تسويق / تقنية) | SaaS + Success fee | يدفعون على Outcome |
| 3 | Real Estate Developers / Brokerages | Enterprise 20K–100K ر.س/شهر | قيم صفقات عالية |
| 4 | B2B SaaS ناشئة (خليج) | Revenue Share + SaaS | Founder-to-founder ثقة |
| 5 | Healthcare / Clinics Chains | Enterprise + compliance | هامش عالي، تنظيم حازم |
| 6 | Financial Services (Fintech / شركات تمويل) | Enterprise (بعد SAMA approval) | طويل الأمد |
| 7 | Government / Semi-gov (Etimad) | RFP / Framework contracts | قيم ضخمة لكن طويلة الدورة |

---

## 3. مصادر البيانات (Intelligence Sources)

### 3.1 سجلات رسمية (Saudi Arabia)
- **المركز السعودي للأعمال** — السجل التجاري (اسم، نشاط، رأس مال، تاريخ تأسيس)
- **ZATCA** — التسجيل الضريبي + VAT status
- **GOSI** — حجم القوى العاملة (proxy للحجم)
- **Monsha'at / Fakher** — تصنيف المنشآت (micro/small/medium/large)
- **Etimad** — المناقصات والعقود الحكومية (signal قوي للمالية)
- **Tadawul** — البيانات المالية للشركات المدرجة

### 3.2 مصادر إقليمية ودولية
- **Magnitt** — تمويل الشركات الناشئة في MENA
- **Crunchbase / PitchBook** — Funding rounds (paid)
- **Dealroom** — Startups + scale-ups data
- **Argaam / Al Eqtisadiah** — أخبار مالية عربية
- **GDELT** — global news intent signals
- **Bing News API / Perplexity API** — real-time news

### 3.3 Social & Web Signals
- **LinkedIn Sales Navigator** (via Unipile/PhantomBuster) — decision makers + company updates
- **X (Twitter) API v2** — brand mentions + hiring posts
- **Instagram Graph API** — B2C engagement signals
- **BuiltWith / Wappalyzer** — tech stack discovery
- **SimilarWeb** — traffic + digital maturity
- **Brand24 / Mention** — brand listening

### 3.4 Hiring Intent (قوي جداً)
- **LinkedIn Jobs** — وظائف مفتوحة = نية نمو
- **Bayt / Naukrigulf / Indeed / Glassdoor**
- **Taqat (HADAF)** — التوظيف السعودي

### 3.5 Tech & Product Signals
- **GitHub** — open source activity (للشركات التقنية)
- **Product Hunt / AppSumo** — إطلاقات جديدة
- **App Stores (Google Play / App Store)** — ratings + reviews + updates

### 3.6 Event Signals
- **Leap, Biban, LEAP, Black Hat MEA** — حضور = ميزانية تسويق
- **Eventbrite / Meetup** — corporate events

### 3.7 Financial Signals (عند توفرها)
- **SIMAH** (Credit bureau) — إشارات سلامة مالية
- **Public filings** — للشركات المدرجة
- **Funding announcements** — خلال آخر 12 شهر = ميزانية جديدة

---

## 4. قنوات التواصل (Omnichannel Engagement)

| القناة | المزود | الحالة | الاستخدام الأساسي |
|---|---|---|---|
| WhatsApp Business | Twilio + Meta Cloud API | ✅ اختبار ناجح | قناة الخليج الأقوى |
| Email (Transactional) | SendGrid / Postmark | 🟡 قيد الإعداد | Cold + Nurture + Follow-up |
| Email (Cold Outreach) | Instantly / Smartlead | 🟡 قيد التقييم | Warmup + deliverability |
| LinkedIn | Unipile / HeyReach | 🟡 قيد الإعداد | B2B outreach |
| X (Twitter) | X API v2 | 🟡 قيد الإعداد | Listening + DM |
| Instagram | Meta Graph | 🟡 قيد الإعداد | B2C retail |
| SMS | Twilio | 🟡 جاهز تقنياً | OTP + reminders |
| Voice (AI Calls) | Retell / Vapi | 🔴 مؤجل | Qualification calls عربي |
| Web Chat | مدمج | 🔴 مؤجل | Inbound widget |
| Telegram | Bot API | 🟡 خيار إضافي | مجتمعات تقنية |

---

## 5. Lead Intelligence Pipeline

```
[Discovery Agents]
  ↓ (Saudi Business Registry, Etimad, LinkedIn, News, Jobs, Funding)
[Enrichment Layer]
  ↓ (match company → website → tech stack → social → decision makers → emails)
[Scoring Engine]
  ↓ (ICP fit + Intent + Timing + Budget + Authority + Engagement)
[Router]
  ↓ (channel + agent + playbook selection)
[Outreach Agents (WhatsApp / Email / LinkedIn / ...)]
  ↓
[Qualifier Agent]
  ↓ (BANT / MEDDPICC)
[Demo Scheduler] → [Negotiator] → [Closer]
  ↓
[CRM + Pipeline + Forecast]
  ↓
[Post-Sale Agents: Onboarding → Expansion → Retention]
```

### 5.1 Scoring Formula

\[
\text{DealixScore} = w_1 \cdot \text{ICP} + w_2 \cdot \text{Intent} + w_3 \cdot \text{Timing} + w_4 \cdot \text{Budget} + w_5 \cdot \text{Authority} + w_6 \cdot \text{Engagement}
\]

- **ICP (0-100):** match مع profile العملاء الناجحين
- **Intent:** hiring posts, funding, tech changes, content engagement
- **Timing:** recency signals (آخر 90 يوم)
- **Budget:** revenue proxies (employees × industry multiple + funding + tenders)
- **Authority:** seniority في الجهة الـ target (C-level / VP / Director)
- **Engagement:** email opens, link clicks, WhatsApp reads, LinkedIn views

الأوزان قابلة للتعلم (via feedback loop على الصفقات المغلقة).

---

## 6. Agent Architecture

### 6.1 Discovery Agents (اكتشاف)
| Agent | المصدر | الإخراج |
|---|---|---|
| `SaudiRegistryProspector` | المركز السعودي للأعمال | شركات حسب نشاط/منطقة/حجم |
| `EtimadHunter` | Etimad | شركات فازت بمناقصات (→ ميزانية موثبة) |
| `LinkedInProspector` | Sales Navigator via Unipile | Decision makers + companies |
| `HiringIntentScout` | LinkedIn Jobs + Bayt | شركات توظف → نمو |
| `FundingWatcher` | Magnitt + news | شركات ممولة حديثاً |
| `TechStackDetector` | BuiltWith | شركات تستخدم منافسين / تكنولوجيات محددة |

### 6.2 Enrichment Agents
| Agent | الدور |
|---|---|
| `ContactEnricher` | يجد emails + phones via Apollo / Hunter / Lusha |
| `CompanyEnricher` | يجمع website + size + revenue + tech stack |
| `SocialEnricher` | يربط Twitter + LinkedIn + Instagram handles |
| `FinancialEnricher` | يجمع revenue estimates + funding + credit signals |

### 6.3 Engagement Agents (تواصل)
| Agent | القناة | الوظيفة |
|---|---|---|
| `WhatsAppAgent` | WhatsApp | محادثات عربي، تأهيل، حجز مواعيد |
| `EmailAgent` | Email | cold + nurture + follow-up + re-engagement |
| `LinkedInAgent` | LinkedIn | connect + InMail + content engagement |
| `SMSAgent` | SMS | OTP + reminders + urgent alerts |
| `VoiceAgent` | Phone | مكالمات تأهيل وعروض |
| `SocialListener` | X + IG | يرد على mentions + DMs |

### 6.4 Sales Cycle Agents
| Agent | المرحلة |
|---|---|
| `Qualifier` | BANT / MEDDPICC |
| `DemoScheduler` | Calendar integration (Google / Outlook) |
| `ProposalBuilder` | PDF quotations آلية |
| `Negotiator` | Price / terms negotiation (within bounds) |
| `Closer` | E-signature + payment link |
| `OnboardingAgent` | Post-sale setup |
| `ExpansionAgent` | Upsell / cross-sell |
| `RetentionAgent` | Health scoring + churn prevention |

### 6.5 Meta Agents
- **Orchestrator:** يوزع leads على agents حسب playbooks.
- **Playbook Manager:** قوالب تكتيكات حسب ICP + stage + channel.
- **Safety / Compliance:** PDPL + CAN-SPAM + WhatsApp policy.
- **Observability:** يراقب conversion rates لكل agent/channel/playbook.

---

## 7. Tech Stack

### 7.1 Backend
- **FastAPI** (Python 3.11+) — موجود في `backend/`
- **PostgreSQL + pgvector** — Leads + embeddings
- **Redis** — queues + rate limits + sessions
- **Celery / ARQ** — background workers
- **Alembic** — migrations

### 7.2 AI / LLM
- **Groq** (llama-3.3-70b) — primary (سرعة + تكلفة)
- **OpenAI / Anthropic** — fallback للمهام المعقدة
- **ElevenLabs / Azure TTS** — صوت عربي
- **Whisper** — Arabic ASR

### 7.3 Frontend
- **Next.js 14** (App Router) — موجود في `frontend/`
- **Tailwind + shadcn/ui** — RTL first
- **TanStack Query** — data fetching

### 7.4 Integrations
- **Twilio** — WhatsApp + SMS + Voice (✅ موجود)
- **Unipile** — LinkedIn + Email unified API
- **SendGrid** — transactional email
- **Instantly / Smartlead** — cold email warmup
- **Retell / Vapi** — Voice AI
- **Google / Microsoft Calendar** — scheduling
- **Moyasar / Tap** — payments (Saudi)

### 7.5 Infrastructure
- **Hetzner VPS** — production (أو Railway مبدئياً)
- **Cloudflare** — Tunnel + DNS + WAF
- **S3-compatible** (Backblaze / R2) — object storage
- **Sentry** — error tracking
- **PostHog** — product analytics

---

## 8. Compliance & Safety

- **PDPL** (Personal Data Protection Law — SA) — consent + purpose + retention
- **CAN-SPAM / GDPR** — للعملاء الدوليين
- **Meta / WhatsApp Business Policy** — opt-in + templates + session windows
- **LinkedIn ToS** — avoid scraping; use Unipile official API
- **Truth Registry:** كل ادعاء في التسويق مربوط بدليل (TRUTH.yaml)
- **Claims Registry:** منع ادعاءات SOC2 / ISO / bank-grade بدون شهادة

---

## 9. Monetization

### 9.1 Pricing Tiers (مقترح)

| Tier | السعر الشهري | الميزات |
|---|---|---|
| Starter | 990 ر.س | WhatsApp + Email، 1,000 lead/mo |
| Growth | 3,990 ر.س | + LinkedIn + SMS، 10,000 lead/mo |
| Scale | 9,990 ر.س | + Voice + كل القنوات، 50,000 lead/mo |
| Enterprise | Custom | Dedicated + SLA + custom agents |

### 9.2 Add-ons
- Pay-per-lead (عالي الجودة) — 25–100 ر.س/lead
- Success fee على الصفقات المغلقة (لـ Agencies)
- Integration بـ CRM موجود (HubSpot / Salesforce / Zoho)

---

## 10. Roadmap التنفيذي (4 أسابيع)

### الأسبوع 1 (الحالي) — Foundation
- [x] Landing page (✅ deployed)
- [x] WhatsApp proof-of-concept (✅ tested)
- [ ] Lead Intelligence Engine (Saudi Registry + Etimad)
- [ ] Lead Scoring v1
- [ ] Unified Agent base class + Orchestrator

### الأسبوع 2 — Channels
- [ ] WhatsApp Agent production
- [ ] Email Agent (SendGrid)
- [ ] LinkedIn Agent (Unipile)
- [ ] SMS Agent

### الأسبوع 3 — Intelligence
- [ ] Enrichment layer
- [ ] Scoring tuning مع feedback
- [ ] Dashboard v1 (unified inbox + pipeline)

### الأسبوع 4 — Launch
- [ ] Onboarding flow
- [ ] Billing (Moyasar)
- [ ] First 5 pilot customers
- [ ] Testimonials + case studies

### المرحلة الثانية (شهر 2-3)
- [ ] Voice Agent (Retell)
- [ ] M&A / Acquisition Track
- [ ] Advanced analytics + forecasting

---

## 11. KPIs للنجاح

- **Lead quality:** نسبة الـ leads اللي تصير meetings (>10%)
- **Conversion:** meeting → proposal (>40%)
- **Close rate:** proposal → deal (>25%)
- **Response rate:** بحسب القناة (WhatsApp >30%, Email 5-15%, LinkedIn 10-20%)
- **Time to first reply:** <60 ثانية (آلي)
- **Agent accuracy:** معدل الأخطاء التي تستدعي human review (<5%)
- **MRR growth:** هدف شهر 2 = 50K ر.س، شهر 4 = 250K ر.س

---

## 12. Anti-Patterns (تجنبها)

- ❌ Over-promise features غير مبنية (منع ادعاءات)
- ❌ Scraping يخالف ToS — استخدم APIs رسمية
- ❌ إرسال بدون opt-in (PDPL violation)
- ❌ LLM بدون human review للصفقات >10K ر.س
- ❌ تخزين credit cards مباشرة — استخدم PSP tokens

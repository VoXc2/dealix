# Lead Intelligence Engine V2 — التصميم الشامل

> **الرؤية:** مكينة ليد حقيقية تبحث بكل طريقة ممكنة، بالعربي والإنجليزي، من كل محركات البحث وكل السوشيل ميديا وكل المصادر العامة، مع التركيز على الخليج (السعودية أولاً). الدقة أولاً، السرعة ثانياً.

**Status:** Design Phase → Implementation
**Owner:** Sami
**Related:** `SYSTEM_DESIGN_AR.md`, `backend/app/intelligence/`

---

## 1. المبادئ الأساسية

1. **عمق > سرعة:** العملية تطول ساعات أو أيام إذا لزم. المهم ليد جاهز للاستهداف.
2. **كل المصادر:** لا مصدر ممنوع إلا الـ TOS explicitly. نستعمل APIs رسمية أو public scraping حيث قانوني.
3. **ثنائي اللغة:** كل query ينفّذ بالعربي والإنجليزي، والنتائج تُدمج وتُنظف من التكرار.
4. **خليجي أولاً:** كل مصدر يدعم فلترة جغرافية (country code, phone prefix, domain TLD, map bbox) للخليج.
5. **AI في القلب:** LLM يخطط البحث (query planning)، يستخرج الكيانات (NER)، يقيم الـ ICP fit، ويولد الـ talking points.
6. **Transparent sourcing:** كل حقل في الليد يحمل provenance (من وين جاء ومتى).
7. **PDPL compliant:** consent log + right to delete/export من البداية.

---

## 2. المصادر (Sources Library)

### 2.1 محركات البحث (Search Engines)

| المصدر | الطريقة | التغطية | ملاحظات |
|---|---|---|---|
| Google Custom Search API | Official API | عالمي + خليج | مدفوع ($5/1000 query)، دقيق |
| Google SerpAPI | Third-party | عالمي | backup |
| Bing Web Search API | Azure | عالمي | رخيص |
| Yandex Search API | Official | روسي + عربي محدود | للشركات الروسية في الخليج |
| Baidu Search | Scrape | صيني | للشركات الصينية |
| DuckDuckGo | Scrape (html.duckduckgo.com) | عالمي | مجاني |
| Brave Search API | Official | عالمي | خصوصية |

**Query patterns:**
- `"مطعم" "الرياض" "+966"` (arabic + phone)
- `site:linkedin.com "Riyadh" "CEO" "SaaS"`
- `"contact us" site:.sa filetype:pdf` (للاستخراج من PDFs)
- `intext:"email" intext:"@company.sa"`

### 2.2 Google Maps / Places

| المصدر | الطريقة | البيانات |
|---|---|---|
| Google Places API (New) | Official | اسم، عنوان، هاتف، موقع، تقييم، ساعات، صور، نوع نشاط |
| Google Maps scrape (fallback) | Playwright | نفس الشي إذا quota نفد |
| Apple Maps (MapKit JS) | Official | تغطية خليجية جيدة، تكميلي |
| OpenStreetMap Nominatim | Free | backup جغرافي |

**Strategy:** لكل category × city نسوي Text Search + Nearby Search. نحفظ الـ place_id ونرجع للـ Details API لجلب الهاتف والموقع.

**Gulf focus:**
- بbox السعودية: `(16.3, 32.1) - (32.2, 55.7)`
- مدن أولوية: الرياض، جدة، الدمام، مكة، المدينة، الخبر، الطائف، بريدة، تبوك، أبها، حائل

### 2.3 السوشيل ميديا

| المنصة | الطريقة | البيانات المستخرجة |
|---|---|---|
| **LinkedIn** | Sales Navigator API (paid) / Public profile scrape | الشركات، الموظفين، الأدوار، المواقع، النشاط |
| **Twitter/X** | X API v2 (paid tier) | bio, mentions, keywords, geolocation |
| **Instagram** | Graph API (business) + public scrape | business accounts, contact buttons, bio |
| **TikTok** | TikTok for Business API | SMB accounts في الخليج |
| **Facebook** | Graph API (Pages) | pages, about, phone, email |
| **Snapchat** | Public Stories only (no API) | trends, not direct leads |
| **YouTube** | YouTube Data API v3 | channels, descriptions, contact |
| **Telegram** | Bot API + MTProto | Arabic business channels |
| **WhatsApp Business** | Catalog API / wa.me scan | business profiles |

**Tactic:** نبحث بالعربي والإنجليزي عن kewywords:
- "نبحث عن" / "looking for"
- "محتاج" / "need"
- "يعلن عن وظيفة" / "hiring" (= growth signal)
- "افتتاح" / "opening" (= new business)

### 2.4 سجلات الشركات والتراخيص الرسمية

| المصدر | الدولة | البيانات |
|---|---|---|
| **وزارة التجارة السعودية** (mc.gov.sa) | SA | السجلات التجارية، الأسماء، النشاط، الملاك |
| **منصة قوى** (qiwa.sa) | SA | الشركات والموظفين (محدود) |
| **الهيئة العامة للاستثمار** (misa.gov.sa) | SA | الاستثمار الأجنبي |
| **غرفة الرياض/جدة/الشرقية** | SA | أعضاء الغرف |
| **DED Dubai** (ded.ae) | UAE | تراخيص تجارية |
| **Abu Dhabi DED** | UAE | تراخيص أبوظبي |
| **MOCI Qatar** | QA | السجلات القطرية |
| **MOCI Kuwait** | KW | السجلات الكويتية |
| **MOIC Bahrain** | BH | السجلات البحرينية |
| **MOCIIP Oman** | OM | السجلات العمانية |
| **OpenCorporates** | عالمي | aggregator مجاني |

### 2.5 دلائل الأعمال (Business Directories)

- yellowpages.com.sa / dalil.sa / adalil.sa
- Daleeli / وتس لايت
- Zoominfo / Apollo.io / Clearbit (paid, مهم)
- Crunchbase (startups)
- AngelList / Wellfound
- Glassdoor / Bayt.com / LinkedIn Jobs (= hiring = growth)

### 2.6 WHOIS / Domain Data

- WhoisXMLAPI / DomainTools — لربط دومين بشركة
- CRT.sh — لإيجاد subdomains
- SecurityTrails — تاريخ DNS
- Wappalyzer — stack detection (هل يستخدم Shopify؟ Salla؟)

### 2.7 News / Press / PR

- GDELT Project (مجاني)
- Al Arabiya / Asharq Al-Awsat / Argaam / Sabq (RSS)
- PR Newswire / Reuters
- **Signal:** "جمعت X ريال تمويل" / "raised $X" = شركة نامية = ICP ممتاز

### 2.8 Job Boards

- Bayt, LinkedIn Jobs, Indeed, GlassDoor, Qiwa
- **Signal:** hiring للـ sales/marketing = jeeshu للمنتج

### 2.9 E-commerce / Marketplaces

- Salla, Zid stores (للبائعين السعوديين)
- Noon sellers, Amazon.sa third-party
- Foodics / Lamma (للمطاعم)

### 2.10 GitHub / Tech Signals

- GitHub users in Gulf → شركات تقنية
- Stack Overflow / Dev.to Arabic

---

## 3. المعمارية

```
┌─────────────────────────────────────────────────────────────┐
│                      DISCOVERY TRIGGER                       │
│  (Dashboard button OR API OR Cron OR Natural Language)       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  QUERY PLANNER (LLM Agent)                   │
│  Input:  ICP definition (industry, size, geo, role, signal) │
│  Output: Search strategy = list of (source, query, filter)  │
│                                                               │
│  Example Input:                                              │
│    "مطاعم في الرياض تبحث عن نظام نقاط بيع"                  │
│                                                               │
│  Example Output:                                             │
│    - google_maps: "مطعم" in Riyadh bbox                     │
│    - google_maps: "restaurant" in Riyadh bbox               │
│    - serp: site:instagram.com "مطعم الرياض"                 │
│    - serp: site:foodics.com "menu" (competitors)            │
│    - job_boards: "كاشير" OR "POS" in Riyadh                 │
│    - twitter: from:* "افتتاح مطعم" geo:Riyadh               │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               PARALLEL COLLECTORS (async workers)            │
│  [GoogleMaps] [SerpAPI] [Bing] [LinkedIn] [Instagram] ...   │
│  Each returns raw records → queue                            │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 NORMALIZATION & NER                          │
│  - extract: company_name (ar+en), phone, email, website,    │
│             address, industry, employees, decision_maker    │
│  - normalize phones to E.164                                 │
│  - validate emails (DNS MX check)                            │
│  - translate names ar↔en via LLM                             │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   DEDUP & MERGE                              │
│  - match by: domain, phone, company name fuzzy (ar+en)      │
│  - merge records; keep richest fields; log provenance       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 ENRICHMENT PIPELINE                          │
│  For each merged lead:                                       │
│    - WHOIS lookup on website                                │
│    - LinkedIn company page scrape                           │
│    - Recent news (GDELT + Arabic sources)                   │
│    - Tech stack (Wappalyzer)                                │
│    - Social presence (all platforms check)                  │
│    - Employee count estimate                                │
│    - Decision maker extraction (CEO/Founder/Marketing Head) │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              AI SCORING & ICP MATCHING                       │
│  LLM evaluates fit: 0-100                                    │
│  Factors:                                                    │
│    - Industry match                                          │
│    - Size match                                              │
│    - Geography                                               │
│    - Growth signals (hiring, funding, new location)          │
│    - Intent signals (job posting for specific role,          │
│      social media complaints about competitor)              │
│  Output: score + 3 personalized talking points              │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT LAYER                              │
│  - Save to DB (leads table with provenance JSON)            │
│  - Push to Dashboard via WebSocket                          │
│  - Export CSV/JSON/Excel                                    │
│  - Auto-trigger engagement (WhatsApp/Email/SMS) if enabled │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. هيكل الكود

```
backend/app/intelligence/v2/
├── __init__.py
├── sources/
│   ├── base.py                 # BaseSource interface
│   ├── search/
│   │   ├── google_custom.py
│   │   ├── serpapi_client.py
│   │   ├── bing.py
│   │   ├── duckduckgo.py
│   │   ├── brave.py
│   │   └── yandex.py
│   ├── maps/
│   │   ├── google_places.py
│   │   ├── apple_maps.py
│   │   └── osm_nominatim.py
│   ├── social/
│   │   ├── linkedin.py
│   │   ├── twitter_x.py
│   │   ├── instagram.py
│   │   ├── tiktok.py
│   │   ├── facebook.py
│   │   ├── youtube.py
│   │   └── telegram.py
│   ├── registries/
│   │   ├── sa_mc_gov.py        # وزارة التجارة السعودية
│   │   ├── sa_qiwa.py
│   │   ├── uae_ded.py
│   │   ├── qa_moci.py
│   │   ├── kw_moci.py
│   │   ├── bh_moic.py
│   │   ├── om_mociip.py
│   │   └── opencorporates.py
│   ├── directories/
│   │   ├── yellowpages_sa.py
│   │   ├── dalil_sa.py
│   │   ├── bayt.py
│   │   └── zoominfo.py
│   ├── whois/
│   │   ├── whoisxml.py
│   │   ├── crt_sh.py
│   │   └── wappalyzer.py
│   ├── news/
│   │   ├── gdelt.py
│   │   ├── argaam.py
│   │   └── sabq.py
│   ├── jobs/
│   │   ├── bayt.py
│   │   ├── linkedin_jobs.py
│   │   └── qiwa_jobs.py
│   └── ecommerce/
│       ├── salla_stores.py
│       ├── zid_stores.py
│       └── noon_sellers.py
├── planner.py                   # Query Planner (LLM)
├── orchestrator.py              # Parallel execution
├── normalizer.py                # NER + phone/email validation
├── dedup.py                     # Fuzzy matching ar+en
├── enrichment.py                # Post-processing pipeline
├── scoring.py                   # AI ICP scoring
├── provenance.py                # Source tracking
├── i18n.py                      # Arabic/English helpers
├── gulf_geo.py                  # Gulf bbox, cities, phone prefixes
└── api.py                       # FastAPI endpoints
```

---

## 5. API Endpoints

```
POST /api/v2/intelligence/discover
  Body: {
    "icp": {
      "industries": ["restaurants", "retail"],
      "geo": {"countries": ["SA"], "cities": ["Riyadh", "Jeddah"]},
      "size": {"min_employees": 10, "max_employees": 200},
      "roles": ["CEO", "Founder", "Marketing Manager"],
      "signals": ["hiring_sales", "recent_funding", "new_location"]
    },
    "languages": ["ar", "en"],
    "sources": ["all"] | ["google_maps", "linkedin", ...],
    "depth": "deep" | "standard" | "quick",
    "limit": 500
  }
  Returns: {"job_id": "...", "status": "running"}

GET  /api/v2/intelligence/jobs/{job_id}
  Returns: progress, partial results, ETA

GET  /api/v2/intelligence/jobs/{job_id}/leads
  Returns: full leads with scoring + provenance

POST /api/v2/intelligence/jobs/{job_id}/export?format=csv|xlsx|json

WS   /api/v2/intelligence/jobs/{job_id}/stream
  Streams leads as they're discovered
```

---

## 6. Dashboard Integration

### صفحة "Sources" (جديدة)
- شبكة بطاقات لكل مصدر (اسم، حالة، آخر استخدام، عدد الـ leads الجاءت منه)
- زر Enable/Disable لكل مصدر
- حقول API keys (مخفية افتراضياً)

### صفحة "Discover" (جديدة)
- نموذج ICP Builder:
  - اختيار صناعات (multi-select من قائمة خليجية)
  - اختيار مدن (map picker)
  - slider لحجم الشركة
  - checkboxes للإشارات (hiring, funding, ...)
  - toggle للغة (AR/EN/Both)
  - depth selector (Quick/Standard/Deep)
- زر "ابدأ البحث" → يُطلق job
- Progress bar حي + stream للـ leads كما تُكتشف

### صفحة "Leads"
- جدول مع فلاتر حسب score, source, industry, geo, date
- كل ليد → تفاصيل كاملة + provenance timeline
- actions: Add to Pipeline / Send WhatsApp / Export

---

## 7. المتطلبات قبل البناء

### API Keys (from Sami)
- [ ] Google Custom Search + Places API key
- [ ] SerpAPI key (backup)
- [ ] Bing Web Search key
- [ ] Brave Search API key
- [ ] Twitter/X Bearer Token
- [ ] LinkedIn (Sales Navigator)
- [ ] Instagram Graph Access Token
- [ ] TikTok for Business token
- [ ] WhoisXMLAPI key
- [ ] Zoominfo/Apollo (optional but powerful)

### Budget
- تقدير: $200–$500/شهر في المرحلة الأولى (مع 1000 lead/يوم)
- ينخفض مع الـ caching الذكي

### Compliance
- [ ] PDPL consent log
- [ ] Robot.txt respect في الـ scrapers
- [ ] Rate limits محترمة
- [ ] TOS audit لكل مصدر

---

## 8. خطة التنفيذ (3 مراحل)

### Phase 1 — Foundation (أسبوع 1)
1. Base interfaces (`sources/base.py`, `orchestrator.py`)
2. Gulf geo helpers + i18n
3. أول 5 مصادر: Google Places, Google CSE, Bing, DuckDuckGo, LinkedIn (public)
4. Normalizer + Dedup + Provenance
5. API skeleton + job queue

### Phase 2 — Breadth (أسبوع 2)
6. كل السوشيل ميديا (Twitter, Instagram, TikTok, Facebook, YouTube, Telegram)
7. كل السجلات الخليجية (6 دول)
8. كل الدلائل (Bayt, Dalil, YellowPages)
9. Query Planner LLM
10. AI Scoring

### Phase 3 — Depth (أسبوع 3)
11. Enrichment (WHOIS, tech stack, news)
12. Dashboard integration (صفحات Sources + Discover)
13. Streaming via WebSocket
14. Export CSV/XLSX/JSON
15. E2E tests + docs

---

## 9. مقاييس النجاح

| المقياس | Target |
|---|---|
| عدد المصادر المفعلة | 25+ |
| سرعة اكتشاف ليد | <5 ثوانٍ للأول، <30 دقيقة للـ 500 |
| دقة البيانات (هاتف/إيميل صحيح) | >85% |
| ICP Match relevance | >70% precision |
| كلفة لكل lead مؤهل | <$0.50 |
| Arabic/English parity | 100% تغطية للاثنين |
| Gulf coverage | 6 دول × 30+ مدينة |

---

## 10. مخاطر ومعالجتها

| المخاطرة | المعالجة |
|---|---|
| TOS violations | API رسمي كل ما أمكن؛ scrape فقط لما يسمح robots.txt |
| Rate limits | Token bucket لكل مصدر + rotating proxies للـ public scrape |
| كلفة APIs | Cache عدواني (7 أيام) + dedup قبل الـ call |
| PDPL | consent + right-to-delete endpoints موجودة |
| Fake/stale data | Confidence score + recency filter + human QA sample |
| LLM hallucination in NER | Validation rules (phone format, email MX, domain exists) |

---

**الخطوة التالية:** فور انتهاء الـ subagents الحاليين، أطلق subagent بناء Phase 1 كاملة.

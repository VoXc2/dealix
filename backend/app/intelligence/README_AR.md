# محرك استخبارات الـ Leads — Dealix Lead Intelligence Engine

> الإصدار 1.0.0 | Python 3.11+ | Pydantic v2 | Async-first

---

## نظرة عامة

محرك استخبارات الـ Leads هو قلب منصة **Dealix** — يكتشف ويُثري ويُسجّل عملاء B2B في المملكة العربية السعودية من مصادر بيانات متعددة.

```
[مصادر البيانات]
  ↓  المركز السعودي للأعمال · اعتماد · LinkedIn · أخبار · توظيف · تقنيات
[خط الإثراء المتوازي — EnrichmentPipeline]
  ↓  asyncio.gather → جميع المصادر في آنٍ واحد
[محرك التسجيل — LeadScorer]
  ↓  ICP + Intent + Timing + Budget + Authority + Engagement → 0-100
[المنسّق — IntelligenceOrchestrator]
  ↓  .discover() + .enrich() + .run_pipeline()
[Lead جاهز للتواصل]
```

---

## البنية الهيكلية

```
app/intelligence/
├── __init__.py              # الواجهة العامة (يستورد كل الكلاسات)
├── models.py                # نماذج Pydantic (Company, Lead, Contact, Signal...)
├── enrichment.py            # EnrichmentPipeline (متوازي)
├── scoring.py               # LeadScorer مع الشرح الكامل
├── orchestrator.py          # IntelligenceOrchestrator (واجهة رئيسية)
├── README_AR.md             # هذا الملف
└── sources/
    ├── __init__.py
    ├── saudi_registry.py    # المركز السعودي للأعمال (30 شركة seed)
    ├── etimad.py            # مناقصات اعتماد الحكومية
    ├── linkedin.py          # LinkedIn عبر Unipile API
    ├── news.py              # أخبار عربية عبر Perplexity API
    ├── hiring.py            # التوظيف (LinkedIn Jobs · Bayt · طاقات)
    └── tech_stack.py        # كشف التقنيات (BuiltWith · Wappalyzer)
```

---

## الاستخدام السريع

### تشغيل العرض التوضيحي (بدون API keys)

```bash
cd /path/to/dealix-clean/backend
python scripts/run_intelligence_demo.py
```

### استخدام Python API

```python
import asyncio
from app.intelligence import (
    IntelligenceOrchestrator,
    DiscoveryCriteria,
    Sector,
    Region,
)

async def main():
    # بدون API keys → يعمل على بيانات الـ seed
    orchestrator = IntelligenceOrchestrator()

    # اكتشاف شركات
    criteria = DiscoveryCriteria(
        sectors=[Sector.ECOMMERCE, Sector.B2B_SAAS],
        regions=[Region.RIYADH],
        min_employees=50,
        limit=20,
    )
    companies = await orchestrator.discover(criteria)

    # إثراء شركة واحدة
    lead = await orchestrator.enrich(companies[0])
    print(f"{lead.company.name}: {lead.dealix_score:.0f}/100 [{lead.priority_tier}]")

    # تشغيل الـ pipeline الكامل
    leads = await orchestrator.run_pipeline(criteria, min_score=40.0)
    for lead in leads:
        print(orchestrator.explain_lead(lead))

asyncio.run(main())
```

### من متغيرات البيئة

```python
from app.intelligence import IntelligenceOrchestrator

# يقرأ كل API keys من .env
orchestrator = IntelligenceOrchestrator.from_env()
```

---

## صيغة التسجيل

```
DealixScore = 0.25·ICP + 0.25·Intent + 0.15·Timing + 0.15·Budget + 0.10·Authority + 0.10·Engagement
```

| البُعد | الوزن | ما يقيسه |
|--------|--------|----------|
| **ICP** | 25% | تطابق الشركة مع ملف العميل المثالي (قطاع + حجم + حضور رقمي) |
| **Intent** | 25% | نية الشراء: تمويل · توظيف · مناقصات · أخبار توسع |
| **Timing** | 15% | حداثة الإشارات (آخر 90 يوم = أعلى نتيجة) |
| **Budget** | 15% | القدرة المالية: إيرادات مقدّرة + عدد موظفين + عقود حكومية |
| **Authority** | 10% | مستوى صانعي القرار المعروفين (C-level > VP > Director) |
| **Engagement** | 10% | تفاعل مع Dealix: فتح بريد · قراءة WhatsApp · LinkedIn |

### فئات الأولوية

| الفئة | النتيجة | الإجراء المقترح |
|-------|---------|----------------|
| 🔥 حارّ | 80-100 | تواصل فوري — WhatsApp + LinkedIn |
| 🟠 ساخن | 60-79 | تواصل خلال 24 ساعة |
| 🟡 دافئ | 40-59 | تسلسل nurture (Email + WhatsApp) |
| 🔵 بارد | 0-39 | حملة awareness طويلة المدى |

---

## مصادر البيانات

### ✅ يعمل الآن (بدون credentials)

| المصدر | البيانات | الحالة |
|--------|---------|--------|
| Saudi Registry Seed | 30 شركة سعودية معروفة | ✅ يعمل |
| Etimad Seed | مناقصات تجريبية | ✅ يعمل |
| News Seed | أخبار تجريبية | ✅ يعمل |
| Hiring Seed | وظائف تجريبية | ✅ يعمل |
| Tech Stack Seed | تقنيات من البيانات الموجودة | ✅ يعمل |

### 🔑 يحتاج credentials (إنتاج)

| المصدر | متغير البيئة | كيفية الحصول عليه |
|--------|------------|------------------|
| Saudi Business Center API | `SBC_API_KEY` | businesscenter.gov.sa/developers |
| ZATCA VAT Verification | `ZATCA_API_USERNAME` + `ZATCA_API_PASSWORD` | zatca.gov.sa |
| GOSI Open Data | `DATA_GOV_SA_API_TOKEN` | data.gov.sa |
| Etimad Tenders | `ETIMAD_API_KEY` | etimad.sa/open-data |
| LinkedIn (Unipile) | `UNIPILE_API_KEY` + `UNIPILE_LINKEDIN_ID` | unipile.com |
| News (Perplexity) | `PERPLEXITY_API_KEY` | perplexity.ai/settings/api |
| Bing News | `BING_NEWS_API_KEY` | microsoft.com/bing/apis |
| Tech Stack (BuiltWith) | `BUILTWITH_API_KEY` | api.builtwith.com |

---

## تشغيل الاختبارات

```bash
cd /path/to/dealix-clean/backend
pytest tests/intelligence/ -v
```

---

## متغيرات البيئة (.env)

```env
# === Saudi Data Sources ===
SBC_API_KEY=your_key_here
ZATCA_API_USERNAME=your_username
ZATCA_API_PASSWORD=your_password
ETIMAD_API_KEY=your_key_here

# === Social / LinkedIn ===
UNIPILE_API_KEY=your_key_here
UNIPILE_LINKEDIN_ID=your_account_id

# === News / Web ===
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxx
BING_NEWS_API_KEY=your_key_here

# === Tech Stack ===
BUILTWITH_API_KEY=your_key_here
```

---

## الامتثال والخصوصية

- **PDPL** (نظام حماية البيانات الشخصية السعودي) — كل بيانات الأشخاص تُجمَع من مصادر عامة معتمدة فقط.
- **LinkedIn ToS** — يستخدم Unipile API رسمياً فقط، لا web scraping.
- **Etimad** — بيانات المناقصات متاحة عبر بوابة البيانات المفتوحة.
- **opt-in required** — لا يُرسَل أي تواصل بدون موافقة المستخدم.

---

## الإضافة المستقبلية

- [ ] دمج GOSI لتحقق موثوق من حجم القوى العاملة
- [ ] إضافة مصدر Tadawul للشركات المدرجة
- [ ] دمج Magnitt لبيانات التمويل الإقليمي (MENA)
- [ ] ML model لتعلّم أوزان التسجيل من صفقات مغلقة
- [ ] Cache layer (Redis) لتجنب تكرار الاستعلامات

---

*آخر تحديث: أبريل 2026 | Dealix Engineering*

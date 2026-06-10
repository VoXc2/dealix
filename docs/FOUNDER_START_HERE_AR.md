# نقطة البداية للمؤسس — FOUNDER_START_HERE_AR

> **هذا هو الملف الوحيد الذي يجب أن تقرأه أولاً كمؤسس.** كل ما تحتاجه لبدء استخدام Dealix OS في يومك الأول، في ملف واحد.
>
> **آخر تحديث:** 2026-06-03
> **المالك:** المؤسس
> **اللغة الأساسية:** العربية
> **الإصدار:** v1.0
> **agent-context:** Agent #35 — Final Integration

---

## (a) ماذا بُني للتو — ما الذي أُنجز في الموجة الأخيرة

أُنجزت **4 أنظمة تشغيلية جديدة** (Wave 29-33)، تشكل معاً طبقة "المبيعات المؤسسية + الحوكمة + البيانات + العروض" فوق البنية القائمة. **86 ملف** جديد بين وثائق + مخططات JSON Schema + بيانات JSONL + تقارير.

| # | النظام | ماذا يفعل | التقرير النهائي |
|---|--------|-----------|-----------------|
| 1 | **Enterprise Sales OS** (Agent 29) | ABM + خريطة المشترين + MAP + Deal Risk أسبوعي | [`reports/enterprise_sales/ENTERPRISE_SALES_FINAL_REPORT.md`](../reports/enterprise_sales/ENTERPRISE_SALES_FINAL_REPORT.md) |
| 2 | **AI Agent Governance OS** (Agent 30) | A0-A5 + دورة حياة الصلاحيات + Incident Response | [`reports/ai_governance/AI_GOVERNANCE_FINAL_REPORT.md`](../reports/ai_governance/AI_GOVERNANCE_FINAL_REPORT.md) |
| 3 | **Data Products OS** (Agent 31) | 7 مكتبات (benchmarks, messages, objections, delivery, renewal, pricing, offers) | [`reports/data_products/DATA_PRODUCTS_FINAL_REPORT.md`](../reports/data_products/DATA_PRODUCTS_FINAL_REPORT.md) |
| 4 | **Offer Landing Pages** (Agent 33) | 6 صفحات عروض جاهزة + FAQ + CTA libraries | [`reports/offers/OFFER_MICRO_PRODUCTS_FINAL_REPORT.md`](../reports/offers/OFFER_MICRO_PRODUCTS_FINAL_REPORT.md) |

> **الحقيقة الصعبة:** كل نظام **PARTIAL** (ناقص founder-confirmed bands وأسماء حسابات حقيقية) — **يحتاج منك** تأكيد pricing + Tier-1 list + brand assets. انظر "أول 3 أسئلة مفتوحة" في القسم (c).

---

## (b) ماذا تقرأ — وبأي ترتيب

| الترتيب | الملف | متى تقرأه | الوقت المقدّر |
|---------|-------|-----------|---------------|
| 1 | [`docs/DEALIX_COMPANY_OS_INDEX_AR.md`](DEALIX_COMPANY_OS_INDEX_AR.md) | الآن | 5 دقائق |
| 2 | [`docs/DEALIX_COMPANY_OS_MAP_AR.md`](DEALIX_COMPANY_OS_MAP_AR.md) | الآن | 5 دقائق |
| 3 | [`docs/PRIORITY_ROADMAP_AR.md`](PRIORITY_ROADMAP_AR.md) | الآن | 5 دقائق |
| 4 | [`docs/enterprise_sales/ENTERPRISE_SALES_OS_AR.md`](enterprise_sales/ENTERPRISE_SALES_OS_AR.md) | قبل أي تواصل مع مؤسسة | 15 دقيقة |
| 5 | [`docs/ai_governance/AI_AGENT_GOVERNANCE_OS_AR.md`](ai_governance/AI_AGENT_GOVERNANCE_OS_AR.md) | قبل تفعيل أي agent جديد | 15 دقيقة |
| 6 | [`docs/data_products/DATA_PRODUCTS_OS_AR.md`](data_products/DATA_PRODUCTS_OS_AR.md) | قبل استخدام أي رقم في عرض تسعير | 10 دقائق |
| 7 | [`docs/offers/OFFER_LANDING_PAGE_SYSTEM_AR.md`](offers/OFFER_LANDING_PAGE_SYSTEM_AR.md) | قبل نشر أي صفحة | 10 دقائق |
| 8 | [`docs/DAILY_OPERATING_GUIDE_AR.md`](DAILY_OPERATING_GUIDE_AR.md) | ابتداءً من غدٍ | مرجع يومي |
| 9 | [`docs/WEEKLY_OPERATING_GUIDE_AR.md`](WEEKLY_OPERATING_GUIDE_AR.md) | كل أحد | مرجع أسبوعي |
| 10 | [`reports/final/DEALIX_COMPANY_OS_FINAL_REPORT.md`](../reports/final/DEALIX_COMPANY_OS_FINAL_REPORT.md) | لتقرير شامل نهائي | 20 دقيقة |

> **المجموع:** 100 دقيقة لأول قراءة كاملة. **لا تحاول قراءتها دفعة واحدة** — اقسمها على 3 أيام.

---

## (c) أهم 3 أسئلة مفتوحة في كل نظام

### Enterprise Sales (Agent 29)
1. **Tier-1 actual list** — من هي **3 مؤسسات سعودية** محددة (اسم + قطاع + حجم) التي ستبحث عنها في أول 30 يوماً؟ (الحالي: placeholders في `data/enterprise_sales/accounts.jsonl`).
2. **Account Selection Weights** — ما هي أوزان ABM (w1..w8) التي تريدها؟ (الحالي: placeholders).
3. **Pricing bands** — ما هي نطاقات Pilot/Annual الحقيقية (placeholders الآن)؟

### AI Agent Governance (Agent 30)
1. **A5 policy** — هل توافق على قاعدة "لا A5 في v1" (لا استقلالية تامة)، أم تريد A5 لشريك محدد؟
2. **Approval routing** — من هو الوكيل الثاني بعدك للموافقة على `external_action_capability = external_with_approval` (Sales Lead؟ CS Lead؟)؟
3. **Agent retirement SLA** — كم يوماً يجب أن يبقى agent متقاعد قبل حذفه (الحالي: 30 يوماً افتراضي)؟

### Data Products (Agent 31)
1. **Sector benchmark refresh** — كل كم شهراً تريد تحديث benchmarks (الحالي: 6 أشهر)؟
2. **Measured vs observed** — ما هي **3 KPIs** الأولى التي تريدها تتحول من `observed` إلى `measured` بعد أول pilot؟
3. **PII redaction level** — هل تقبل التجميع على مستوى قطاع فرعي (sub-vertical)، أم تطلب قطاع رئيسي فقط؟

### Offers (Agent 33)
1. **6 pricing bands** — كل عرض من 6 له band. هل تؤكّد: 0 / 499 / 1,500-3,000 / 2,999-4,999 / 7,500-15,000 / 25,000-60,000 SAR؟
2. **Calendly + WhatsApp** — أعطني الأرقام/الروابط الحقيقية لاستبدال placeholders.
3. **3 offers تحتاج مراجعة (NEEDS_REVIEW):** FULL_REVENUE_OS, MONTHLY_OPTIMIZATION, AI_REVENUE_OPS_STARTER — متى يمكننا إكمالها؟

---

## (d) أولويات 7 أيام و 30 يوماً

### أول 7 أيام (NOW)

| اليوم | الإجراء | المسؤول |
|-------|---------|---------|
| 1 (اليوم) | اقرأ هذا الملف + الفهرس + الخريطة | المؤسس |
| 1 | شغّل `bash scripts/founder_daily_runbook.sh` | المؤسس |
| 2 | اقرأ ENTERPRISE_SALES_OS_AR.md + TAP | المؤسس + Sales Lead |
| 3 | أجب عن Tier-1 list (3 مؤسسات بأسماء حقيقية) | المؤسس |
| 4 | أكّد 6 pricing bands من Offers | المؤسس |
| 5 | راجع `data/ai_governance/agent_registry.jsonl` — 7 وكلاء | المؤسس + CTO |
| 6 | أول Weekly Operating Meeting (Sunday) | المؤسس |
| 7 | راجع DEALIX_COMPANY_OS_FINAL_REPORT.md | المؤسس |

### أول 30 يوماً (NEXT)

- **Week 2:** إرسال أول outreach لـ Tier-1 (3 مؤسسات). تتبع في `data/enterprise_sales/stakeholders.jsonl`.
- **Week 3:** أول pilot proposal. تأكيد pricing bands الفعلي.
- **Week 4:** أول Agent Eval weekly — قياس 7 وكلاء موجودين. تسجيل أول حادثة في `data/ai_governance/agent_incidents.jsonl` (إن حصلت).
- **Continuous:** تحديث `data/data_products/*.jsonl` مع أي observed data.

---

## (e) أوامر اليوم الأول — انسخ والصق

### أمر 1: التحقق من الشركة (Company Ready)
```bash
bash scripts/company_ready_verify.sh
```

### أمر 2: التحقق من الإطلاق الرسمي
```bash
bash scripts/official_launch_verify.sh
# يجب أن يطبع: OFFICIAL_LAUNCH_VERDICT=PASS
```

### أمر 3: التحقق من الـ Commercial Launch
```bash
bash scripts/verify_dealix_commercial_go_live.sh
# يجب أن يطبع: DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS
```

### أمر 4: الحالة اليومية (مدة 5 دقائق)
```bash
python scripts/run_dealix_daily_ops.py --api-only
```

### أمر 5: مراجعة الأنظمة الـ 4 الجديدة
```bash
# اقرأ التقارير الـ 4 النهائية
cat reports/enterprise_sales/ENTERPRISE_SALES_FINAL_REPORT.md
cat reports/ai_governance/AI_GOVERNANCE_FINAL_REPORT.md
cat reports/data_products/DATA_PRODUCTS_FINAL_REPORT.md
cat reports/offers/OFFER_MICRO_PRODUCTS_FINAL_REPORT.md
```

### أمر 6: القواعد الخمس اليومية (5 metrics)
```bash
python scripts/founder_daily_five_metrics.py
```

### أمر 7: الخطة الشاملة (138 مهمة)
```bash
bash scripts/founder_one_command.sh
```

> **القاعدة:** لا تشغّل أي script ينشر خارجياً (إرسال WhatsApp, LinkedIn, email) قبل موافقتك الصريحة. راجع `docs/FOUNDER_GO_LIVE_DAY0_AR.md`.

---

## Open Questions for Founder

1. **ما هو قرارك اليوم** في الـ 4 pricing bands من Offers (0 / 499 / 1,500-3,000 / 2,999-4,999 / 7,500-15,000 / 25,000-60,000 SAR)؟ — هذا **يحجب** Deploy لصفحة Full Revenue OS.
2. **ما هي أول 3 شركات Tier-1** ستبدأ بها ABM؟ — هذا **يحجب** ركن `stakeholders.jsonl` الحقيقي.
3. **من هو نائبك** (Sales Lead) في approval routing لـ `external_action_capability`؟ — هذا **يحجب** تفعيل أي agent عند A4+.
4. **هل توافق** على الإبقاء على الأنظمة الجديدة (29-33) في `docs/enterprise_sales/` + `docs/ai_governance/` + `docs/data_products/` + `docs/offers/` (الحالي)، أم تريد نقلها إلى `docs/dealix_os/v1/`؟ — هذا **يؤثر** على كل cross-references.

# Service Catalog — كتالوج الخدمات

> **المرجع الحاكم (plan of record):**
> [`docs/transformation/DEALIX_COMPREHENSIVE_MASTER_PLAN.md`](../transformation/DEALIX_COMPREHENSIVE_MASTER_PLAN.md) §6.
> هذا الملف يصف **التموضع التجاري المستهدف** تحت positioning «Governed Revenue & AI Operations».
> الكتالوج البرمجي القابل للبيع حاليًا في `auto_client_acquisition/service_catalog/registry.py`
> — انظر «حالة المزامنة» في الأسفل.

## الكتالوج المستهدف — Target Catalog (7 خدمات)

| # | الخدمة | السعر (SAR) | المرحلة |
|---|--------|-------------|---------|
| 1 | **Governed Revenue Ops Diagnostic** | 4,999 – 15,000 · enterprise 15,000 – 25,000 | discovery / first_paid |
| 2 | **Revenue Intelligence Sprint** | 25,000 | sprint |
| 3 | **Governed Ops Retainer** | 4,999 – 15,000/شهر · enterprise 15,000 – 35,000/شهر | retainer |
| 4 | **AI Governance for Revenue Teams** | حسب النطاق | governance |
| 5 | **CRM / Data Readiness for AI** | حسب النطاق | data_readiness |
| 6 | **Board Decision Memo** | حسب النطاق | board |
| 7 | **Trust Pack Lite** | حسب النطاق — تُباع عند `asks_for_security` | trust |

تفاصيل المشكلة والمخرجات لكل خدمة: انظر §6 في الخطة الرئيسية.

## العروض الثلاثة الأولى — First 3 Offers

ابدأ بثلاثة فقط، بالتسلسل: **Diagnostic → Sprint → Retainer**
(الخطة الرئيسية §7). لا تُعرض الخدمات السبع دفعة واحدة.

## Blueprints per service

مجلدات التسليم القياسية: [`docs/services/`](../services/) — انظر
[`SERVICE_ID_MAP.yaml`](SERVICE_ID_MAP.yaml) لربط المجلد بـ`service_id` في الكود.

## توسع المراحل (نية)

مسار الخدمات من Sprint إلى SaaS وEnterprise:
[`DEALIX_AI_OS_LONG_TERM_AR.md`](DEALIX_AI_OS_LONG_TERM_AR.md) (قسم «الخدمات والمراحل»).

---

## حالة المزامنة — Sync Status

| الطبقة | الحالة |
|--------|--------|
| الخطة الرئيسية §6 (هذا التموضع) | **Plan of record** — معتمد |
| `registry.py` / `services-catalog.json` (الكتالوج البرمجي) | **لم يُزامَن بعد** — لا يزال يحمل الكتالوج السابق (free / 499 / 1500 / 2999/mo / …) |
| `no_overclaim.yaml` | يحمل المطالبة `governed_revenue_ai_catalog` بحالة `Planned` |

**سبب عدم مزامنة الكتالوج البرمجي فورًا:** `services-catalog.json` ملف **مُولَّد**
من `registry.py` (المصدر الوحيد — Article 11)، والكتالوج البرمجي مربوط بـ4 ملفات اختبار
+ راوتر `commercial_map.py` + إعدادات الجاهزية. إعادة تصميم الكتالوج البرمجي = مهمة هندسية
محكومة، مُدرجة في [`90_day_execution.yaml`](../../dealix/registers/90_day_execution.yaml)
كبند `P1-12`، ولا تُنشر على صفحة الهبوط قبل اجتياز بوابة الجاهزية المقابلة.

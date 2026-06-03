# حدود الأنظمة — Business System Boundaries (عربي أولًا)

> ما الذي يملكه كل نظام، وأين تنتهي مسؤوليته، وكيف لا نُكرّر أساس السوق/التجاري (Agent #1).

---

## 1. الحد الأكبر: السوق/التجاري مقابل العميل/الإيراد/التسليم

| الطبقة | المالك | الموقع | نتعامل معها كـ |
|---|---|---|---|
| السوق/التجاري (GTM) | Agent #1 | `company_os/{revenue,marketing,war_room}`, `scripts/`, `api/`, `src/` | **مرجع/مدخل فقط — لا نُكرّر ولا نُعدّل** |
| العميل/الإيراد/التسليم | Agent #2 | `docs/{whatsapp,client_portal,revenue_execution,delivery,customer_success,renewal,founder_control,business_os}`, `schemas/`, `data/`, `reports/`, `tests/` | **ملكيتنا** |

**نقطة التسليم بينهما:** "رد إيجابي / حجز / تعبئة نموذج / علاقة عميل قائمة" — من هنا تبدأ طبقاتنا.

## 2. حدود داخلية واضحة

| النظام | يملك | لا يملك (يحوّل إلى) |
|---|---|---|
| WhatsApp Client OS | المحادثة، البطاقات، الفحص | الأسرار/الملفات → البوابة؛ السعر النهائي/الدفع → تسليم بشري |
| Secure Portal | الأسرار، الملفات، الصلاحيات، المراجعات | التسعير → revenue execution؛ القرار → المؤسس |
| Revenue Execution | العرض/الإثبات/تجهيز الدفع | اعتماد السعر/الإرسال → المؤسس؛ القانوني → تسليم بشري |
| Delivery | handoff/إعداد/تقارير/قبول | التسعير الجديد → revenue؛ التجديد → renewal |
| Customer Success | صحة العميل | اعتماد التدخل → المؤسس |
| Renewal | مسودات تجديد/ترقية | الاعتماد والإرسال → المؤسس |
| Governance | المراجعة والتنبيه | أي قرار تنفيذي → المؤسس |

## 3. قواعد عدم التكرار
- كتالوج المنتجات يشير إلى SKUs في `company_os/revenue/proposals.json` عبر `sku_ref` (لا نُعيد تعريف الأسعار).
- Proof Pack يوسّع `company_os/delivery/proof_pack_template.md` (لا يُعاد كتابته).
- الإعداد يربط `company_os/delivery/p1_intake_template.md`.
- الحوكمة/الخصوصية تبني على `company_os/governance/*` (لا تُكرّر).

## 4. تعارضات قائمة موثّقة (للمؤسس)
- تكرار `company_os/company_os/**` (نسخة قديمة) — يُعتمد المستوى الأول كمصدر حقيقة.
- `package.json` يشير إلى `scripts/commercial-*.js` غير موجودة (نطاق Agent #1) — لم نُصلحها تفاديًا للتداخل.
- اختلاف enum الباقات في `db/schema.ts` (Basic/Standard/Premium) عن الكتالوج — يُعتمد الكتالوج للربط، وتُترك المواءمة في DB لـ Agent #1.

(التفصيل في `reports/business_os/CLAUDE_CLIENT_REVENUE_DELIVERY_AUDIT.md` §9.)

---
*المرجع الحاكم: `AGENTS.md`.*

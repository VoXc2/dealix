# حزم Dealix التجارية — التشغيل المحكوم للإيراد والذكاء الاصطناعي

**المرجع الشامل لشركة التشغيل:** [DEALIX_AI_OPERATING_COMPANY_AR.md](DEALIX_AI_OPERATING_COMPANY_AR.md)
**كتالوج الخدمات (مصدر الحقيقة):** [../COMPANY_SERVICE_LADDER.md](../COMPANY_SERVICE_LADDER.md)
**مقاييس North Star:** [NORTH_STAR_METRICS_AR.md](NORTH_STAR_METRICS_AR.md)
**كود الكتالوج:** `auto_client_acquisition/service_catalog/registry.py`

## الموقف التجاري

Dealix تُباع كـ **شركة تشغيل محكوم للإيراد والذكاء الاصطناعي**: نرتّب البيانات،
نحدّد الفرص، نجهّز مسودات آمنة، نوضّح الـ pipeline، ونخرج تقارير مربوطة بـ
**Decision Passport** و**Proof** وبآلة الحالة [CEL](COMMERCIAL_EVIDENCE_STATE_MACHINE.md).
ليست استشارة نماذج لغوية عابرة، ولا SaaS رخيص بلا مخرجات ملموسة.

**قواعد منتج غير قابلة للمساومة:**

- لا إرسال بارد (واتساب / LinkedIn automation) — مسودات وموافقة أولاً.
- لا قوائم مشتراة ولا scraping إنتاجي.
- أي «Outreach» في العروض = **Draft Pack** فقط حتى موافقة صريحة (`CEL4`).
- لا أسعار ثابتة لخدمة `recommended_draft` قبل **3 بايلوتات مدفوعة**.
- لا اعتراف بإيراد قبل `invoice_paid` (`CEL7_confirmed`).

## نموذج التسعير

| `price_mode` | المعنى |
|--------------|--------|
| `range` | نطاق min–max حقيقي يسعّر المؤسس داخله حسب النطاق. |
| `recommended_draft` | لا رقم ثابت بعد — يُسعّر لكل ارتباط حتى تُنضج 3 بايلوتات مدفوعة نطاقاً. |
| `fixed` | سعر واحد مؤكد — يُستخدم فقط بعد دليل كافٍ. |

## الخدمات السبع

| # | الخدمة | `price_mode` | السعر (ريال) |
|---|--------|--------------|---------------|
| 1 | Governed Revenue Ops Diagnostic | `range` | 4,999 – 25,000 |
| 2 | Revenue Intelligence Sprint | `recommended_draft` | حسب النطاق |
| 3 | Governed Ops Retainer | `recommended_draft` | حسب الشهر |
| 4 | AI Governance for Revenue Teams | `recommended_draft` | حسب النطاق |
| 5 | CRM / Data Readiness for AI | `recommended_draft` | حسب النطاق |
| 6 | Board Decision Memo | `recommended_draft` | حسب النطاق |
| 7 | Trust Pack Lite | `recommended_draft` | حسب النطاق |

## العروض الثلاثة الرئيسية (ابدأ بها)

لا تعرض سبع خدمات في أول رسالة. اعرض ثلاثة فقط:

1. **Governed Revenue Ops Diagnostic** — التشخيص، نقطة الدخول.
2. **Revenue Intelligence Sprint** — الخدمة الأساسية بعد التشخيص.
3. **Governed Ops Retainer** — الارتباط المتكرر بعد أول Sprint.

> رسالة البيع: «نبدأ بتشخيص صغير، إذا أثبت قيمة ننتقل إلى Sprint، وإذا تكرر
> الـ workflow نحوّله إلى Retainer.»

## 1) Governed Revenue Ops Diagnostic — نطاق 4,999–25,000 ريال

**يشمل:** Revenue Workflow Map، مراجعة جودة CRM/المصادر، خريطة مخاطر pipeline،
تحليل فجوات المتابعة، Decision Passport، فرص لإثبات القيمة، توصية Sprint/Retainer.
**لا يشمل:** تنظيف كامل للداتا، إعداد CRM كامل، تنفيذ outreach، تكاملات عميقة.
النطاق الأعلى للشركات الأكبر.

## 2) Revenue Intelligence Sprint — `recommended_draft`

**يشمل:** ترتيب الحسابات، تسجيل مخاطر الصفقات، مسودات الإجراء التالي، قوالب
متابعة، Revenue Opportunity Ledger، Decision Passport، Proof Pack.
**لا يشمل:** إرسال فعلي لطرف ثالث، أتمتة LinkedIn، واتساب بارد، ضمان تحويل رقمي.

## 3) Governed Ops Retainer — `recommended_draft` / شهرياً

**مخرجات شهرية:** مراجعة إيراد، مراجعة جودة pipeline، مراجعة قرارات AI، طابور
متابعة معتمد، Risk Register، تقرير قيمة، Board Memo. هذا طريق الإيراد المتكرر.

## 4–7) الخدمات المساندة

- **AI Governance for Revenue Teams:** أفعال AI مسموحة/ممنوعة، حدود موافقة،
  قواعد مصدر، سياسة عدم الإرسال الخارجي التلقائي، تسجيل أدلة.
- **CRM / Data Readiness for AI:** تقرير نظافة CRM، خريطة مصادر، حقول ناقصة،
  حسابات مكررة، مراحل دورة حياة خاطئة، درجة جاهزية بيانات. يُباع قبل أي أتمتة AI.
- **Board Decision Memo:** أهم قرارات الإيراد، مخاطر pipeline والحوكمة، تخصيص
  رأس مال، توصيات بناء/إبقاء/إيقاف.
- **Trust Pack Lite:** سياسة أفعال AI، مصفوفة موافقات، التعامل مع الأدلة،
  أفعال ممنوعة، قواعد سلامة الوكيل. يُباع فقط على إشارة (`asks_for_security`).

## ربط المنتج — أين يدعم الكود الحالي كل عرض؟

| عنصر تسليم | مسار / وحدة في الريبو | ملاحظة |
|------------|----------------------|--------|
| كتالوج الخدمات | `GET /api/v1/services`، `service_catalog/registry.py` | مصدر الحقيقة للأسعار |
| تشخيص Revenue Ops + جواز قرار | `POST /api/v1/revenue-ops/diagnostics`، `revenue_ops/` | مسار تشخيص كامل |
| رفع CRM Export | `POST /api/v1/revenue-ops/upload`، إعادة استخدام `data_os` | استيراد ومعاينة جودة |
| تسجيل الفرص/المخاطر | `POST /api/v1/revenue-ops/score` | scoring deterministic |
| Decision Passport | `GET /api/v1/revenue-ops/{id}/decision-passport` | إعادة استخدام `decision_passport` |
| مسودات المتابعة | `POST /api/v1/revenue-ops/{id}/follow-up-drafts` | تمر عبر `draft_gate` + Approval Center |
| أحداث الأدلة وانتقالات CEL | `POST /api/v1/evidence/events`، `commercial_os/` | يرفض الانتقال غير المشروع 422 |
| الموافقات | `POST /api/v1/approvals`، `approval_center` | لا قناة خارجية بلا موافقة |

## مسار البيع

```text
Diagnostic -> Revenue Intelligence Sprint -> Governed Ops Retainer
```

كل ترقية مشروطة بدليل من المرحلة السابقة وببوابة من
[COMMERCIAL_GATES.md](COMMERCIAL_GATES.md).

## روابط داخلية

- [كتالوج الخدمات](../COMPANY_SERVICE_LADDER.md)
- [آلة الحالة CEL](COMMERCIAL_EVIDENCE_STATE_MACHINE.md)
- [البوابات التجارية](COMMERCIAL_GATES.md)
- [رسالة البيع](SALES_MESSAGE.md)
